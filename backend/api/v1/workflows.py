"""
Workflow orchestration API endpoints.

Provides endpoints for creating, managing, and executing multi-agent workflows.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.session import get_db
from models.user import User
from models.workflow import (
    AgentWorkflow,
    WorkflowExecution,
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowInDB,
    WorkflowExecutionCreate,
    WorkflowExecutionInDB,
    WorkflowExecutionDetail,
    WorkflowStatus,
    WorkflowExecutionStatus,
)
from core.security import get_current_user
from api.v1.agents import invoke_agent
from datetime import datetime
import json


router = APIRouter()


# ============================================================================
# Workflow CRUD Operations
# ============================================================================


@router.post("/", response_model=WorkflowInDB, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_data: WorkflowCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new workflow.

    Workflows allow chaining multiple agents together in sequence,
    passing outputs from one agent as inputs to the next.
    """
    # Convert Pydantic models to dict for JSON storage
    steps_json = [step.model_dump() for step in workflow_data.steps]

    workflow = AgentWorkflow(
        name=workflow_data.name,
        description=workflow_data.description,
        created_by=current_user.id,
        is_template=False,  # User workflows are not templates by default
        is_public=workflow_data.is_public,
        status=WorkflowStatus.DRAFT,
        steps=steps_json,
        tags=workflow_data.tags,
    )

    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    return workflow


@router.get("/", response_model=List[WorkflowInDB])
async def list_workflows(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: Optional[WorkflowStatus] = None,
    is_template: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List workflows accessible to the current user.

    Returns workflows created by the user, plus public workflows and templates.
    """
    query = db.query(AgentWorkflow)

    # Filter: User's own workflows OR public workflows OR templates
    query = query.filter(
        (AgentWorkflow.created_by == current_user.id)
        | (AgentWorkflow.is_public == True)
        | (AgentWorkflow.is_template == True)
    )

    # Optional filters
    if status_filter:
        query = query.filter(AgentWorkflow.status == status_filter.value)

    if is_template is not None:
        query = query.filter(AgentWorkflow.is_template == is_template)

    if search:
        query = query.filter(
            (AgentWorkflow.name.ilike(f"%{search}%"))
            | (AgentWorkflow.description.ilike(f"%{search}%"))
        )

    # Order by most recently updated
    query = query.order_by(desc(AgentWorkflow.updated_at))

    workflows = query.offset(skip).limit(limit).all()
    return workflows


@router.get("/{workflow_id}", response_model=WorkflowInDB)
async def get_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get workflow details by ID."""
    workflow = db.query(AgentWorkflow).filter(AgentWorkflow.id == workflow_id).first()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Check access: owner, public, or template
    if (
        workflow.created_by != current_user.id
        and not workflow.is_public
        and not workflow.is_template
    ):
        raise HTTPException(status_code=403, detail="Access denied")

    return workflow


@router.put("/{workflow_id}", response_model=WorkflowInDB)
async def update_workflow(
    workflow_id: int,
    workflow_data: WorkflowUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an existing workflow (owner only)."""
    workflow = db.query(AgentWorkflow).filter(AgentWorkflow.id == workflow_id).first()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Only owner can update
    if workflow.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can update this workflow")

    # Update fields if provided
    update_data = workflow_data.model_dump(exclude_unset=True)

    # Handle steps conversion
    if "steps" in update_data and update_data["steps"]:
        update_data["steps"] = [step.model_dump() for step in workflow_data.steps]

    for field, value in update_data.items():
        setattr(workflow, field, value)

    db.commit()
    db.refresh(workflow)

    return workflow


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a workflow (owner only)."""
    workflow = db.query(AgentWorkflow).filter(AgentWorkflow.id == workflow_id).first()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Only owner can delete
    if workflow.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can delete this workflow")

    db.delete(workflow)
    db.commit()


# ============================================================================
# Workflow Execution Operations
# ============================================================================


@router.post("/{workflow_id}/execute", response_model=WorkflowExecutionInDB, status_code=status.HTTP_202_ACCEPTED)
async def start_workflow_execution(
    workflow_id: int,
    execution_data: WorkflowExecutionCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Start executing a workflow in the background.

    The workflow will run asynchronously, chaining agents together
    and passing outputs between steps.
    """
    # Verify workflow exists and is accessible
    workflow = db.query(AgentWorkflow).filter(AgentWorkflow.id == workflow_id).first()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Check access
    if (
        workflow.created_by != current_user.id
        and not workflow.is_public
        and not workflow.is_template
    ):
        raise HTTPException(status_code=403, detail="Access denied")

    # Verify workflow is active
    if workflow.status != WorkflowStatus.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail=f"Workflow must be in 'active' status to execute (current: {workflow.status})"
        )

    # Create execution record
    execution = WorkflowExecution(
        workflow_id=workflow_id,
        user_id=current_user.id,
        status=WorkflowExecutionStatus.QUEUED,
        current_step_index=0,
        step_results=[],
        input_parameters=execution_data.input_parameters,
    )

    db.add(execution)
    db.commit()
    db.refresh(execution)

    # Start background execution
    background_tasks.add_task(
        execute_workflow,
        execution_id=execution.id,
        workflow_id=workflow_id,
        user_id=current_user.id,
    )

    return execution


@router.get("/executions/{execution_id}", response_model=WorkflowExecutionDetail)
async def get_execution_status(
    execution_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get detailed status of a workflow execution."""
    execution = (
        db.query(WorkflowExecution)
        .filter(WorkflowExecution.id == execution_id)
        .first()
    )

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    # Only owner can view
    if execution.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return execution


@router.get("/executions", response_model=List[WorkflowExecutionInDB])
async def list_executions(
    workflow_id: Optional[int] = None,
    status_filter: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List workflow executions for the current user."""
    query = db.query(WorkflowExecution).filter(
        WorkflowExecution.user_id == current_user.id
    )

    if workflow_id:
        query = query.filter(WorkflowExecution.workflow_id == workflow_id)

    if status_filter and status_filter.strip():
        try:
            status_enum = WorkflowExecutionStatus(status_filter)
            query = query.filter(WorkflowExecution.status == status_enum.value)
        except ValueError:
            pass  # Invalid status, ignore filter

    # Order by most recent first
    query = query.order_by(desc(WorkflowExecution.created_at))

    executions = query.offset(skip).limit(limit).all()
    return executions


@router.post("/executions/{execution_id}/cancel", response_model=WorkflowExecutionInDB)
async def cancel_execution(
    execution_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cancel a running workflow execution."""
    execution = (
        db.query(WorkflowExecution)
        .filter(WorkflowExecution.id == execution_id)
        .first()
    )

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    # Only owner can cancel
    if execution.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Can only cancel queued or running executions
    if execution.status not in [WorkflowExecutionStatus.QUEUED, WorkflowExecutionStatus.RUNNING]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel execution in '{execution.status}' status"
        )

    execution.status = WorkflowExecutionStatus.CANCELLED
    execution.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(execution)

    return execution


# ============================================================================
# Background Workflow Execution
# ============================================================================


async def execute_workflow(execution_id: int, workflow_id: int, user_id: int):
    """
    Execute a workflow in the background, orchestrating multiple agents.

    This function runs asynchronously and updates the execution record
    as it progresses through each step.
    """
    from database.session import SessionLocal

    db = SessionLocal()

    try:
        # Load execution and workflow
        execution = db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
        workflow = db.query(AgentWorkflow).filter(AgentWorkflow.id == workflow_id).first()

        if not execution or not workflow:
            return

        # Update status to running
        execution.status = WorkflowExecutionStatus.RUNNING
        execution.started_at = datetime.utcnow()
        db.commit()

        # Execute each step in sequence
        steps = workflow.steps
        step_results = []
        previous_output = None

        for step_index, step_config in enumerate(steps):
            # Update current step
            execution.current_step_index = step_index
            db.commit()

            try:
                # Prepare task description with parameter interpolation
                task_template = step_config.get("task_template", "")
                parameters = step_config.get("parameters", {})

                # Combine input parameters with step parameters
                all_params = {**(execution.input_parameters or {}), **parameters}

                # Add previous output if enabled
                if step_config.get("use_previous_output", True) and previous_output:
                    all_params["previous_output"] = previous_output

                # Interpolate task template
                try:
                    task_description = task_template.format(**all_params)
                except KeyError as e:
                    raise ValueError(f"Missing parameter in task template: {e}")

                # Invoke the agent for this step
                agent_type = step_config["agent_type"]

                # Call agent (this would normally call the Professor Framework agent)
                # For now, we'll simulate by calling the existing invoke_agent endpoint logic
                result = await invoke_agent_sync(
                    agent_type=agent_type,
                    task_description=task_description,
                    user_id=user_id,
                    db=db,
                )

                # Store step result
                step_result = {
                    "step_index": step_index,
                    "step_name": step_config.get("name", f"Step {step_index + 1}"),
                    "agent_type": agent_type,
                    "status": "completed",
                    "output": result.get("result", ""),
                    "completed_at": datetime.utcnow().isoformat(),
                }
                step_results.append(step_result)

                # Update previous output for next step
                previous_output = result.get("result", "")

            except Exception as step_error:
                # Handle step failure
                step_result = {
                    "step_index": step_index,
                    "step_name": step_config.get("name", f"Step {step_index + 1}"),
                    "agent_type": step_config["agent_type"],
                    "status": "failed",
                    "error": str(step_error),
                    "completed_at": datetime.utcnow().isoformat(),
                }
                step_results.append(step_result)

                # Check if step is required
                if step_config.get("required", True):
                    # Fail entire workflow
                    execution.status = WorkflowExecutionStatus.FAILED
                    execution.error_message = f"Step {step_index} failed: {str(step_error)}"
                    execution.failed_step_index = step_index
                    execution.step_results = step_results
                    execution.completed_at = datetime.utcnow()
                    db.commit()
                    return
                else:
                    # Continue to next step (non-required step)
                    continue

        # All steps completed successfully
        execution.status = WorkflowExecutionStatus.COMPLETED
        execution.step_results = step_results
        execution.final_output = previous_output  # Last step's output
        execution.completed_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        # Workflow-level failure
        execution.status = WorkflowExecutionStatus.FAILED
        execution.error_message = f"Workflow execution error: {str(e)}"
        execution.completed_at = datetime.utcnow()
        db.commit()

    finally:
        db.close()


async def invoke_agent_sync(
    agent_type: str,
    task_description: str,
    user_id: int,
    db: Session,
) -> dict:
    """
    Execute agent using real Claude API within workflow execution.

    Calls the AgentExecutor to invoke Claude AI for content generation.
    """
    from services.agent_executor import get_agent_executor

    try:
        # Get agent executor
        agent_executor = get_agent_executor()

        # Execute agent with real Claude API
        result = await agent_executor.execute_agent(
            agent_type=agent_type,
            task=task_description,
            parameters=None,  # Parameters already in task_description
            use_knowledge_base=True,
        )

        # Check if execution was successful
        if result["metadata"]["success"]:
            return {
                "task_id": f"task_{agent_type}_{datetime.utcnow().timestamp()}",
                "agent_type": agent_type,
                "status": "completed",
                "result": result["output"],
                "metadata": result["metadata"],
            }
        else:
            raise Exception(result["metadata"].get("error", "Agent execution failed"))

    except Exception as e:
        # Return error result
        return {
            "task_id": f"task_{agent_type}_{datetime.utcnow().timestamp()}",
            "agent_type": agent_type,
            "status": "failed",
            "result": None,
            "error": str(e),
        }
