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
    concept_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="Concept",
        api_name="concept",
        description="Atomic idea or skill underpinning multiple standards. Used for semantic linking across curricula and enabling knowledge graph connections.",
        icon="AcademicCapIcon",
        category="pedagogy",
        is_system_type=True,
        schema={
            "attributes": [
                {
                    "name": "name",
                    "display_name": "Concept Name",
                    "type": "text",
                    "required": True,
                    "validation": {
                        "min_length": 3,
                        "max_length": 200
                    },
                    "help_text": "Clear, concise name for the concept (e.g., 'Place Value', 'Photosynthesis', 'Topic Sentence')",
                    "example": "Equivalent Fractions"
                },
                {
                    "name": "description",
                    "display_name": "Description",
                    "type": "rich_text",
                    "required": True,
                    "validation": {
                        "min_length": 50,
                        "max_length": 2000
                    },
                    "help_text": "Detailed explanation of the concept, including what it is, why it's important, and how it connects to learning",
                    "example": "The understanding that fractions represent the same quantity when the numerator and denominator are multiplied by the same number. This foundational concept enables fraction comparison, simplification, and operations."
                },
                {
                    "name": "related_standards",
                    "display_name": "Related Standards",
                    "type": "reference",
                    "reference_type": "standard",
                    "multiple": True,
                    "required": False,
                    "help_text": "Standards that address or depend on this concept",
                    "example": ["CCSS.MATH.3.NF.A.3", "CCSS.MATH.4.NF.A.1"]
                },
                {
                    "name": "parent_concept",
                    "display_name": "Parent Concept",
                    "type": "reference",
                    "reference_type": "concept",
                    "multiple": False,
                    "required": False,
                    "help_text": "Broader concept that this concept is part of (creates concept hierarchy)",
                    "example": "Fractions"
                },
                {
                    "name": "child_concepts",
                    "display_name": "Child Concepts",
                    "type": "reference",
                    "reference_type": "concept",
                    "multiple": True,
                    "required": False,
                    "help_text": "More specific concepts that build on this one",
                    "example": ["Simplifying Fractions", "Comparing Fractions"]
                },
                {
                    "name": "examples",
                    "display_name": "Examples",
                    "type": "list",
                    "item_type": "text",
                    "required": True,
                    "validation": {
                        "min_items": 2,
                        "max_items": 10
                    },
                    "help_text": "Concrete examples that illustrate the concept",
                    "example": [
                        "1/2 = 2/4 = 3/6 = 4/8",
                        "3/5 = 6/10 = 9/15",
                        "Visual: Pizza slices showing 2/4 equals 1/2"
                    ]
                },
                {
                    "name": "misconceptions",
                    "display_name": "Common Misconceptions",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "validation": {
                        "max_items": 10
                    },
                    "help_text": "Common student misunderstandings about this concept",
                    "example": [
                        "Thinking 2/4 is larger than 1/2 because 2 and 4 are bigger numbers",
                        "Believing you can only find equivalent fractions by multiplying by 2"
                    ]
                },
                {
                    "name": "prerequisite_concepts",
                    "display_name": "Prerequisite Concepts",
                    "type": "reference",
                    "reference_type": "concept",
                    "multiple": True,
                    "required": False,
                    "help_text": "Concepts students should understand before learning this one",
                    "example": ["Fraction Basics", "Multiplication Facts"]
                },
                {
                    "name": "grade_level_range",
                    "display_name": "Grade Level Range",
                    "type": "text",
                    "required": False,
                    "help_text": "Grade levels where this concept is typically taught (e.g., '3-5', 'K-2', '9-12')",
                    "example": "3-5"
                },
                {
                    "name": "subject_area",
                    "display_name": "Subject Area",
                    "type": "select",
                    "options": [
                        "Mathematics",
                        "English Language Arts",
                        "Science",
                        "Social Studies",
                        "Computer Science",
                        "World Languages",
                        "Fine Arts",
                        "Physical Education",
                        "Cross-Curricular"
                    ],
                    "required": True,
                    "help_text": "Primary subject area for this concept"
                },
                {
                    "name": "cognitive_level",
                    "display_name": "Cognitive Level (Bloom's)",
                    "type": "select",
                    "options": [
                        "Remember",
                        "Understand",
                        "Apply",
                        "Analyze",
                        "Evaluate",
                        "Create"
                    ],
                    "required": False,
                    "help_text": "Highest Bloom's Taxonomy level required to master this concept"
                },
                {
                    "name": "real_world_applications",
                    "display_name": "Real-World Applications",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "help_text": "How this concept applies outside the classroom",
                    "example": [
                        "Cooking: Doubling or halving recipe measurements",
                        "Shopping: Comparing unit prices and discounts"
                    ]
                },
                {
                    "name": "teaching_strategies",
                    "display_name": "Effective Teaching Strategies",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "help_text": "Research-based strategies for teaching this concept",
                    "example": [
                        "Use visual models (fraction bars, number lines)",
                        "Start with concrete manipulatives before abstract symbols",
                        "Connect to prior knowledge of multiplication"
                    ]
                },
                {
                    "name": "assessment_suggestions",
                    "display_name": "Assessment Suggestions",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "help_text": "Ways to assess student understanding of this concept",
                    "example": [
                        "Have students generate three equivalent fractions for a given fraction",
                        "Ask students to explain why two fractions are equivalent using visual models"
                    ]
                },
                {
                    "name": "vocabulary",
                    "display_name": "Key Vocabulary",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "help_text": "Essential terms students need to know",
                    "example": ["equivalent", "numerator", "denominator", "multiply", "simplify"]
                },
                {
                    "name": "tags",
                    "display_name": "Tags",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "help_text": "Keywords for searching and categorizing (e.g., 'fractions', 'number-sense', 'elementary')"
                }
            ]
        },
        created_by=None
    )

    db.add(concept_type)
    db.commit()
    db.refresh(concept_type)

    print(f"✓ Created Concept content type: {concept_type.id}")
    return concept_type


def create_learning_target_content_type(db: Session):
    """
    Create Learning Target content type.

    Learning Target: Rephrasing of a standard in student-friendly language ("I can…").
    Helps students understand what they're learning and why.
    """
    learning_target_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="Learning Target",
        api_name="learning_target",
        description="Student-friendly rephrasing of standards as 'I can...' statements. Makes learning goals transparent and accessible to students.",
        icon="CheckCircleIcon",
        category="pedagogy",
        is_system_type=True,
        schema={
            "attributes": [
                {
                    "name": "statement",
                    "display_name": "I Can Statement",
                    "type": "text",
                    "required": True,
                    "validation": {
                        "min_length": 10,
                        "max_length": 500,
                        "pattern": "^I can.*"
                    },
                    "help_text": "Student-friendly statement starting with 'I can...' that describes what students will be able to do",
                    "example": "I can compare two fractions with different numerators and different denominators using visual models."
                },
                {
                    "name": "grade",
                    "display_name": "Grade Level",
                    "type": "text",
                    "required": True,
                    "help_text": "Grade level for this learning target (e.g., '3', '4', '9-10', 'K')",
                    "example": "4"
                },
                {
                    "name": "linked_standards",
                    "display_name": "Linked Standards",
                    "type": "reference",
                    "reference_type": "standard",
                    "multiple": True,
                    "required": True,
                    "validation": {
                        "min_items": 1
                    },
                    "help_text": "Educational standards that this learning target addresses",
                    "example": ["CCSS.MATH.4.NF.A.2"]
                },
                {
                    "name": "linked_concepts",
                    "display_name": "Linked Concepts",
                    "type": "reference",
                    "reference_type": "concept",
                    "multiple": True,
                    "required": False,
                    "help_text": "Core concepts that this learning target builds upon",
                    "example": ["Equivalent Fractions", "Fraction Comparison"]
                },
                {
                    "name": "complexity",
                    "display_name": "Complexity Level",
                    "type": "select",
                    "options": [
                        "Low",
                        "Medium",
                        "High"
                    ],
                    "required": True,
                    "help_text": "Overall difficulty/complexity of this learning target for the grade level"
                },
                {
                    "name": "depth_of_knowledge",
                    "display_name": "Depth of Knowledge (DOK)",
                    "type": "select",
                    "options": [
                        "DOK 1: Recall & Reproduction",
                        "DOK 2: Skills & Concepts",
                        "DOK 3: Strategic Thinking",
                        "DOK 4: Extended Thinking"
                    ],
                    "required": True,
                    "help_text": "Webb's Depth of Knowledge level required to meet this target",
                    "example": "DOK 2: Skills & Concepts"
                },
                {
                    "name": "success_criteria",
                    "display_name": "Success Criteria",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "validation": {
                        "min_items": 1,
                        "max_items": 10
                    },
                    "help_text": "Specific, observable criteria that show students have met the target",
                    "example": [
                        "I can explain why 2/3 is greater than 1/2 using a visual model",
                        "I can place fractions in order from least to greatest",
                        "I can use common denominators to compare fractions"
                    ]
                },
                {
                    "name": "assessment_type",
                    "display_name": "How Students Will Show Learning",
                    "type": "multiselect",
                    "options": [
                        "Written Response",
                        "Oral Explanation",
                        "Visual Representation",
                        "Performance Task",
                        "Project",
                        "Quiz/Test",
                        "Discussion",
                        "Demonstration"
                    ],
                    "required": False,
                    "help_text": "Ways students will demonstrate they've met this target"
                },
                {
                    "name": "blooms_taxonomy",
                    "display_name": "Bloom's Taxonomy Level",
                    "type": "select",
                    "options": [
                        "Remember",
                        "Understand",
                        "Apply",
                        "Analyze",
                        "Evaluate",
                        "Create"
                    ],
                    "required": False,
                    "help_text": "Highest Bloom's level required by this target"
                },
                {
                    "name": "subject_area",
                    "display_name": "Subject Area",
                    "type": "select",
                    "options": [
                        "Mathematics",
                        "English Language Arts",
                        "Science",
                        "Social Studies",
                        "Computer Science",
                        "World Languages",
                        "Fine Arts",
                        "Physical Education",
                        "Cross-Curricular"
                    ],
                    "required": True,
                    "help_text": "Primary subject area"
                },
                {
                    "name": "estimated_time",
                    "display_name": "Estimated Time to Master",
                    "type": "text",
                    "required": False,
                    "help_text": "Approximate time needed for most students to master this target (e.g., '2 lessons', '1 week', '3-5 class periods')",
                    "example": "3-5 class periods"
                },
                {
                    "name": "prerequisite_targets",
                    "display_name": "Prerequisite Learning Targets",
                    "type": "reference",
                    "reference_type": "learning_target",
                    "multiple": True,
                    "required": False,
                    "help_text": "Learning targets students should master before this one"
                },
                {
                    "name": "student_friendly_rubric",
                    "display_name": "Student-Friendly Rubric",
                    "type": "rich_text",
                    "required": False,
                    "help_text": "Simple rubric students can use to self-assess (e.g., 'Not Yet', 'Getting There', 'Got It!')",
                    "example": "**Not Yet:** I need help comparing fractions\n**Getting There:** I can compare some fractions with help\n**Got It!:** I can compare any two fractions and explain my thinking"
                },
                {
                    "name": "scaffolds",
                    "display_name": "Scaffolds & Supports",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "help_text": "Supports to help struggling students reach this target",
                    "example": [
                        "Fraction strips",
                        "Number lines with benchmarks (0, 1/2, 1)",
                        "Step-by-step comparison checklist"
                    ]
                },
                {
                    "name": "extensions",
                    "display_name": "Extensions for Advanced Students",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "help_text": "Challenge activities for students who master the target quickly",
                    "example": [
                        "Compare three or more fractions",
                        "Create word problems involving fraction comparison",
                        "Explore comparing fractions greater than 1"
                    ]
                },
                {
                    "name": "academic_vocabulary",
                    "display_name": "Academic Vocabulary",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "help_text": "Key academic terms students need to understand",
                    "example": ["compare", "greater than", "less than", "numerator", "denominator", "benchmark fractions"]
                },
                {
                    "name": "real_world_connection",
                    "display_name": "Real-World Connection",
                    "type": "text",
                    "required": False,
                    "help_text": "Brief explanation of why this matters outside of school",
                    "example": "Comparing fractions helps when cooking (which recipe needs more sugar?), shopping (which deal is better?), and sharing fairly."
                },
                {
                    "name": "formative_assessment",
                    "display_name": "Formative Assessment Ideas",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "help_text": "Quick checks for understanding during instruction",
                    "example": [
                        "Exit ticket: Compare 3/8 and 1/2",
                        "Think-Pair-Share: Which is greater, 2/3 or 5/8?",
                        "Show thumbs up/down: Is 4/5 greater than 3/4?"
                    ]
                },
                {
                    "name": "tags",
                    "display_name": "Tags",
                    "type": "list",
                    "item_type": "text",
                    "required": False,
                    "help_text": "Keywords for searching and organization"
                }
            ]
        },
        created_by=None
    )

    db.add(learning_target_type)
    db.commit()
    db.refresh(learning_target_type)

    print(f"✓ Created Learning Target content type: {learning_target_type.id}")
    return learning_target_type


def main():
    """Create both pedagogical content types."""
    print("=" * 60)
    print("Creating Core Pedagogical Content Types")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Create Concept type
        print("\n1. Creating Concept content type...")
        concept_type = create_concept_content_type(db)
        print(f"   Name: {concept_type.name}")
        print(f"   API Name: {concept_type.api_name}")
        print(f"   Attributes: {len(concept_type.schema['attributes'])}")

        # Create Learning Target type
        print("\n2. Creating Learning Target content type...")
        target_type = create_learning_target_content_type(db)
        print(f"   Name: {target_type.name}")
        print(f"   API Name: {target_type.api_name}")
        print(f"   Attributes: {len(target_type.schema['attributes'])}")

        print("\n" + "=" * 60)
        print("✓ Both content types created successfully!")
        print("=" * 60)

        print("\nNext Steps:")
        print("1. Navigate to Content Types in the UI")
        print("2. Create Concept instances for core ideas in your curriculum")
        print("3. Create Learning Target instances aligned to your standards")
        print("4. Link Concepts to Standards for semantic navigation")
        print("5. Use Learning Targets to make lessons student-centered")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
