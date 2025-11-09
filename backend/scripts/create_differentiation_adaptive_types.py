"""
Create differentiation and adaptive content types: LearnerProfile, DifferentiationStrategy, Accommodation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.session import SessionLocal
from models.content_type import ContentTypeModel
import uuid


def create_learner_profile_content_type(db: Session):
    """
    Create LearnerProfile content type.

    LearnerProfile: Captures individual learner needs for adaptive sequencing and personalization.
    """
    print("   Creating LearnerProfile content type...")

    learner_profile_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="LearnerProfile",
        description="Individual learner profile capturing skills, preferences, progress history, and accommodation needs to enable adaptive learning pathways and personalized instruction.",
        icon="UserIcon",
        is_system=True,
        attributes=[
            {
                "name": "student_id",
                "label": "Student ID",
                "type": "text",
                "required": True,
                "config": {
                    "maxLength": 100,
                    "unique": True
                },
                "help_text": "Unique identifier for the student (district student ID, SIS ID, or internal ID)",
                "order_index": 0
            },
            {
                "name": "student_name",
                "label": "Student Name",
                "type": "text",
                "required": True,
                "config": {
                    "minLength": 2,
                    "maxLength": 200
                },
                "help_text": "Student's full name",
                "order_index": 1
            },
            {
                "name": "grade_level",
                "label": "Current Grade Level",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": ["Pre-K", "K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
                },
                "help_text": "Student's current grade level",
                "order_index": 2
            },
            {
                "name": "skills_map",
                "label": "Skills Map",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Map of skills and proficiency levels. Example: {\"fractions_addition\": 0.85, \"photosynthesis\": 0.72, \"topic_sentences\": 0.91} where values are 0-1",
                "default_value": {},
                "order_index": 3
            },
            {
                "name": "learning_preferences",
                "label": "Learning Preferences",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Learning style and preference data. Example: {\"modalityPreference\": \"visual\", \"pacePreference\": \"self-paced\", \"groupingPreference\": \"collaborative\", \"timeOfDay\": \"morning\"}",
                "default_value": {},
                "order_index": 4
            },
            {
                "name": "learning_style",
                "label": "Primary Learning Style",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
                    "choices": ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"]
                },
                "help_text": "Dominant learning modalities (VARK model)",
                "order_index": 5
            },
            {
                "name": "progress_history",
                "label": "Progress History",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Historical progress data. Array of progress snapshots. Example: [{\"date\": \"2024-01-15\", \"assessment_id\": \"abc123\", \"score\": 0.85, \"standards\": [...]}, ...]",
                "default_value": [],
                "order_index": 6
            },
            {
                "name": "accommodations",
                "label": "Accommodations",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Accommodation",
                    "multiple": True
                },
                "help_text": "Active accommodations for this learner (IEP, 504, ELL support)",
                "order_index": 7
            },
            {
                "name": "iep_active",
                "label": "IEP Active",
                "type": "boolean",
                "required": False,
                "config": {},
                "help_text": "Whether student has an active Individualized Education Program",
                "order_index": 8
            },
            {
                "name": "section_504_active",
                "label": "Section 504 Active",
                "type": "boolean",
                "required": False,
                "config": {},
                "help_text": "Whether student has an active Section 504 plan",
                "order_index": 9
            },
            {
                "name": "ell_status",
                "label": "English Language Learner Status",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Not ELL", "ELL Level 1 - Beginner", "ELL Level 2 - Intermediate", "ELL Level 3 - Advanced", "ELL Level 4 - Transitioning", "Former ELL (Monitored)"]
                },
                "help_text": "ELL proficiency level if applicable",
                "order_index": 10
            },
            {
                "name": "home_language",
                "label": "Home Language",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 100
                },
                "help_text": "Primary language spoken at home",
                "order_index": 11
            },
            {
                "name": "gifted_talented",
                "label": "Gifted/Talented",
                "type": "boolean",
                "required": False,
                "config": {},
                "help_text": "Whether student is identified as gifted/talented",
                "order_index": 12
            },
            {
                "name": "interests",
                "label": "Student Interests",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Topics and activities student is interested in. Array of strings. Example: ['dinosaurs', 'soccer', 'music', 'building']",
                "default_value": [],
                "order_index": 13
            },
            {
                "name": "strengths",
                "label": "Strengths",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Student's academic and personal strengths",
                "order_index": 14
            },
            {
                "name": "growth_areas",
                "label": "Growth Areas",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Areas where student needs additional support or development",
                "order_index": 15
            },
            {
                "name": "motivators",
                "label": "Motivators",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "What motivates this student. Array of strings. Example: ['peer recognition', 'choice activities', 'technology', 'hands-on projects']",
                "default_value": [],
                "order_index": 16
            },
            {
                "name": "current_performance_level",
                "label": "Current Performance Level",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Well Below Grade Level", "Below Grade Level", "Approaching Grade Level", "On Grade Level", "Above Grade Level", "Well Above Grade Level"]
                },
                "help_text": "Overall academic performance relative to grade level",
                "order_index": 17
            },
            {
                "name": "attendance_rate",
                "label": "Attendance Rate (%)",
                "type": "number",
                "required": False,
                "config": {
                    "min": 0,
                    "max": 100,
                    "step": 0.1
                },
                "help_text": "Percentage of days attended (for consideration in adaptive pacing)",
                "order_index": 18
            },
            {
                "name": "adaptive_settings",
                "label": "Adaptive System Settings",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Configuration for adaptive learning system. Example: {\"allowSkip\": true, \"scaffoldLevel\": \"high\", \"hintPreference\": \"progressive\", \"feedbackTiming\": \"immediate\"}",
                "default_value": {},
                "order_index": 19
            },
            {
                "name": "last_updated",
                "label": "Last Profile Update",
                "type": "date",
                "required": False,
                "config": {},
                "help_text": "Date when profile was last updated",
                "order_index": 20
            },
            {
                "name": "notes",
                "label": "Teacher Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Additional notes about the learner (private, for educators only)",
                "order_index": 21
            }
        ],
        created_by=1  # Admin user
    )

    db.add(learner_profile_type)
    return learner_profile_type


def create_differentiation_strategy_content_type(db: Session):
    """
    Create DifferentiationStrategy content type.

    DifferentiationStrategy: Describes how lessons adapt for readiness, interest, or learning style.
    """
    print("   Creating DifferentiationStrategy content type...")

    differentiation_strategy_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="DifferentiationStrategy",
        description="Specific instructional strategy for differentiating content, process, or product based on student readiness, interest, or learning profile. Provides concrete guidance for adapting lessons.",
        icon="AdjustmentsHorizontalIcon",
        is_system=True,
        attributes=[
            {
                "name": "name",
                "label": "Strategy Name",
                "type": "text",
                "required": True,
                "config": {
                    "minLength": 5,
                    "maxLength": 200
                },
                "help_text": "Clear, descriptive name. Example: 'Tiered Assignment - Fraction Operations', 'Choice Board - Ecosystem Project', 'Learning Centers - Phonics Skills'",
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
                "help_text": "Detailed explanation of the strategy, including its purpose and implementation",
                "order_index": 1
            },
            {
                "name": "strategy_type",
                "label": "Strategy Type",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": [
                        "Content Differentiation",
                        "Process Differentiation",
                        "Product Differentiation",
                        "Environment/Affect Differentiation"
                    ]
                },
                "help_text": "Which element of instruction is being differentiated (Tomlinson framework)",
                "order_index": 2
            },
            {
                "name": "differentiation_basis",
                "label": "Differentiation Basis",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": True,
                    "choices": [
                        "Readiness/Skill Level",
                        "Student Interest",
                        "Learning Profile/Style",
                        "Language Proficiency",
                        "Cognitive Level"
                    ]
                },
                "help_text": "What student characteristic(s) this strategy responds to",
                "order_index": 3
            },
            {
                "name": "instructional_approach",
                "label": "Instructional Approach",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": [
                        "Tiered Assignment",
                        "Learning Centers/Stations",
                        "Choice Board/Menu",
                        "Flexible Grouping",
                        "Compacting",
                        "Learning Contracts",
                        "Think-Tac-Toe",
                        "RAFT (Role-Audience-Format-Topic)",
                        "Anchor Activities",
                        "Parallel Tasks",
                        "Open-Ended Tasks",
                        "Scaffolded Supports",
                        "Extension/Enrichment"
                    ]
                },
                "help_text": "Specific differentiation technique or structure",
                "order_index": 4
            },
            {
                "name": "applicable_to",
                "label": "Applicable To",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
                    "choices": [
                        "Below Grade Level",
                        "On Grade Level",
                        "Above Grade Level",
                        "English Language Learners",
                        "Students with IEPs",
                        "Gifted/Talented",
                        "Visual Learners",
                        "Auditory Learners",
                        "Kinesthetic Learners"
                    ]
                },
                "help_text": "Which student groups this strategy is designed for",
                "order_index": 5
            },
            {
                "name": "example",
                "label": "Concrete Example",
                "type": "rich_text",
                "required": True,
                "config": {
                    "minLength": 50,
                    "maxLength": 2000
                },
                "help_text": "Detailed example of how this strategy works in practice, including specific tasks or materials",
                "order_index": 6
            },
            {
                "name": "linked_lessons",
                "label": "Linked Lessons",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Lesson",
                    "multiple": True
                },
                "help_text": "Lessons that use this differentiation strategy",
                "order_index": 7
            },
            {
                "name": "linked_units",
                "label": "Linked Units",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Unit",
                    "multiple": True
                },
                "help_text": "Units where this strategy is applied",
                "order_index": 8
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
                "help_text": "Grade levels where this strategy is appropriate",
                "order_index": 9
            },
            {
                "name": "subject_areas",
                "label": "Subject Areas",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
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
                "help_text": "Subject areas where this strategy applies",
                "order_index": 10
            },
            {
                "name": "implementation_time",
                "label": "Implementation Time",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Quick (5-15 min)", "Moderate (15-30 min)", "Extensive (30+ min)", "Multi-day"]
                },
                "help_text": "How much time this strategy requires to implement",
                "order_index": 11
            },
            {
                "name": "preparation_effort",
                "label": "Teacher Preparation Effort",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Low - Minimal prep", "Moderate - Some planning needed", "High - Significant prep required"]
                },
                "help_text": "Amount of teacher preparation required",
                "order_index": 12
            },
            {
                "name": "materials_needed",
                "label": "Materials Needed",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "List of materials required. Array of strings. Example: ['Index cards', 'Chart paper', 'Manipulatives', 'Graphic organizers']",
                "default_value": [],
                "order_index": 13
            },
            {
                "name": "grouping_structure",
                "label": "Grouping Structure",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Individual", "Pairs", "Small Groups", "Whole Class", "Flexible/Mixed"]
                },
                "help_text": "How students are grouped for this strategy",
                "order_index": 14
            },
            {
                "name": "assessment_considerations",
                "label": "Assessment Considerations",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "How to assess student learning when using this differentiated approach",
                "order_index": 15
            },
            {
                "name": "common_challenges",
                "label": "Common Challenges",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Common pitfalls or challenges when implementing this strategy and how to address them",
                "order_index": 16
            },
            {
                "name": "success_indicators",
                "label": "Success Indicators",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "How to know if the strategy is working. Array of strings. Example: ['All students engaged', 'Students working at appropriate challenge level', 'Multiple correct solution paths observed']",
                "default_value": [],
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
                "label": "Implementation Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Additional tips and observations",
                "order_index": 19
            }
        ],
        created_by=1  # Admin user
    )

    db.add(differentiation_strategy_type)
    return differentiation_strategy_type


def create_accommodation_content_type(db: Session):
    """
    Create Accommodation content type.

    Accommodation: Supports for students with IEPs, 504 plans, or ELL needs.
    """
    print("   Creating Accommodation content type...")

    accommodation_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="Accommodation",
        description="Instructional accommodation or support for students with IEPs, Section 504 plans, or English language learner needs. Specifies what support is needed and how to implement it.",
        icon="ShieldCheckIcon",
        is_system=True,
        attributes=[
            {
                "name": "name",
                "label": "Accommodation Name",
                "type": "text",
                "required": True,
                "config": {
                    "minLength": 5,
                    "maxLength": 200
                },
                "help_text": "Clear name for the accommodation. Example: 'Extended Time (1.5x)', 'Text-to-Speech', 'Simplified Language', 'Visual Supports'",
                "order_index": 0
            },
            {
                "name": "description",
                "label": "Description",
                "type": "rich_text",
                "required": True,
                "config": {
                    "minLength": 20,
                    "maxLength": 2000
                },
                "help_text": "Detailed description of what this accommodation entails and how it supports learning",
                "order_index": 1
            },
            {
                "name": "category",
                "label": "Accommodation Category",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": [
                        "Presentation - How content is presented",
                        "Response - How student responds",
                        "Setting - Environment adjustments",
                        "Timing/Scheduling - Time or schedule changes",
                        "Language Support - ELL accommodations",
                        "Assistive Technology",
                        "Behavioral/Emotional Support"
                    ]
                },
                "help_text": "Type of accommodation (IEP/504 category)",
                "order_index": 2
            },
            {
                "name": "applicable_programs",
                "label": "Applicable Programs",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": True,
                    "choices": [
                        "IEP - Individualized Education Program",
                        "504 - Section 504 Plan",
                        "ELL - English Language Learner",
                        "Gifted/Talented",
                        "General Education - All Students"
                    ]
                },
                "help_text": "Which student support programs this accommodation applies to",
                "order_index": 3
            },
            {
                "name": "grade_bands",
                "label": "Grade Bands",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
                    "choices": ["Pre-K", "K-2", "3-5", "6-8", "9-12"]
                },
                "help_text": "Grade level ranges where this accommodation is appropriate",
                "order_index": 4
            },
            {
                "name": "subject_applicability",
                "label": "Subject Applicability",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
                    "choices": [
                        "All Subjects",
                        "Mathematics",
                        "English Language Arts",
                        "Science",
                        "Social Studies",
                        "Computer Science",
                        "World Languages",
                        "Fine Arts",
                        "Physical Education"
                    ]
                },
                "help_text": "Which subjects this accommodation applies to",
                "order_index": 5
            },
            {
                "name": "implementation_guidance",
                "label": "Implementation Guidance",
                "type": "rich_text",
                "required": True,
                "config": {
                    "minLength": 50,
                    "maxLength": 2000
                },
                "help_text": "Step-by-step instructions for implementing this accommodation in the classroom",
                "order_index": 6
            },
            {
                "name": "linked_lessons",
                "label": "Linked Lessons",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Lesson",
                    "multiple": True
                },
                "help_text": "Lessons where this accommodation is specified",
                "order_index": 7
            },
            {
                "name": "linked_assessments",
                "label": "Linked Assessments",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Assessment",
                    "multiple": True
                },
                "help_text": "Assessments where this accommodation is available",
                "order_index": 8
            },
            {
                "name": "required_materials",
                "label": "Required Materials/Technology",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Materials, tools, or technology needed. Array of strings. Example: ['Text-to-speech software', 'Headphones', 'Timer', 'Graphic organizers']",
                "default_value": [],
                "order_index": 9
            },
            {
                "name": "frequency_of_use",
                "label": "Frequency of Use",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Always", "Frequently", "As Needed", "Assessments Only", "Specific Activities Only"]
                },
                "help_text": "How often this accommodation should be provided",
                "order_index": 10
            },
            {
                "name": "training_required",
                "label": "Training Required",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["None - Easy to implement", "Minimal - Brief orientation", "Moderate - Workshop recommended", "Extensive - Specialist training required"]
                },
                "help_text": "Level of teacher training needed to implement effectively",
                "order_index": 11
            },
            {
                "name": "effectiveness_indicators",
                "label": "Effectiveness Indicators",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "How to know if accommodation is working. Array of strings. Example: ['Student completes assignments independently', 'Reduced frustration observed', 'Performance improvement']",
                "default_value": [],
                "order_index": 12
            },
            {
                "name": "alternatives",
                "label": "Alternative Accommodations",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 500
                },
                "help_text": "Other accommodations that could achieve similar support",
                "order_index": 13
            },
            {
                "name": "legal_compliance",
                "label": "Legal/Compliance Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 500
                },
                "help_text": "Any legal or compliance considerations (IDEA, ADA, Title III)",
                "order_index": 14
            },
            {
                "name": "fading_plan",
                "label": "Fading Plan",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "If applicable, how to gradually reduce or remove this accommodation as student develops independence",
                "order_index": 15
            },
            {
                "name": "tags",
                "label": "Tags",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Keywords for organizing. Array of strings.",
                "default_value": [],
                "order_index": 16
            },
            {
                "name": "notes",
                "label": "Implementation Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Additional notes, tips, or observations",
                "order_index": 17
            }
        ],
        created_by=1  # Admin user
    )

    db.add(accommodation_type)
    return accommodation_type


def main():
    """Create differentiation and adaptive content types."""
    print("=" * 60)
    print("Creating Differentiation and Adaptive Content Types")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Create LearnerProfile type
        print("\n1. Creating LearnerProfile content type...")
        learner_profile_type = create_learner_profile_content_type(db)
        db.commit()
        print(f"   ✓ LearnerProfile type created: {learner_profile_type.name}")
        print(f"     ID: {learner_profile_type.id}")
        print(f"     Attributes: {len(learner_profile_type.attributes)}")

        # Create DifferentiationStrategy type
        print("\n2. Creating DifferentiationStrategy content type...")
        differentiation_strategy_type = create_differentiation_strategy_content_type(db)
        db.commit()
        print(f"   ✓ DifferentiationStrategy type created: {differentiation_strategy_type.name}")
        print(f"     ID: {differentiation_strategy_type.id}")
        print(f"     Attributes: {len(differentiation_strategy_type.attributes)}")

        # Create Accommodation type
        print("\n3. Creating Accommodation content type...")
        accommodation_type = create_accommodation_content_type(db)
        db.commit()
        print(f"   ✓ Accommodation type created: {accommodation_type.name}")
        print(f"     ID: {accommodation_type.id}")
        print(f"     Attributes: {len(accommodation_type.attributes)}")

        print("\n" + "=" * 60)
        print("All Differentiation and Adaptive Content Types Created!")
        print("=" * 60)
        print("\nNext Steps:")
        print("1. Navigate to Content Types in the UI")
        print("2. Create LearnerProfile instances for students needing personalization")
        print("3. Build DifferentiationStrategy library for teachers")
        print("4. Create Accommodation instances for IEP/504/ELL support")
        print("5. Link profiles and accommodations to lessons and assessments")
        print("6. Enable adaptive learning pathways based on learner profiles")

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
