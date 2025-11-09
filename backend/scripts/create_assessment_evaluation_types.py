"""
Create assessment and evaluation content types: Assessment, QuestionItem, and Rubric
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.session import SessionLocal
from models.content_type import ContentTypeModel
import uuid


def create_assessment_content_type(db: Session):
    """
    Create Assessment content type.

    Assessment: Summative or formative evaluation aligned to standards.
    Used for measuring student learning and progress.
    """
    print("   Creating Assessment content type...")

    assessment_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="Assessment",
        description="Summative or formative evaluation tool aligned to standards. Measures student knowledge, skills, and understanding through various question types and performance tasks.",
        icon="ClipboardDocumentCheckIcon",
        is_system=True,
        attributes=[
            {
                "name": "title",
                "label": "Assessment Title",
                "type": "text",
                "required": True,
                "config": {
                    "minLength": 5,
                    "maxLength": 300
                },
                "help_text": "Clear, descriptive title. Example: 'Unit 3 Fractions Quiz', 'Ecosystem Performance Task', 'Mid-Year Reading Assessment'",
                "order_index": 0
            },
            {
                "name": "description",
                "label": "Description",
                "type": "rich_text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Overview of the assessment purpose, content, and format",
                "order_index": 1
            },
            {
                "name": "assessment_type",
                "label": "Assessment Type",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": [
                        "Formative - Exit Ticket",
                        "Formative - Quiz",
                        "Formative - Observation Checklist",
                        "Formative - Self-Assessment",
                        "Formative - Peer Assessment",
                        "Summative - Unit Test",
                        "Summative - End-of-Course Exam",
                        "Summative - Performance Task",
                        "Summative - Project",
                        "Summative - Portfolio",
                        "Diagnostic - Pre-Assessment",
                        "Diagnostic - Benchmark",
                        "Interim/Benchmark"
                    ]
                },
                "help_text": "Type of assessment and its purpose in the learning cycle",
                "order_index": 2
            },
            {
                "name": "grade",
                "label": "Grade Level",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": ["Pre-K", "K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
                },
                "help_text": "Target grade level for this assessment",
                "order_index": 3
            },
            {
                "name": "subject",
                "label": "Subject Area",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": [
                        "Mathematics",
                        "English Language Arts",
                        "Science",
                        "Social Studies",
                        "Computer Science",
                        "World Languages",
                        "Fine Arts",
                        "Music",
                        "Physical Education & Health"
                    ]
                },
                "help_text": "Primary subject area",
                "order_index": 4
            },
            {
                "name": "linked_standards",
                "label": "Linked Standards",
                "type": "reference",
                "required": True,
                "config": {
                    "contentType": "Standard",
                    "multiple": True
                },
                "help_text": "Standards this assessment measures (at least one required)",
                "order_index": 5
            },
            {
                "name": "linked_concepts",
                "label": "Linked Concepts",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Concept",
                    "multiple": True
                },
                "help_text": "Concepts assessed in this evaluation",
                "order_index": 6
            },
            {
                "name": "linked_learning_targets",
                "label": "Linked Learning Targets",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Learning Target",
                    "multiple": True
                },
                "help_text": "Learning targets this assessment measures",
                "order_index": 7
            },
            {
                "name": "question_items",
                "label": "Question Items",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "QuestionItem",
                    "multiple": True
                },
                "help_text": "Individual questions/tasks that comprise this assessment",
                "order_index": 8
            },
            {
                "name": "rubric",
                "label": "Scoring Rubric",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Rubric",
                    "multiple": False
                },
                "help_text": "Rubric for scoring open-ended responses or performance tasks",
                "order_index": 9
            },
            {
                "name": "difficulty",
                "label": "Difficulty Level",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": ["Below Grade Level", "On Grade Level", "Above Grade Level", "Mixed"]
                },
                "help_text": "Overall difficulty relative to grade level expectations",
                "order_index": 10
            },
            {
                "name": "depth_of_knowledge",
                "label": "Depth of Knowledge (DOK)",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["DOK 1 - Recall", "DOK 2 - Skill/Concept", "DOK 3 - Strategic Thinking", "DOK 4 - Extended Thinking", "Mixed DOK Levels"]
                },
                "help_text": "Primary Webb's DOK level for the assessment",
                "order_index": 11
            },
            {
                "name": "blooms_taxonomy",
                "label": "Bloom's Taxonomy Level",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create", "Mixed Levels"]
                },
                "help_text": "Primary cognitive level",
                "order_index": 12
            },
            {
                "name": "total_points",
                "label": "Total Points",
                "type": "number",
                "required": False,
                "config": {
                    "min": 1,
                    "max": 1000
                },
                "help_text": "Total possible points for the assessment",
                "order_index": 13
            },
            {
                "name": "time_limit",
                "label": "Time Limit (minutes)",
                "type": "number",
                "required": False,
                "config": {
                    "min": 1,
                    "max": 300
                },
                "help_text": "Recommended or required time limit in minutes",
                "order_index": 14
            },
            {
                "name": "scoring_guide",
                "label": "Scoring Guide",
                "type": "rich_text",
                "required": False,
                "config": {
                    "maxLength": 3000
                },
                "help_text": "Detailed instructions for scoring the assessment, including point allocation and answer keys",
                "order_index": 15
            },
            {
                "name": "answer_key",
                "label": "Answer Key",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Answer key for selected-response items. Format: [{\"item\": 1, \"answer\": \"B\", \"points\": 1}, ...]. Use QuestionItem references for detailed items.",
                "default_value": [],
                "order_index": 16
            },
            {
                "name": "accommodations",
                "label": "Accommodations",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
                    "choices": [
                        "Extended Time (1.5x)",
                        "Extended Time (2x)",
                        "Read Aloud",
                        "Scribe",
                        "Reduced Distractions",
                        "Breaks as Needed",
                        "Calculator",
                        "Simplified Language",
                        "Visual Supports",
                        "Translation/Bilingual Dictionary"
                    ]
                },
                "help_text": "Available accommodations for students with IEPs or 504 plans",
                "order_index": 17
            },
            {
                "name": "ell_supports",
                "label": "ELL Supports",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Specific supports for English language learners",
                "order_index": 18
            },
            {
                "name": "prerequisite_skills",
                "label": "Prerequisite Skills",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Skills students should have before taking this assessment",
                "order_index": 19
            },
            {
                "name": "materials_needed",
                "label": "Materials Needed",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Materials students need for the assessment. Array of strings. Example: ['Calculator', 'Ruler', 'Graph paper', 'Periodic table']",
                "default_value": [],
                "order_index": 20
            },
            {
                "name": "administration_instructions",
                "label": "Administration Instructions",
                "type": "rich_text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Step-by-step instructions for administering the assessment",
                "order_index": 21
            },
            {
                "name": "mastery_threshold",
                "label": "Mastery Threshold (%)",
                "type": "number",
                "required": False,
                "config": {
                    "min": 0,
                    "max": 100
                },
                "help_text": "Percentage score indicating mastery (typically 70-80%)",
                "order_index": 22
            },
            {
                "name": "alignment_notes",
                "label": "Alignment Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "How this assessment aligns to curriculum, standards, or learning objectives",
                "order_index": 23
            },
            {
                "name": "tags",
                "label": "Tags",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Keywords for organizing. Array of strings.",
                "default_value": [],
                "order_index": 24
            },
            {
                "name": "notes",
                "label": "Teacher Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Additional notes, tips, or observations",
                "order_index": 25
            }
        ],
        created_by=1  # Admin user
    )

    db.add(assessment_type)
    return assessment_type


def create_question_item_content_type(db: Session):
    """
    Create QuestionItem content type.

    QuestionItem: Individual question, task, or prompt within an assessment.
    """
    print("   Creating QuestionItem content type...")

    question_item_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="QuestionItem",
        description="Individual question, task, or prompt used in assessments. Includes multiple choice, constructed response, performance tasks, and other item types with scoring information.",
        icon="QuestionMarkCircleIcon",
        is_system=True,
        attributes=[
            {
                "name": "prompt",
                "label": "Question Prompt",
                "type": "rich_text",
                "required": True,
                "config": {
                    "minLength": 10,
                    "maxLength": 5000
                },
                "help_text": "The question text, task description, or prompt. Can include images, diagrams, or formatted text.",
                "order_index": 0
            },
            {
                "name": "item_type",
                "label": "Item Type",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": [
                        "Multiple Choice - Single Answer",
                        "Multiple Choice - Multiple Answers",
                        "True/False",
                        "Matching",
                        "Fill in the Blank",
                        "Short Answer",
                        "Extended Response/Essay",
                        "Performance Task",
                        "Constructed Response",
                        "Technology-Enhanced (TEI)",
                        "Drag and Drop",
                        "Hot Spot/Clickable Image",
                        "Open-Ended"
                    ]
                },
                "help_text": "Type of question or task",
                "order_index": 1
            },
            {
                "name": "choices",
                "label": "Answer Choices",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "For selected-response items, the answer choices. Array of objects. Example: [{\"id\": \"A\", \"text\": \"Producers\"}, {\"id\": \"B\", \"text\": \"Consumers\"}, ...]",
                "default_value": [],
                "order_index": 2
            },
            {
                "name": "correct_answer",
                "label": "Correct Answer",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "For selected-response items: answer key (e.g., 'B', 'A,C,D'). For constructed-response: sample correct answer or answer guidelines.",
                "order_index": 3
            },
            {
                "name": "rationale",
                "label": "Answer Rationale",
                "type": "rich_text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Explanation of why the correct answer is correct and why distractors are incorrect. Useful for formative feedback.",
                "order_index": 4
            },
            {
                "name": "distractors_analysis",
                "label": "Distractor Analysis",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "For multiple choice items, analysis of each distractor. Example: [{\"id\": \"A\", \"misconception\": \"Confuses producers with consumers\"}, ...]",
                "default_value": [],
                "order_index": 5
            },
            {
                "name": "points",
                "label": "Point Value",
                "type": "number",
                "required": True,
                "config": {
                    "min": 0,
                    "max": 100
                },
                "help_text": "How many points this item is worth",
                "order_index": 6
            },
            {
                "name": "partial_credit",
                "label": "Partial Credit Available",
                "type": "boolean",
                "required": False,
                "config": {},
                "help_text": "Whether partial credit can be awarded for this item",
                "order_index": 7
            },
            {
                "name": "scoring_rubric",
                "label": "Item Scoring Rubric",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Rubric",
                    "multiple": False
                },
                "help_text": "Rubric for scoring constructed-response or performance items",
                "order_index": 8
            },
            {
                "name": "linked_concepts",
                "label": "Linked Concepts",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Concept",
                    "multiple": True
                },
                "help_text": "Concepts this item assesses",
                "order_index": 9
            },
            {
                "name": "linked_standards",
                "label": "Linked Standards",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Standard",
                    "multiple": True
                },
                "help_text": "Standards this item aligns to",
                "order_index": 10
            },
            {
                "name": "cognitive_level",
                "label": "Cognitive Level (Bloom's)",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
                },
                "help_text": "Bloom's Taxonomy level this item targets",
                "order_index": 11
            },
            {
                "name": "depth_of_knowledge",
                "label": "Depth of Knowledge (DOK)",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": ["DOK 1 - Recall", "DOK 2 - Skill/Concept", "DOK 3 - Strategic Thinking", "DOK 4 - Extended Thinking"]
                },
                "help_text": "Webb's Depth of Knowledge level",
                "order_index": 12
            },
            {
                "name": "difficulty",
                "label": "Difficulty Level",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Easy", "Medium", "Hard"]
                },
                "help_text": "Estimated difficulty for target grade level",
                "order_index": 13
            },
            {
                "name": "estimated_time",
                "label": "Estimated Time (minutes)",
                "type": "number",
                "required": False,
                "config": {
                    "min": 0.5,
                    "max": 120,
                    "step": 0.5
                },
                "help_text": "Estimated time for students to complete this item",
                "order_index": 14
            },
            {
                "name": "stimulus_material",
                "label": "Stimulus Material",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Resource",
                    "multiple": False
                },
                "help_text": "Reading passage, graph, diagram, or other stimulus material for this item",
                "order_index": 15
            },
            {
                "name": "accommodations_notes",
                "label": "Accommodations Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 500
                },
                "help_text": "How this item can be adapted for students with accommodations",
                "order_index": 16
            },
            {
                "name": "metadata",
                "label": "Item Metadata",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Additional metadata (item bank ID, last revision date, usage statistics, etc.). JSON object.",
                "default_value": {},
                "order_index": 17
            },
            {
                "name": "tags",
                "label": "Tags",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Keywords for organizing. Array of strings.",
                "default_value": [],
                "order_index": 18
            },
            {
                "name": "notes",
                "label": "Author Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Internal notes about this item",
                "order_index": 19
            }
        ],
        created_by=1  # Admin user
    )

    db.add(question_item_type)
    return question_item_type


def create_rubric_content_type(db: Session):
    """
    Create Rubric content type.

    Rubric: Defines performance levels for scoring open-ended tasks and responses.
    """
    print("   Creating Rubric content type...")

    rubric_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="Rubric",
        description="Scoring guide that defines performance levels and criteria for evaluating student work. Used for constructed responses, essays, projects, and performance tasks.",
        icon="TableCellsIcon",
        is_system=True,
        attributes=[
            {
                "name": "title",
                "label": "Rubric Title",
                "type": "text",
                "required": True,
                "config": {
                    "minLength": 5,
                    "maxLength": 300
                },
                "help_text": "Clear title for the rubric. Example: 'Argumentative Essay Rubric', 'Scientific Investigation Performance Rubric', 'Oral Presentation Rubric'",
                "order_index": 0
            },
            {
                "name": "description",
                "label": "Description",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Brief description of what this rubric assesses and how it should be used",
                "order_index": 1
            },
            {
                "name": "rubric_type",
                "label": "Rubric Type",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": [
                        "Analytic - Multiple Criteria",
                        "Holistic - Single Score",
                        "Single-Point - Meet/Not Meet",
                        "Developmental - Growth-Oriented"
                    ]
                },
                "help_text": "Type of rubric structure",
                "order_index": 2
            },
            {
                "name": "criteria",
                "label": "Criteria",
                "type": "json",
                "required": True,
                "config": {},
                "help_text": "List of criteria being assessed. Array of objects. Example: [{\"id\": \"thesis\", \"name\": \"Thesis Statement\", \"description\": \"Clear, arguable claim\", \"weight\": 20}, ...]",
                "default_value": [],
                "order_index": 3
            },
            {
                "name": "levels",
                "label": "Performance Levels",
                "type": "json",
                "required": True,
                "config": {},
                "help_text": "Performance levels from highest to lowest. Array of objects. Example: [{\"id\": \"advanced\", \"name\": \"Advanced\", \"points\": 4, \"description\": \"Exceeds expectations\"}, {\"id\": \"proficient\", \"name\": \"Proficient\", \"points\": 3}, ...]",
                "default_value": [],
                "order_index": 4
            },
            {
                "name": "descriptors",
                "label": "Performance Descriptors",
                "type": "json",
                "required": True,
                "config": {},
                "help_text": "Matrix of descriptors for each criterion at each level. Array of objects. Example: [{\"criterion_id\": \"thesis\", \"level_id\": \"advanced\", \"descriptor\": \"Thesis is compelling, insightful, and clearly stated...\"}, ...]",
                "default_value": [],
                "order_index": 5
            },
            {
                "name": "total_points",
                "label": "Total Possible Points",
                "type": "number",
                "required": False,
                "config": {
                    "min": 1,
                    "max": 500
                },
                "help_text": "Maximum points possible on this rubric (for analytic rubrics, sum of all criteria)",
                "order_index": 6
            },
            {
                "name": "grade_levels",
                "label": "Grade Levels",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
                    "choices": ["Pre-K", "K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
                },
                "help_text": "Grade levels this rubric is appropriate for",
                "order_index": 7
            },
            {
                "name": "subject",
                "label": "Subject Area",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": [
                        "Mathematics",
                        "English Language Arts",
                        "Science",
                        "Social Studies",
                        "Computer Science",
                        "World Languages",
                        "Fine Arts",
                        "Music",
                        "Physical Education & Health",
                        "Cross-Curricular"
                    ]
                },
                "help_text": "Primary subject area",
                "order_index": 8
            },
            {
                "name": "linked_standards",
                "label": "Linked Standards",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Standard",
                    "multiple": True
                },
                "help_text": "Standards this rubric helps assess",
                "order_index": 9
            },
            {
                "name": "student_friendly_version",
                "label": "Student-Friendly Version",
                "type": "rich_text",
                "required": False,
                "config": {
                    "maxLength": 3000
                },
                "help_text": "Simplified version of the rubric for students to use for self-assessment",
                "order_index": 10
            },
            {
                "name": "scoring_guidelines",
                "label": "Scoring Guidelines",
                "type": "rich_text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Instructions for teachers on how to apply this rubric consistently",
                "order_index": 11
            },
            {
                "name": "anchor_examples",
                "label": "Anchor Examples",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Example student work at each performance level. Array of objects. Example: [{\"level_id\": \"advanced\", \"description\": \"See Student Sample A\", \"link\": \"/samples/a.pdf\"}, ...]",
                "default_value": [],
                "order_index": 12
            },
            {
                "name": "common_pitfalls",
                "label": "Common Scoring Pitfalls",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Common mistakes to avoid when using this rubric",
                "order_index": 13
            },
            {
                "name": "feedback_prompts",
                "label": "Feedback Prompts",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Suggested feedback phrases for each criterion/level to speed up grading. Array of objects.",
                "default_value": [],
                "order_index": 14
            },
            {
                "name": "tags",
                "label": "Tags",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Keywords for organizing. Array of strings.",
                "default_value": [],
                "order_index": 15
            },
            {
                "name": "notes",
                "label": "Author Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Internal notes about this rubric",
                "order_index": 16
            }
        ],
        created_by=1  # Admin user
    )

    db.add(rubric_type)
    return rubric_type


def main():
    """Create assessment and evaluation content types."""
    print("=" * 60)
    print("Creating Assessment and Evaluation Content Types")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Check if Assessment already exists
        print("\n1. Checking Assessment content type...")
        existing_assessment = db.query(ContentTypeModel).filter(ContentTypeModel.name == "Assessment").first()
        if existing_assessment:
            print(f"   ⚠ Assessment type already exists (skipping)")
            print(f"     ID: {existing_assessment.id}")
            print(f"     Attributes: {len(existing_assessment.attributes)}")
        else:
            print("   Creating Assessment content type...")
            assessment_type = create_assessment_content_type(db)
            db.commit()
            print(f"   ✓ Assessment type created: {assessment_type.name}")
            print(f"     ID: {assessment_type.id}")
            print(f"     Attributes: {len(assessment_type.attributes)}")

        # Create QuestionItem type
        print("\n2. Creating QuestionItem content type...")
        question_item_type = create_question_item_content_type(db)
        db.commit()
        print(f"   ✓ QuestionItem type created: {question_item_type.name}")
        print(f"     ID: {question_item_type.id}")
        print(f"     Attributes: {len(question_item_type.attributes)}")

        # Create Rubric type
        print("\n3. Creating Rubric content type...")
        rubric_type = create_rubric_content_type(db)
        db.commit()
        print(f"   ✓ Rubric type created: {rubric_type.name}")
        print(f"     ID: {rubric_type.id}")
        print(f"     Attributes: {len(rubric_type.attributes)}")

        print("\n" + "=" * 60)
        print("All Assessment and Evaluation Content Types Created!")
        print("=" * 60)
        print("\nNext Steps:")
        print("1. Navigate to Content Types in the UI")
        print("2. Create QuestionItem instances for your item bank")
        print("3. Create Rubric instances for scoring open-ended work")
        print("4. Build Assessment instances that reference questions and rubrics")
        print("5. Link assessments to Standards and Learning Targets")
        print("6. Use assessments to measure student progress")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
