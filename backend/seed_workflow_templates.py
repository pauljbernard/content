"""
Seed workflow templates into the database.

Pre-built workflows for common educational content development scenarios.
"""
from sqlalchemy.orm import Session
from database.session import SessionLocal, engine, Base

# Import all models to ensure relationships are resolved
from models.user import User
from models.agent import AgentJob
from models.content import Content
from models.workflow import AgentWorkflow, WorkflowExecution, WorkflowStatus

# Create tables
Base.metadata.create_all(bind=engine)


# Workflow templates
WORKFLOW_TEMPLATES = [
    {
        "name": "Complete Content Development",
        "description": "End-to-end content creation with pedagogical review and accessibility validation. Creates high-quality, standards-aligned instructional materials.",
        "steps": [
            {
                "agent_type": "content-developer",
                "name": "Generate Content",
                "description": "Create initial lesson content aligned to standards",
                "task_template": "Create a {subject} lesson for grade {grade_level} on the topic: {topic}. Align to {standards} standards.",
                "parameters": {},
                "use_previous_output": False,
                "required": True,
            },
            {
                "agent_type": "pedagogical-reviewer",
                "name": "Review Pedagogy",
                "description": "Review content for pedagogical soundness and constructive alignment",
                "task_template": "Review the following content for pedagogical soundness, constructive alignment, and learning science best practices: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
            {
                "agent_type": "accessibility-validator",
                "name": "Validate Accessibility",
                "description": "Check WCAG 2.1 AA compliance and UDL implementation",
                "task_template": "Validate WCAG 2.1 AA compliance and Universal Design for Learning (UDL) implementation for: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
        ],
        "tags": ["content-development", "quality-assurance", "accessibility"],
        "estimated_duration": "2-3 hours",
    },
    {
        "name": "Assessment Creation Pipeline",
        "description": "Comprehensive assessment development with quality assurance and standards validation. Creates valid, reliable assessment instruments.",
        "steps": [
            {
                "agent_type": "assessment-designer",
                "name": "Design Assessment",
                "description": "Create assessment blueprint and items",
                "task_template": "Design a {assessment_type} assessment for {subject} grade {grade_level} aligned to learning objectives: {objectives}",
                "parameters": {},
                "use_previous_output": False,
                "required": True,
            },
            {
                "agent_type": "quality-assurance",
                "name": "Quality Review",
                "description": "Comprehensive quality review across all pillars",
                "task_template": "Conduct comprehensive quality review of the following assessment: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
            {
                "agent_type": "standards-compliance",
                "name": "Validate Standards Alignment",
                "description": "Verify alignment to state and national standards",
                "task_template": "Validate standards alignment for {standards} standards: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
        ],
        "tags": ["assessment", "quality-assurance", "standards"],
        "estimated_duration": "2-4 hours",
    },
    {
        "name": "Full Quality Review",
        "description": "Multi-dimensional quality review covering pedagogy, accessibility, bias detection, and standards compliance. Ensures content meets all quality standards.",
        "steps": [
            {
                "agent_type": "pedagogical-reviewer",
                "name": "Pedagogical Review",
                "description": "Review pedagogical soundness",
                "task_template": "Review the following content for pedagogical soundness: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
            {
                "agent_type": "accessibility-validator",
                "name": "Accessibility Check",
                "description": "Validate WCAG compliance and UDL",
                "task_template": "Check WCAG 2.1 AA compliance and UDL implementation: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
            {
                "agent_type": "quality-assurance",
                "name": "Bias Detection",
                "description": "Detect and eliminate bias using CEID framework",
                "task_template": "Detect and report any bias using the CEID 11-category framework: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
            {
                "agent_type": "standards-compliance",
                "name": "Standards Validation",
                "description": "Verify standards alignment",
                "task_template": "Validate alignment to {standards} standards: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
        ],
        "tags": ["quality-assurance", "accessibility", "bias-detection", "standards"],
        "estimated_duration": "3-4 hours",
    },
    {
        "name": "Curriculum Architecture",
        "description": "Complete curriculum design from research to content development. Creates comprehensive curriculum structures with scope and sequence.",
        "steps": [
            {
                "agent_type": "curriculum-architect",
                "name": "Curriculum Research",
                "description": "Research standards and design curriculum structure",
                "task_template": "Research {subject} for grade {grade_level} aligned to {standards} standards and design curriculum scope and sequence",
                "parameters": {},
                "use_previous_output": False,
                "required": True,
            },
            {
                "agent_type": "instructional-designer",
                "name": "Instructional Design",
                "description": "Design learning experiences and activities",
                "task_template": "Design learning experiences, activities, and instructional strategies for: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
            {
                "agent_type": "assessment-designer",
                "name": "Assessment Blueprint",
                "description": "Create assessment blueprint aligned to objectives",
                "task_template": "Create assessment blueprint with item types, cognitive levels, and rubrics for: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
        ],
        "tags": ["curriculum-design", "instructional-design", "assessment"],
        "estimated_duration": "4-6 hours",
    },
    {
        "name": "Adaptive Learning Development",
        "description": "Create adaptive learning content with personalized pathways and analytics. Develops differentiated instruction based on learner needs.",
        "steps": [
            {
                "agent_type": "content-developer",
                "name": "Create Base Content",
                "description": "Develop foundational learning content",
                "task_template": "Create {subject} content for grade {grade_level} on topic: {topic}",
                "parameters": {},
                "use_previous_output": False,
                "required": True,
            },
            {
                "agent_type": "adaptive-learning",
                "name": "Design Adaptive Pathways",
                "description": "Create personalized learning pathways",
                "task_template": "Design adaptive learning pathways with differentiation strategies for: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
            {
                "agent_type": "learning-analytics",
                "name": "Analytics Integration",
                "description": "Define learning analytics and success metrics",
                "task_template": "Define learning analytics, performance metrics, and success indicators for: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
        ],
        "tags": ["adaptive-learning", "personalization", "analytics"],
        "estimated_duration": "3-5 hours",
    },
    {
        "name": "SCORM Package Production",
        "description": "Package content for LMS deployment with SCORM validation. Creates LMS-ready learning objects with proper metadata and sequencing.",
        "steps": [
            {
                "agent_type": "content-developer",
                "name": "Prepare Content",
                "description": "Finalize content for packaging",
                "task_template": "Prepare and finalize content for SCORM packaging: {content_description}",
                "parameters": {},
                "use_previous_output": False,
                "required": True,
            },
            {
                "agent_type": "scorm-validator",
                "name": "SCORM Packaging",
                "description": "Package as SCORM 1.2 or 2004",
                "task_template": "Package the following content as SCORM {scorm_version} with proper manifest and sequencing: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
            {
                "agent_type": "quality-assurance",
                "name": "LMS Testing",
                "description": "Test in target LMS environment",
                "task_template": "Validate SCORM package for {lms_platform} compatibility and grade passback: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
        ],
        "tags": ["scorm", "lms", "packaging"],
        "estimated_duration": "1-2 hours",
    },
    {
        "name": "Localization Pipeline",
        "description": "Translate and culturally adapt content for international markets. Maintains pedagogical quality across languages.",
        "steps": [
            {
                "agent_type": "content-developer",
                "name": "Source Content",
                "description": "Prepare source content for localization",
                "task_template": "Prepare {subject} content for grade {grade_level} for localization to {target_language}: {topic}",
                "parameters": {},
                "use_previous_output": False,
                "required": True,
            },
            {
                "agent_type": "localization",
                "name": "Translation & Cultural Adaptation",
                "description": "Translate and adapt for target culture",
                "task_template": "Translate and culturally adapt to {target_language} and {target_culture}: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
            {
                "agent_type": "quality-assurance",
                "name": "Quality Review",
                "description": "Validate translation quality and cultural appropriateness",
                "task_template": "Review translation quality, cultural appropriateness, and pedagogical equivalence: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
        ],
        "tags": ["localization", "translation", "internationalization"],
        "estimated_duration": "3-4 hours",
    },
    {
        "name": "Corporate Training Development",
        "description": "Create professional learning content for workplace training. Includes performance assessment and business impact measurement.",
        "steps": [
            {
                "agent_type": "corporate-training",
                "name": "Training Design",
                "description": "Design corporate training program",
                "task_template": "Design corporate training program for: {training_topic} targeting {audience} with learning objectives: {objectives}",
                "parameters": {},
                "use_previous_output": False,
                "required": True,
            },
            {
                "agent_type": "assessment-designer",
                "name": "Performance Assessment",
                "description": "Create performance-based assessments",
                "task_template": "Design performance-based assessments and real-world application scenarios for: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
            {
                "agent_type": "learning-analytics",
                "name": "Impact Measurement",
                "description": "Define business impact metrics",
                "task_template": "Define training impact metrics, ROI measurement, and business outcomes for: {previous_output}",
                "parameters": {},
                "use_previous_output": True,
                "required": True,
            },
        ],
        "tags": ["corporate-training", "professional-learning", "assessment"],
        "estimated_duration": "3-5 hours",
    },
]


def seed_templates(db: Session):
    """Seed workflow templates into the database."""

    # Get admin user (from init_db.py) or any superuser
    admin_user = db.query(User).filter(
        (User.email == "admin@nova.ai") | (User.is_superuser == True)
    ).first()

    if not admin_user:
        print("No admin user found. Workflow templates require an admin/superuser.")
        print("Please run init_db.py first to create the admin user.")
        return

    print(f"Using admin user: {admin_user.email} (ID: {admin_user.id})")

    # Check for existing templates
    existing_templates = db.query(AgentWorkflow).filter(
        AgentWorkflow.is_template == True
    ).all()

    if existing_templates:
        print(f"\nFound {len(existing_templates)} existing templates.")
        response = input("Delete existing templates and recreate? (y/n): ")
        if response.lower() == 'y':
            for template in existing_templates:
                db.delete(template)
            db.commit()
            print("Deleted existing templates.")

    # Create templates
    print(f"\nCreating {len(WORKFLOW_TEMPLATES)} workflow templates...")

    for template_data in WORKFLOW_TEMPLATES:
        workflow = AgentWorkflow(
            name=template_data["name"],
            description=template_data["description"],
            created_by=admin_user.id,
            is_template=True,  # Mark as template
            is_public=True,    # Make publicly accessible
            status=WorkflowStatus.ACTIVE,  # Templates are active
            steps=template_data["steps"],
            tags=template_data["tags"],
            estimated_duration=template_data.get("estimated_duration"),
        )

        db.add(workflow)
        print(f"  ✓ Created: {template_data['name']}")

    db.commit()
    print(f"\n✅ Successfully created {len(WORKFLOW_TEMPLATES)} workflow templates!")

    # Print summary
    print("\n" + "="*60)
    print("WORKFLOW TEMPLATES SUMMARY")
    print("="*60)
    for i, template in enumerate(WORKFLOW_TEMPLATES, 1):
        print(f"\n{i}. {template['name']}")
        print(f"   Description: {template['description']}")
        print(f"   Steps: {len(template['steps'])}")
        print(f"   Tags: {', '.join(template['tags'])}")
        print(f"   Duration: {template.get('estimated_duration', 'N/A')}")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_templates(db)
    finally:
        db.close()
