"""
Agent Execution Service

This service orchestrates AI-powered content generation by:
1. Retrieving context using ContextRetriever
2. Assembling prompts from templates
3. Calling Anthropic Claude API for generation
4. Validating and returning results
"""

import logging
import json
from typing import Dict, Any, Optional, List
from anthropic import Anthropic
from sqlalchemy.orm import Session

from core.config import settings
from services.context_retrieval import ContextRetriever
from models.content_type import ContentInstanceModel, ContentTypeModel
from utils.validation import validate_instance_data

logger = logging.getLogger(__name__)

# Initialize Anthropic client
if not settings.ANTHROPIC_API_KEY:
    logger.warning("ANTHROPIC_API_KEY not set - agent execution will fail")

anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None


class AgentExecutor:
    """Executes AI agents for content generation."""

    def __init__(self, db: Session):
        self.db = db
        self.context_retriever = ContextRetriever(db)

    def load_agent_config(self, agent_config_id: str) -> Dict[str, Any]:
        """
        Load agent configuration from content instance.

        Args:
            agent_config_id: ID of the Agent Configuration content instance

        Returns:
            Agent configuration data
        """
        instance = self.db.query(ContentInstanceModel).filter(
            ContentInstanceModel.id == agent_config_id,
            ContentInstanceModel.status == "published"
        ).first()

        if not instance:
            raise ValueError(f"Agent configuration not found: {agent_config_id}")

        return instance.data

    def check_dependencies(
        self,
        agent_config: Dict[str, Any],
        current_data: Dict[str, Any]
    ) -> tuple[bool, List[str]]:
        """
        Check if all dependencies are met for agent execution.

        Args:
            agent_config: Agent configuration
            current_data: Current content instance data

        Returns:
            Tuple of (dependencies_met, missing_fields)
        """
        missing_fields = []

        # Check required user inputs
        required_inputs = agent_config.get("required_user_inputs", [])
        for field in required_inputs:
            if field not in current_data or not current_data[field]:
                missing_fields.append(field)

        # Check field dependencies
        field_deps = agent_config.get("field_dependencies", [])
        for field in field_deps:
            if field not in current_data or not current_data[field]:
                missing_fields.append(field)

        return len(missing_fields) == 0, missing_fields

    def format_current_data(self, current_data: Dict[str, Any]) -> str:
        """Format current data for display in prompt."""
        sections = []
        for key, value in current_data.items():
            if value is not None and value != "":
                sections.append(f"**{key}**: {json.dumps(value) if isinstance(value, (dict, list)) else value}")
        return "\n".join(sections) if sections else "(No data provided yet)"

    def assemble_prompt(
        self,
        prompt_template: str,
        context: Dict[str, Any],
        user_inputs: Dict[str, Any],
        examples: Optional[List[Dict[str, Any]]] = None,
        custom_prompt: Optional[str] = None
    ) -> str:
        """
        Assemble the final prompt from template, context, and examples.

        Args:
            prompt_template: Template string with {placeholders}
            context: Retrieved context
            user_inputs: User-provided inputs
            examples: Few-shot examples
            custom_prompt: User-defined custom instructions for this specific field

        Returns:
            Complete prompt string
        """
        # Format context as string
        context_str = self.context_retriever.format_context_for_prompt(context)

        # Format current data
        current_data_formatted = self.format_current_data(user_inputs)

        # Start with the template
        prompt = prompt_template

        # Replace placeholders
        prompt = prompt.replace("{context}", context_str)
        prompt = prompt.replace("{current_data_formatted}", current_data_formatted)

        # Replace user input placeholders
        for key, value in user_inputs.items():
            placeholder = f"{{{key}}}"
            prompt = prompt.replace(placeholder, str(value))

        # Add few-shot examples if provided
        if examples:
            examples_section = "\n\n## Examples\n\n"
            for i, example in enumerate(examples, 1):
                examples_section += f"### Example {i}\n"
                examples_section += f"**Input:** {example.get('input', '')}\n"
                examples_section += f"**Output:** {example.get('output', '')}\n\n"
            prompt = examples_section + prompt

        # Add custom prompt instructions if provided
        if custom_prompt and custom_prompt.strip():
            prompt += "\n\n## Additional Field-Specific Instructions\n\n"
            prompt += custom_prompt.strip()
            prompt += "\n"

        return prompt

    def get_builtin_agent_config(
        self,
        agent_name: str,
        field_name: str,
        content_type_id: str
    ) -> Dict[str, Any]:
        """
        Get configuration for a built-in agent by name.

        Built-in agents are specialized Claude Code agents with optimized
        prompts and retrieval strategies for specific tasks.
        """
        # Get content type to understand context
        content_type = self.db.query(ContentTypeModel).filter(
            ContentTypeModel.id == content_type_id
        ).first()
        content_type_name = content_type.name if content_type else "content"

        # Extract RAG content types and custom prompt from attribute configuration
        rag_content_types = []
        custom_prompt = None
        if content_type and content_type.attributes:
            for attr in content_type.attributes:
                if attr.get("name") == field_name:
                    rag_content_types = attr.get("ai_rag_content_types", [])
                    custom_prompt = attr.get("ai_custom_prompt")
                    break

        # Define built-in agent configurations
        builtin_agents = {
            "curriculum-architect": {
                "agent_name": "Curriculum Architect",
                "retrieval_config": {
                    "content_types": rag_content_types,  # Use user-configured RAG content types
                    "knowledge_base_paths": [
                        "/universal/frameworks/",
                        "/subjects/{subject}/common/",
                        "/districts/{state}/"
                    ],
                    "use_kb_vector_search": True,  # Enable KB vector search
                    "filters": {}
                },
                "prompt_template": f"""You are Claude Code acting as a Curriculum Architect, specializing in educational curriculum design and standards alignment.

{{context}}

## Task

Design high-quality curriculum content for the "{field_name}" field in a {content_type_name}.

## Current Data

{{current_data_formatted}}

## Your Expertise

As a Curriculum Architect, you excel at:
- Aligning content to educational standards (CCSS, NGSS, state standards)
- Designing learning progressions and scope & sequence
- Ensuring vertical and horizontal alignment
- Applying research-based instructional frameworks (UDL, Understanding by Design)
- Creating standards-aligned learning objectives using Bloom's Taxonomy

## Output

Provide curriculum content that is standards-aligned, pedagogically sound, and ready for implementation.""",
                "temperature": 0.7
            },
            "lesson-planner": {
                "agent_name": "Lesson Planner",
                "retrieval_config": {
                    "content_types": rag_content_types,  # Use user-configured RAG content types
                    "knowledge_base_paths": [
                        "/universal/frameworks/",
                        "/subjects/{subject}/common/",
                        "/universal/frameworks/eb-scaffolding-guide.md"
                    ],
                    "filters": {}
                },
                "prompt_template": f"""You are Claude Code acting as a Lesson Planner, specializing in creating engaging, effective lesson plans.

{{context}}

## Task

Create lesson content for the "{field_name}" field in a {content_type_name}.

## Current Data

{{current_data_formatted}}

## Your Expertise

As a Lesson Planner, you excel at:
- Designing engaging learning activities with clear objectives
- Sequencing instruction from engagement to assessment
- Incorporating formative assessment opportunities
- Providing scaffolding for diverse learners (UDL, ELL supports)
- Applying subject-specific instructional routines (MLRs, literacy routines)

## Output

Provide detailed, actionable lesson content ready for classroom implementation.""",
                "temperature": 0.8
            },
            "assessment-designer": {
                "agent_name": "Assessment Designer",
                "retrieval_config": {
                    "content_types": rag_content_types,  # Use user-configured RAG content types
                    "knowledge_base_paths": [
                        "/universal/assessment/",
                        "/subjects/{subject}/common/",
                        "/universal/frameworks/dok-framework-guide.md"
                    ],
                    "use_kb_vector_search": True,  # Enable KB vector search
                    "filters": {}
                },
                "prompt_template": f"""You are Claude Code acting as an Assessment Designer, specializing in creating valid, reliable assessments.

{{context}}

## Task

Design assessment content for the "{field_name}" field in a {content_type_name}.

## Current Data

{{current_data_formatted}}

## Your Expertise

As an Assessment Designer, you excel at:
- Creating assessment items aligned to learning objectives
- Applying Webb's Depth of Knowledge (DOK) framework
- Designing multiple item types (MC, CR, performance tasks)
- Writing clear, unbiased items and rubrics
- Ensuring accessibility and fairness

## Output

Provide assessment content that is valid, reliable, and aligned to objectives.""",
                "temperature": 0.6
            },
            "content-developer": {
                "agent_name": "Content Developer",
                "retrieval_config": {
                    "content_types": rag_content_types,  # Use user-configured RAG content types
                    "knowledge_base_paths": [
                        "/universal/frameworks/",
                        "/subjects/{subject}/common/"
                    ],
                    "use_kb_vector_search": True,  # Enable KB vector search
                    "filters": {}
                },
                "prompt_template": f"""You are Claude Code acting as a Content Developer, specializing in creating high-quality educational content.

{{context}}

## Task

Develop content for the "{field_name}" field in a {content_type_name}.

## Current Data

{{current_data_formatted}}

## Your Expertise

As a Content Developer, you excel at:
- Writing clear, engaging instructional content
- Adapting content for diverse learners
- Incorporating multimedia and interactive elements
- Ensuring pedagogical soundness and accuracy
- Following style guides and content standards

## Output

Provide well-structured, engaging content ready for publication.""",
                "temperature": 0.7
            },
            "pedagogical-reviewer": {
                "agent_name": "Pedagogical Reviewer",
                "retrieval_config": {
                    "content_types": rag_content_types,  # Use user-configured RAG content types
                    "knowledge_base_paths": [
                        "/universal/frameworks/"
                    ],
                    "filters": {}
                },
                "prompt_template": f"""You are Claude Code acting as a Pedagogical Reviewer, specializing in evaluating instructional design quality.

{{context}}

## Task

Review and improve the "{field_name}" field content in a {content_type_name}.

## Current Data

{{current_data_formatted}}

## Your Expertise

As a Pedagogical Reviewer, you excel at:
- Evaluating constructive alignment between objectives, activities, and assessments
- Ensuring research-based instructional strategies
- Identifying gaps in scaffolding and differentiation
- Verifying UDL principles and accessibility
- Assessing cognitive load and learning progressions

## Output

Provide improved content with pedagogical enhancements and justification.""",
                "temperature": 0.7
            },
            "accessibility-reviewer": {
                "agent_name": "Accessibility Reviewer",
                "retrieval_config": {
                    "content_types": rag_content_types,  # Use user-configured RAG content types
                    "knowledge_base_paths": [
                        "/universal/frameworks/udl-principles-guide.md"
                    ],
                    "filters": {}
                },
                "prompt_template": f"""You are Claude Code acting as an Accessibility Reviewer, specializing in WCAG compliance and UDL.

{{context}}

## Task

Review and enhance accessibility for the "{field_name}" field in a {content_type_name}.

## Current Data

{{current_data_formatted}}

## Your Expertise

As an Accessibility Reviewer, you excel at:
- Ensuring WCAG 2.1 AA compliance
- Implementing Universal Design for Learning (UDL) principles
- Providing alternative representations for diverse learners
- Ensuring screen reader compatibility
- Creating accessible multimedia and interactive elements

## Output

Provide accessibility-enhanced content meeting all compliance standards.""",
                "temperature": 0.6
            }
        }

        # Get the built-in agent config or use a generic default
        agent_config = builtin_agents.get(agent_name, {
            "agent_name": agent_name.replace("-", " ").title(),
            "retrieval_config": {
                "content_types": rag_content_types,  # Use user-configured RAG content types
                "knowledge_base_paths": ["/universal/frameworks/"],
                "filters": {}
            },
            "prompt_template": f"""You are Claude Code with specialized agent: {agent_name}.

{{context}}

## Task

Generate content for the "{field_name}" field in a {content_type_name}.

## Current Data

{{current_data_formatted}}

## Output

Provide high-quality content appropriate for this field.""",
            "temperature": 0.7
        })

        return {
            "agent_id": agent_name,
            "agent_name": agent_config["agent_name"],
            "target_fields": [field_name],
            "retrieval_config": agent_config["retrieval_config"],
            "prompt_template": agent_config["prompt_template"],
            "custom_prompt": custom_prompt,  # User-defined custom instructions for this field
            "required_user_inputs": [],
            "field_dependencies": [],
            "model_config": {
                "model": "claude-sonnet-4-5",
                "temperature": agent_config.get("temperature", 0.7),
                "max_tokens": 4096
            },
            "examples": None
        }

    async def execute_agent(
        self,
        field_name: str,
        current_data: Dict[str, Any],
        content_type_id: str,
        agent_config_id: str = None
    ) -> Dict[str, Any]:
        """
        Execute an agent to generate content for a specific field.

        Args:
            field_name: Name of the field to populate
            current_data: Current content instance data (user inputs + existing fields)
            content_type_id: ID of the content type being edited
            agent_config_id: Optional ID of the agent configuration to use (uses default if None)

        Returns:
            Result dictionary containing:
                - generated_value: The AI-generated content
                - confidence: Confidence score (0-1)
                - context_used: Metadata about retrieved context
                - prompt: The actual prompt sent to the LLM (for debugging)
        """
        if not anthropic_client:
            raise ValueError("Anthropic API key not configured")

        # 1. Load agent configuration
        if agent_config_id:
            # Check if it's a UUID (content instance ID) or a built-in agent name
            try:
                # Try to parse as UUID - if successful, it's a content instance ID
                import uuid
                uuid.UUID(agent_config_id)
                # It's a valid UUID, load from database
                agent_config = self.load_agent_config(agent_config_id)
            except (ValueError, AttributeError):
                # Not a UUID, treat as built-in agent name
                agent_config = self.get_builtin_agent_config(agent_config_id, field_name, content_type_id)
        else:
            # No agent specified, use generic default
            agent_config = self.get_builtin_agent_config("default", field_name, content_type_id)

        # 2. Check dependencies
        deps_met, missing = self.check_dependencies(agent_config, current_data)
        if not deps_met:
            logger.error(f"Dependencies not met for field '{field_name}': missing {missing}")
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        # 3. Verify this agent can populate this field
        target_fields = agent_config.get("target_fields", [])
        logger.info(f"Agent '{agent_config.get('agent_name')}' target fields: {target_fields}, requested field: {field_name}")
        if field_name not in target_fields:
            logger.error(f"Field '{field_name}' not in target fields {target_fields}")
            raise ValueError(f"Agent '{agent_config['agent_name']}' cannot populate field '{field_name}'")

        # 4. Retrieve context
        retrieval_config = agent_config.get("retrieval_config", {})
        context = await self.context_retriever.assemble_context(
            retrieval_config=retrieval_config,
            user_inputs=current_data
        )

        # 5. Assemble prompt
        prompt_template = agent_config.get("prompt_template", "")
        examples = agent_config.get("examples")
        custom_prompt = agent_config.get("custom_prompt")
        full_prompt = self.assemble_prompt(
            prompt_template=prompt_template,
            context=context,
            user_inputs=current_data,
            examples=examples,
            custom_prompt=custom_prompt
        )

        # 6. Get model configuration
        model_config = agent_config.get("model_config", {})
        model = model_config.get("model", "claude-sonnet-4-5")
        temperature = model_config.get("temperature", 0.7)
        max_tokens = model_config.get("max_tokens", 4096)

        # 7. Call Claude API
        try:
            logger.info(f"Calling Claude API for field '{field_name}' with agent '{agent_config['agent_id']}'")

            message = anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ]
            )

            # Extract generated content
            generated_text = message.content[0].text

            # Try to parse as JSON if the field expects JSON
            # (You could enhance this by checking the content type schema)
            generated_value = generated_text
            try:
                # Attempt to parse as JSON
                generated_value = json.loads(generated_text)
            except json.JSONDecodeError:
                # Not JSON, keep as string
                pass

            # Calculate a simple confidence score based on response metadata
            # In production, you might use Claude's confidence indicators or other heuristics
            confidence = 0.85  # Placeholder

            return {
                "field_name": field_name,
                "generated_value": generated_value,
                "confidence": confidence,
                "context_used": {
                    "total_instances": context["metadata"]["total_instances"],
                    "total_knowledge_files": context["metadata"]["total_knowledge_files"],
                    "retrieval_config": retrieval_config,
                },
                "prompt": full_prompt,  # For debugging/transparency
                "model": model,
                "usage": {
                    "input_tokens": message.usage.input_tokens,
                    "output_tokens": message.usage.output_tokens,
                }
            }

        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            raise ValueError(f"Agent execution failed: {str(e)}")

    async def execute_agent_stream(
        self,
        field_name: str,
        current_data: Dict[str, Any],
        content_type_id: str,
        agent_config_id: str = None
    ):
        """
        Execute agent with streaming response.

        Yields Server-Sent Events (SSE) with:
        - Incremental text chunks as they're generated
        - Final metadata when complete
        """
        if not anthropic_client:
            yield f"data: {json.dumps({'error': 'Anthropic API key not configured'})}\n\n"
            return

        # 1. Load agent configuration (same as non-streaming)
        if agent_config_id:
            try:
                import uuid
                uuid.UUID(agent_config_id)
                agent_config = self.load_agent_config(agent_config_id)
            except (ValueError, AttributeError):
                agent_config = self.get_builtin_agent_config(agent_config_id, field_name, content_type_id)
        else:
            agent_config = self.get_builtin_agent_config("default", field_name, content_type_id)

        # 2. Check dependencies
        deps_met, missing = self.check_dependencies(agent_config, current_data)
        if not deps_met:
            error_msg = f"Missing required fields: {', '.join(missing)}"
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
            return

        # 3. Verify agent can populate this field
        target_fields = agent_config.get("target_fields", [])
        if field_name not in target_fields:
            error_msg = f"Agent cannot populate field '{field_name}'"
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
            return

        # 4. Retrieve context
        retrieval_config = agent_config.get("retrieval_config", {})
        context = await self.context_retriever.assemble_context(
            retrieval_config=retrieval_config,
            user_inputs=current_data
        )

        # 5. Assemble prompt
        prompt_template = agent_config.get("prompt_template", "")
        examples = agent_config.get("examples")
        custom_prompt = agent_config.get("custom_prompt")
        full_prompt = self.assemble_prompt(
            prompt_template=prompt_template,
            context=context,
            user_inputs=current_data,
            examples=examples,
            custom_prompt=custom_prompt
        )

        # 6. Get model configuration
        model_config = agent_config.get("model_config", {})
        model = model_config.get("model", "claude-sonnet-4-5")
        temperature = model_config.get("temperature", 0.7)
        max_tokens = model_config.get("max_tokens", 4096)

        # 7. Stream from Claude API with retry logic
        max_retries = 3
        retry_delay = 1  # seconds

        try:
            for attempt in range(max_retries):
                try:
                    logger.info(f"Starting streaming generation for field '{field_name}' with agent '{agent_config.get('agent_id', 'unknown')}' (attempt {attempt + 1}/{max_retries})")
                    logger.info(f"Agent config: {agent_config.get('agent_name')}, Target fields: {agent_config.get('target_fields')}")

                    # Send metadata first (only on first attempt)
                    if attempt == 0:
                        start_data = {'type': 'start', 'field_name': field_name, 'agent': agent_config.get('agent_name', 'Unknown')}
                        logger.info(f"Sending start event: {start_data}")
                        yield f"data: {json.dumps(start_data)}\n\n"

                    accumulated_text = ""
                    input_tokens = 0
                    output_tokens = 0

                    import asyncio

                    with anthropic_client.messages.stream(
                        model=model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        messages=[{"role": "user", "content": full_prompt}]
                    ) as stream:
                        chunk_count = 0
                        for text in stream.text_stream:
                            accumulated_text += text
                            chunk_count += 1
                            # Send each chunk
                            chunk_data = {'type': 'content', 'text': text}
                            logger.debug(f"Sending chunk {chunk_count}: {len(text)} chars")
                            yield f"data: {json.dumps(chunk_data)}\n\n"
                            # Give control back to event loop to flush immediately
                            await asyncio.sleep(0)

                        logger.info(f"Streamed {chunk_count} chunks, total {len(accumulated_text)} chars")

                        # Get final message for usage stats
                        final_message = stream.get_final_message()
                        input_tokens = final_message.usage.input_tokens
                        output_tokens = final_message.usage.output_tokens

                    # Success - break out of retry loop
                    break

                except Exception as retry_error:
                    # Check if it's an overloaded error
                    error_str = str(retry_error)
                    is_overloaded = 'overloaded' in error_str.lower() or (hasattr(retry_error, 'status_code') and retry_error.status_code == 529)

                    if is_overloaded and attempt < max_retries - 1:
                        # Wait and retry
                        import asyncio
                        wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(f"API overloaded, retrying in {wait_time}s...")
                        yield f"data: {json.dumps({'type': 'info', 'message': f'API busy, retrying in {wait_time}s...'})}\n\n"
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        # Not overloaded or max retries reached, propagate error
                        raise retry_error

            # After successful streaming, send completion metadata
            # Try to parse as JSON
            generated_value = accumulated_text
            try:
                generated_value = json.loads(accumulated_text)
            except json.JSONDecodeError:
                pass

            # Send completion metadata
            completion_data = {
                "type": "done",
                "field_name": field_name,
                "generated_value": generated_value,
                "confidence": 0.85,
                "context_metadata": {
                    "total_instances": context["metadata"]["total_instances"],
                    "total_knowledge_files": context["metadata"]["total_knowledge_files"],
                },
                "model": model,
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                }
            }
            logger.info(f"Sending done event with {len(str(generated_value))} chars")
            yield f"data: {json.dumps(completion_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in streaming generation: {e}")

            # Handle Anthropic API errors specially
            error_message = str(e)
            if hasattr(e, 'status_code'):
                # Anthropic API error
                if hasattr(e, 'message'):
                    error_message = e.message
                elif hasattr(e, 'body'):
                    error_body = e.body if isinstance(e.body, dict) else {}
                    error_message = error_body.get('error', {}).get('message', str(e))

            error_data = {
                'type': 'error',
                'error': error_message
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    async def execute_auto_populate(
        self,
        content_type_id: str,
        current_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute all auto-populate agents for a content instance.

        This finds all active agents configured for this content type with
        trigger_mode="auto_populate" and executes them.

        Args:
            content_type_id: Content type being edited
            current_data: Current instance data

        Returns:
            Dictionary mapping field names to generated values
        """
        # Query for active agent configurations targeting this content type
        # with auto_populate trigger mode
        # This would require querying the Agent Configuration content instances
        # For now, return empty dict as a placeholder

        # TODO: Implement auto-populate logic
        return {}


def get_agent_executor(db: Session) -> AgentExecutor:
    """Factory function to create an agent executor."""
    return AgentExecutor(db)
