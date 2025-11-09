"""
Create instructional sequence content types: Resource and Unit
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.session import SessionLocal
from models.content_type import ContentTypeModel
import uuid


def create_resource_content_type(db: Session):
    """
    Create Resource content type.

    Resource: Any external or internal asset (PDF, video, simulation, worksheet).
    Used for organizing and cataloging instructional materials.
    """
    print("   Creating Resource content type...")

    resource_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="Resource",
        description="External or internal instructional asset including PDFs, videos, simulations, worksheets, and other learning materials. Enables organized cataloging and discovery of teaching resources.",
        icon="DocumentTextIcon",
        is_system=True,
        attributes=[
            {
                "name": "title",
                "label": "Resource Title",
                "type": "text",
                "required": True,
                "config": {
                    "minLength": 3,
                    "maxLength": 300
                },
                "help_text": "Clear, descriptive title for the resource. Example: 'Fraction Circles Manipulative Kit', 'Photosynthesis Animation Video', 'Revolutionary War Primary Source Documents'",
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
                "help_text": "Detailed description of the resource, including its purpose, contents, and instructional use",
                "order_index": 1
            },
            {
                "name": "resource_type",
                "label": "Resource Type",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": [
                        "PDF Document",
                        "Video",
                        "Audio",
                        "Interactive Simulation",
                        "Worksheet",
                        "Presentation",
                        "Image",
                        "Infographic",
                        "Game",
                        "Quiz",
                        "Manipulative",
                        "Website/Link",
                        "Software/App",
                        "Dataset",
                        "Code/Script",
                        "Other"
                    ]
                },
                "help_text": "Type of resource (determines icon and handling)",
                "order_index": 2
            },
            {
                "name": "url",
                "label": "Resource URL",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 2000,
                    "pattern": "^(https?://|/uploads/|/assets/).*"
                },
                "help_text": "URL to access the resource. Can be external (https://...) or internal (/uploads/..., /assets/...)",
                "order_index": 3
            },
            {
                "name": "file_upload",
                "label": "Upload File",
                "type": "media",
                "required": False,
                "config": {
                    "accept": ".pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.mp4,.mp3,.png,.jpg,.jpeg,.gif,.svg,.zip",
                    "maxSize": 52428800  # 50MB
                },
                "help_text": "Upload resource file (if not providing external URL). Maximum 50MB.",
                "order_index": 4
            },
            {
                "name": "thumbnail",
                "label": "Thumbnail Image",
                "type": "media",
                "required": False,
                "config": {
                    "accept": ".png,.jpg,.jpeg,.gif,.svg",
                    "maxSize": 2097152  # 2MB
                },
                "help_text": "Preview image for the resource (recommended 16:9 aspect ratio, 1280x720 or 640x360)",
                "order_index": 5
            },
            {
                "name": "license",
                "label": "License",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": [
                        "All Rights Reserved",
                        "CC0 - Public Domain",
                        "CC BY - Attribution",
                        "CC BY-SA - Attribution-ShareAlike",
                        "CC BY-ND - Attribution-NoDerivatives",
                        "CC BY-NC - Attribution-NonCommercial",
                        "CC BY-NC-SA - Attribution-NonCommercial-ShareAlike",
                        "CC BY-NC-ND - Attribution-NonCommercial-NoDerivatives",
                        "Fair Use (Educational)",
                        "Proprietary/Licensed",
                        "Open Educational Resource (OER)"
                    ]
                },
                "help_text": "Usage rights and licensing for this resource",
                "order_index": 6
            },
            {
                "name": "license_details",
                "label": "License Details",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Additional licensing information, attribution requirements, or restrictions",
                "order_index": 7
            },
            {
                "name": "locale",
                "label": "Language/Locale",
                "type": "choice",
                "required": True,
                "config": {
                    "multiple": False,
                    "choices": [
                        "en-US - English (United States)",
                        "en-GB - English (United Kingdom)",
                        "es-MX - Spanish (Mexico)",
                        "es-ES - Spanish (Spain)",
                        "fr-FR - French (France)",
                        "de-DE - German (Germany)",
                        "zh-CN - Chinese (Simplified)",
                        "ja-JP - Japanese (Japan)",
                        "ar-SA - Arabic (Saudi Arabia)",
                        "pt-BR - Portuguese (Brazil)",
                        "multilingual",
                        "other"
                    ]
                },
                "help_text": "Primary language of the resource",
                "order_index": 8
            },
            {
                "name": "grade_levels",
                "label": "Grade Levels",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
                    "choices": ["Pre-K", "K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "Higher Ed", "Professional"]
                },
                "help_text": "Appropriate grade levels for this resource",
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
                        "Career & Technical Education"
                    ]
                },
                "help_text": "Subject areas this resource supports",
                "order_index": 10
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
                "help_text": "Concepts this resource helps teach or illustrate",
                "order_index": 11
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
                "help_text": "Standards this resource aligns with",
                "order_index": 12
            },
            {
                "name": "author",
                "label": "Author/Creator",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 300
                },
                "help_text": "Name of the resource creator or author",
                "order_index": 13
            },
            {
                "name": "publisher",
                "label": "Publisher/Source",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 300
                },
                "help_text": "Publisher or source organization",
                "order_index": 14
            },
            {
                "name": "publication_date",
                "label": "Publication Date",
                "type": "date",
                "required": False,
                "config": {},
                "help_text": "When the resource was created or published",
                "order_index": 15
            },
            {
                "name": "duration",
                "label": "Duration/Length",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 100
                },
                "help_text": "Time to complete or consume resource (e.g., '15 minutes', '3 pages', '45 min video')",
                "order_index": 16
            },
            {
                "name": "accessibility_features",
                "label": "Accessibility Features",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": True,
                    "choices": [
                        "Closed Captions",
                        "Transcripts",
                        "Audio Descriptions",
                        "Screen Reader Compatible",
                        "Keyboard Navigation",
                        "High Contrast Mode",
                        "Adjustable Text Size",
                        "Alternative Text for Images",
                        "Sign Language Interpretation"
                    ]
                },
                "help_text": "Accessibility features included in this resource",
                "order_index": 17
            },
            {
                "name": "instructional_strategies",
                "label": "Suggested Instructional Strategies",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "How to effectively use this resource in instruction",
                "order_index": 18
            },
            {
                "name": "differentiation_notes",
                "label": "Differentiation Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "How to adapt this resource for different learner needs",
                "order_index": 19
            },
            {
                "name": "technical_requirements",
                "label": "Technical Requirements",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 500
                },
                "help_text": "Software, hardware, or platform requirements (e.g., 'Requires Adobe Reader', 'Works on tablets', 'Needs internet connection')",
                "order_index": 20
            },
            {
                "name": "cost",
                "label": "Cost",
                "type": "choice",
                "required": False,
                "config": {
                    "multiple": False,
                    "choices": ["Free", "Freemium", "Paid", "Subscription Required", "Institutional License Required"]
                },
                "help_text": "Cost model for this resource",
                "order_index": 21
            },
            {
                "name": "quality_rating",
                "label": "Quality Rating",
                "type": "number",
                "required": False,
                "config": {
                    "min": 1,
                    "max": 5,
                    "step": 0.5
                },
                "help_text": "Internal quality rating (1-5 stars)",
                "order_index": 22
            },
            {
                "name": "tags",
                "label": "Tags",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Keywords for searching and organizing. Array of strings. Example: ['manipulatives', 'visual', 'hands-on', 'inquiry']",
                "default_value": [],
                "order_index": 23
            },
            {
                "name": "notes",
                "label": "Internal Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Private notes for instructors or administrators (not shown to students)",
                "order_index": 24
            }
        ],
        created_by=1  # Admin user
    )

    db.add(resource_type)
    return resource_type


def create_unit_content_type(db: Session):
    """
    Create Unit content type.

    Unit: Cluster of lessons sharing a theme or culminating in a project.
    Represents a multi-week instructional sequence.
    """
    print("   Creating Unit content type...")

    unit_type = ContentTypeModel(
        id=str(uuid.uuid4()),
        name="Unit",
        description="A coherent cluster of lessons organized around a theme, essential questions, or culminating project. Typically spans 2-6 weeks of instruction.",
        icon="RectangleGroupIcon",
        is_system=True,
        attributes=[
            {
                "name": "title",
                "label": "Unit Title",
                "type": "text",
                "required": True,
                "config": {
                    "minLength": 5,
                    "maxLength": 200
                },
                "help_text": "Clear, engaging title for the unit. Example: 'Exploring Ecosystems', 'The American Revolution', 'Algebraic Thinking and Patterns'",
                "order_index": 0
            },
            {
                "name": "summary",
                "label": "Unit Summary",
                "type": "rich_text",
                "required": True,
                "config": {
                    "minLength": 100,
                    "maxLength": 3000
                },
                "help_text": "Comprehensive overview of the unit, including its purpose, scope, and learning trajectory",
                "order_index": 1
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
                "help_text": "Primary grade level for this unit",
                "order_index": 2
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
                        "Physical Education & Health",
                        "Interdisciplinary"
                    ]
                },
                "help_text": "Primary subject area for this unit",
                "order_index": 3
            },
            {
                "name": "duration",
                "label": "Duration (weeks)",
                "type": "number",
                "required": True,
                "config": {
                    "min": 1,
                    "max": 36,
                    "step": 0.5
                },
                "help_text": "Estimated duration in weeks (e.g., 3, 4.5, 6)",
                "order_index": 4
            },
            {
                "name": "essential_questions",
                "label": "Essential Questions",
                "type": "json",
                "required": True,
                "config": {},
                "help_text": "Overarching questions that guide the unit. Array of strings. Example: ['How do organisms depend on each other in an ecosystem?', 'What happens when ecosystems are disrupted?', 'How can we protect ecosystems?']",
                "default_value": [],
                "order_index": 5
            },
            {
                "name": "big_ideas",
                "label": "Big Ideas",
                "type": "json",
                "required": True,
                "config": {},
                "help_text": "Core understandings students should take away. Array of strings. Example: ['All organisms in an ecosystem are interconnected', 'Energy flows through ecosystems', 'Human actions affect ecosystem health']",
                "default_value": [],
                "order_index": 6
            },
            {
                "name": "learning_objectives",
                "label": "Unit Learning Objectives",
                "type": "rich_text",
                "required": True,
                "config": {
                    "minLength": 50,
                    "maxLength": 2000
                },
                "help_text": "What students will know and be able to do by the end of the unit",
                "order_index": 7
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
                "help_text": "State/national standards addressed in this unit",
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
                "help_text": "Key concepts developed throughout the unit",
                "order_index": 9
            },
            {
                "name": "learning_targets",
                "label": "Learning Targets",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Learning Target",
                    "multiple": True
                },
                "help_text": "Student-friendly 'I can' statements for the unit",
                "order_index": 10
            },
            {
                "name": "lessons",
                "label": "Lessons",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Lesson",
                    "multiple": True
                },
                "help_text": "Individual lessons that comprise this unit (in sequence)",
                "order_index": 11
            },
            {
                "name": "assessments",
                "label": "Assessments",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Assessment",
                    "multiple": True
                },
                "help_text": "Formative and summative assessments for this unit",
                "order_index": 12
            },
            {
                "name": "resources",
                "label": "Unit Resources",
                "type": "reference",
                "required": False,
                "config": {
                    "contentType": "Resource",
                    "multiple": True
                },
                "help_text": "Materials, texts, media, and other resources used throughout the unit",
                "order_index": 13
            },
            {
                "name": "prerequisite_knowledge",
                "label": "Prerequisite Knowledge",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "What students should already know before starting this unit",
                "order_index": 14
            },
            {
                "name": "vocabulary",
                "label": "Unit Vocabulary",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Key terms introduced and used throughout the unit. Array of strings. Example: ['ecosystem', 'producer', 'consumer', 'decomposer', 'food chain', 'food web']",
                "default_value": [],
                "order_index": 15
            },
            {
                "name": "culminating_project",
                "label": "Culminating Project",
                "type": "rich_text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Description of the final project or performance task that demonstrates unit learning",
                "order_index": 16
            },
            {
                "name": "differentiation_strategies",
                "label": "Differentiation Strategies",
                "type": "rich_text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "How to adapt the unit for diverse learners (scaffolds, extensions, language support)",
                "order_index": 17
            },
            {
                "name": "interdisciplinary_connections",
                "label": "Interdisciplinary Connections",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "How this unit connects to other subjects or can be integrated with other content areas",
                "order_index": 18
            },
            {
                "name": "real_world_connections",
                "label": "Real-World Connections",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "How unit content relates to students' lives and the world beyond school",
                "order_index": 19
            },
            {
                "name": "ell_supports",
                "label": "English Language Learner Supports",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Specific strategies and scaffolds for supporting English language learners",
                "order_index": 20
            },
            {
                "name": "technology_integration",
                "label": "Technology Integration",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "How technology is used to enhance learning in this unit",
                "order_index": 21
            },
            {
                "name": "materials_needed",
                "label": "Materials Needed",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "List of materials and supplies needed for the entire unit. Array of strings.",
                "default_value": [],
                "order_index": 22
            },
            {
                "name": "pacing_guide",
                "label": "Pacing Guide",
                "type": "rich_text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Suggested timeline and pacing for unit lessons and activities",
                "order_index": 23
            },
            {
                "name": "parent_communication",
                "label": "Parent Communication",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 1000
                },
                "help_text": "Suggested communication to families about this unit (can be adapted for newsletters)",
                "order_index": 24
            },
            {
                "name": "tags",
                "label": "Tags",
                "type": "json",
                "required": False,
                "config": {},
                "help_text": "Keywords for searching and organizing. Array of strings.",
                "default_value": [],
                "order_index": 25
            },
            {
                "name": "notes",
                "label": "Teacher Notes",
                "type": "text",
                "required": False,
                "config": {
                    "maxLength": 2000
                },
                "help_text": "Additional notes, tips, or reflections for teachers",
                "order_index": 26
            }
        ],
        created_by=1  # Admin user
    )

    db.add(unit_type)
    return unit_type


def main():
    """Create instructional sequence content types."""
    print("=" * 60)
    print("Creating Instructional Sequence Content Types")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Create Resource type
        print("\n1. Creating Resource content type...")
        resource_type = create_resource_content_type(db)
        db.commit()
        print(f"   ✓ Resource type created: {resource_type.name}")
        print(f"     ID: {resource_type.id}")
        print(f"     Attributes: {len(resource_type.attributes)}")

        # Create Unit type
        print("\n2. Creating Unit content type...")
        unit_type = create_unit_content_type(db)
        db.commit()
        print(f"   ✓ Unit type created: {unit_type.name}")
        print(f"     ID: {unit_type.id}")
        print(f"     Attributes: {len(unit_type.attributes)}")

        print("\n" + "=" * 60)
        print("All Instructional Sequence Content Types Created!")
        print("=" * 60)
        print("\nNext Steps:")
        print("1. Navigate to Content Types in the UI")
        print("2. Create Resource instances to catalog your materials")
        print("3. Build Units that reference Lessons, Concepts, and Resources")
        print("4. Link Units to Standards and Learning Targets")
        print("5. Use Units to organize curriculum scope and sequence")

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
