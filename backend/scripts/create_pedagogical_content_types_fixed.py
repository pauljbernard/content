"""
Create core pedagogical content types: Concept and Learning Target
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.session import SessionLocal
from models.content_type import ContentTypeModel
import uuid


def create_concept_content_type(db: Session):
    """
    Create Concept content type.

    Concept: Atomic idea or skill underpinning multiple standards.
    Used for semantic linking across curricula.
    """
    print("   Creating Concept content type...")

    concept_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="Concept",
        description="Atomic idea or skill underpinning multiple standards. Used for semantic linking across curricula and enabling knowledge graph connections.",
        icon="AcademicCapIcon",
        is_system=True,
        attributes=[
            {
                "name": "name",
                "label": "Concept Name",
                "type": "text",
                "required": True,
                "config": {
                    "minLength": 3,
                    "maxLength": 200
                },
                "help_text": "Clear, concise name for the concept. Example: 'Equivalent Fractions', 'Photosynthesis', 'Topic Sentence'",
                "order_index": 0
            },
            {
                "name": "description",
                "label": "Description",
                "type": "rich_text",
                "required": True,
                "config": {
                    "minLength": 50,
                    "maxLength": 2000
                },
                "help_text": "Comprehensive explanation of the concept, including its definition, key characteristics, and importance in the curriculum",
                "order_index": 1
            },
            {
                "name": "related_standards",
                "label": "Related Standards",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Standard",
                    "multiple": True
                },
                "help_text": "Standards that directly address or incorporate this concept",
                "order_index": 2
            },
            {
                "name": "parent_concept",
                "label": "Parent Concept",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Concept",
                    "multiple": False
                },
                "help_text": "Broader concept that contains or encompasses this concept (for building concept hierarchies)",
                "order_index": 3
            },
            {
                "name": "child_concepts",
                "label": "Child Concepts",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Concept",
                    "multiple": True
                },
                "help_text": "More specific sub-concepts that fall under this concept",
                "order_index": 4
            },
            {
                "name": "examples",
                "label": "Examples",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Concrete examples demonstrating the concept. Array of strings. Example: ['1/2 = 2/4 = 3/6', '3/4 = 6/8 = 9/12']",
                "default_value": [],
                "order_index": 5
            },
            {
                "name": "misconceptions",
                "label": "Common Misconceptions",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Common student misunderstandings about this concept. Array of strings. Example: ['Students think fractions with larger denominators are bigger', 'Confusion between numerator and denominator roles']",
                "default_value": [],
                "order_index": 6
            },
            {
                "name": "prerequisite_concepts",
                "label": "Prerequisite Concepts",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Concept",
                    "multiple": True
                },
                "help_text": "Concepts students should understand before learning this concept",
                "order_index": 7
            },
            {
                "name": "grade_level_range",
                "label": "Grade Level Range",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
                    "choices": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
                },
                "help_text": "Grade levels where this concept is typically taught",
                "order_index": 8
            },
            {
                "name": "subject_area",
                "label": "Subject Area",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": ["Mathematics", "English Language Arts", "Science", "Social Studies", "Computer Science", "World Languages", "Fine Arts", "Physical Education & Health"]
                },
                "help_text": "Primary subject area for this concept",
                "order_index": 9
            },
            {
                "name": "cognitive_level",
                "label": "Cognitive Level (Bloom's Taxonomy)",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
                },
                "help_text": "Primary cognitive level at which students typically engage with this concept",
                "order_index": 10
            },
            {
                "name": "real_world_applications",
                "label": "Real-World Applications",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "How this concept is used in real-world contexts outside the classroom",
                "order_index": 11
            },
            {
                "name": "teaching_strategies",
                "label": "Recommended Teaching Strategies",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Effective instructional approaches for teaching this concept",
                "order_index": 12
            },
            {
                "name": "assessment_suggestions",
                "label": "Assessment Suggestions",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Ways to assess student understanding of this concept",
                "order_index": 13
            },
            {
                "name": "vocabulary",
                "label": "Key Vocabulary",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Important terms associated with this concept. Array of strings. Example: ['numerator', 'denominator', 'equivalent', 'simplify']",
                "default_value": [],
                "order_index": 14
            },
            {
                "name": "tags",
                "label": "Tags",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Additional metadata tags for organizing and searching. Array of strings.",
                "default_value": [],
                "order_index": 15
            }
        ],
        created_by=1  # Admin user
    )

    db.add(concept_type)
    return concept_type


def create_learning_target_content_type(db: Session):
    """
    Create Learning Target content type.

    Learning Target: Student-friendly rephrasing of standards ("I can..." statements).
    """
    print("   Creating Learning Target content type...")

    learning_target_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="Learning Target",
        description="Student-friendly rephrasing of a standard in 'I can...' language. Helps students understand learning goals and self-assess progress.",
        icon="CheckBadgeIcon",
        is_system=True,
        attributes=[
            {
                "name": "statement",
                "label": "Learning Target Statement",
                "type": "text",
                "required": True,
                "config": {
                    "minLength": 10,
                    "maxLength": 500,
                    "pattern": "^I can\\s+"
                },
                "help_text": "Student-friendly 'I can...' statement. Must start with 'I can'. Example: 'I can identify and create equivalent fractions using visual models and multiplication'",
                "order_index": 0
            },
            {
                "name": "grade",
                "label": "Grade Level",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
                },
                "help_text": "Target grade level for this learning target",
                "order_index": 1
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
                "help_text": "Standards that this learning target addresses (at least one required)",
                "order_index": 2
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
                "help_text": "Concepts that underpin this learning target",
                "order_index": 3
            },
            {
                "name": "complexity",
                "label": "Complexity Level",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": ["Low", "Medium", "High"]
                },
                "help_text": "Overall complexity of the learning target for the grade level",
                "order_index": 4
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
                "help_text": "Webb's Depth of Knowledge level for this target",
                "order_index": 5
            },
            {
                "name": "success_criteria",
                "label": "Success Criteria",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Observable indicators that students have met this target. Array of strings. Example: ['Correctly identifies 4 out of 5 equivalent fraction pairs', 'Creates visual models showing equivalence', 'Explains reasoning using mathematical language']",
                "default_value": [],
                "order_index": 6
            },
            {
                "name": "assessment_type",
                "label": "Assessment Type",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
                    "choices": ["Formative", "Summative", "Performance Task", "Self-Assessment", "Peer Assessment", "Exit Ticket", "Portfolio"]
                },
                "help_text": "Types of assessments suitable for measuring this target",
                "order_index": 7
            },
            {
                "name": "blooms_taxonomy",
                "label": "Bloom's Taxonomy Level",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
                },
                "help_text": "Primary cognitive level of this learning target",
                "order_index": 8
            },
            {
                "name": "subject_area",
                "label": "Subject Area",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": ["Mathematics", "English Language Arts", "Science", "Social Studies", "Computer Science", "World Languages", "Fine Arts", "Physical Education & Health"]
                },
                "help_text": "Subject area for this learning target",
                "order_index": 9
            },
            {
                "name": "estimated_time",
                "label": "Estimated Learning Time (minutes)",
                "type": "number",
                "required": False,
                "config": {
                    "min": 5,
                    "max": 600
                },
                "help_text": "Approximate time for students to achieve this target",
                "order_index": 10
            },
            {
                "name": "prerequisite_targets",
                "label": "Prerequisite Learning Targets",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Learning Target",
                    "multiple": True
                },
                "help_text": "Learning targets students should achieve before this one",
                "order_index": 11
            },
            {
                "name": "student_friendly_rubric",
                "label": "Student-Friendly Rubric",
                "type": "rich_text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Simple rubric students can use to self-assess their progress (e.g., 'I'm starting to...', 'I can...', 'I can teach others...')",
                "order_index": 12
            },
            {
                "name": "scaffolds",
                "label": "Scaffolds for Support",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Supports for students who need help reaching this target. Array of strings. Example: ['Use fraction bars or circles', 'Work with a partner', 'Start with simpler fractions (halves and fourths)']",
                "default_value": [],
                "order_index": 13
            },
            {
                "name": "extensions",
                "label": "Extensions for Advanced Learners",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Challenge activities for students who quickly master this target. Array of strings.",
                "default_value": [],
                "order_index": 14
            },
            {
                "name": "academic_vocabulary",
                "label": "Academic Vocabulary",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Key terms students need to understand for this target. Array of strings.",
                "default_value": [],
                "order_index": 15
            },
            {
                "name": "real_world_connection",
                "label": "Real-World Connection",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 500
                },
                "help_text": "How this learning connects to students' lives or real-world contexts",
                "order_index": 16
            },
            {
                "name": "formative_assessment",
                "label": "Formative Assessment Ideas",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Quick checks for understanding during learning. Array of strings. Example: ['Show thumbs up/down for confidence', 'Draw a visual model', 'Explain to a partner']",
                "default_value": [],
                "order_index": 17
            },
            {
                "name": "tags",
                "label": "Tags",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Additional metadata tags for organizing and searching. Array of strings.",
                "default_value": [],
                "order_index": 18
            }
        ],
        created_by=1  # Admin user
    )

    db.add(learning_target_type)
    return learning_target_type


def main():
    """Create pedagogical content types."""
    print("=" * 60)
    print("Creating Core Pedagogical Content Types")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Create Concept type
        print("\n1. Creating Concept content type...")
        concept_type = create_concept_content_type(db)
        db.commit()
        print(f"   ✓ Concept type created: {concept_type.name}")
        print(f"     ID: {concept_type.id}")
        print(f"     Attributes: {len(concept_type.attributes)}")

        # Create Learning Target type
        print("\n2. Creating Learning Target content type...")
        learning_target_type = create_learning_target_content_type(db)
        db.commit()
        print(f"   ✓ Learning Target type created: {learning_target_type.name}")
        print(f"     ID: {learning_target_type.id}")
        print(f"     Attributes: {len(learning_target_type.attributes)}")

        print("\n" + "=" * 60)
        print("All Pedagogical Content Types Created Successfully!")
        print("=" * 60)
        print("\nNext Steps:")
        print("1. Navigate to Content Types in the UI")
        print("2. Start creating Concept instances to build your knowledge graph")
        print("3. Create Learning Targets linked to your Standards")
        print("4. Use semantic relationships to connect curricula")

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
