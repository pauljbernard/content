"""
Create all remaining content types in one efficient script
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.session import SessionLocal
from models.content_type import ContentTypeModel
import uuid

def check_or_create(db, name, create_func):
    """Helper to check if type exists before creating."""
    existing = db.query(ContentTypeModel).filter(ContentTypeModel.name == name).first()
    if existing:
        print(f"   ⚠ {name} already exists (skipping)")
        return existing, False
    else:
        print(f"   Creating {name}...")
        new_type = create_func(db)
        return new_type, True

# Function implementations would go here for each content type
# Creating abbreviated versions for efficiency

def create_all_types():
    """Create all remaining content types."""
    print("=" * 60)
    print("Creating All Remaining Content Types")
    print("=" * 60)
    
    db = SessionLocal()
    created_count = 0
    skipped_count = 0
    
    try:
        # Define all content types to create
        types_to_create = [
            # Format: (name, description, icon, attributes)
            ("CurriculumMap", "Scope and sequence for grade/subject", "MapIcon", [
                {"name": "title", "label": "Map Title", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Title for curriculum map", "order_index": 0},
                {"name": "grade", "label": "Grade", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]}, "help_text": "Grade level", "order_index": 1},
                {"name": "subject", "label": "Subject", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["Math", "ELA", "Science", "Social Studies"]}, "help_text": "Subject area", "order_index": 2},
                {"name": "units", "label": "Units", "type": "reference", "required": False, "config": {"contentType": "Unit", "multiple": True}, "help_text": "Units in this curriculum", "order_index": 3},
                {"name": "timeline", "label": "Timeline", "type": "rich_text", "required": False, "config": {}, "help_text": "Pacing guide", "order_index": 4}
            ]),
            
            ("Alignment", "Mappings between standards", "LinkIcon", [
                {"name": "source_standard", "label": "Source Standard", "type": "reference", "required": True, "config": {"contentType": "Standard", "multiple": False}, "help_text": "Source standard", "order_index": 0},
                {"name": "target_standard", "label": "Target Standard", "type": "reference", "required": True, "config": {"contentType": "Standard", "multiple": False}, "help_text": "Target standard", "order_index": 1},
                {"name": "confidence_score", "label": "Confidence", "type": "number", "required": False, "config": {"min": 0, "max": 1, "step": 0.01}, "help_text": "Alignment confidence 0-1", "order_index": 2},
                {"name": "reviewer_notes", "label": "Notes", "type": "text", "required": False, "config": {"maxLength": 1000}, "help_text": "Reviewer observations", "order_index": 3}
            ]),
            
            ("FeedbackLoop", "Performance data for content updates", "ArrowPathIcon", [
                {"name": "content_id", "label": "Content ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "ID of content being evaluated", "order_index": 0},
                {"name": "feedback_type", "label": "Type", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["Performance Data", "Teacher Review", "Student Feedback", "AI Evaluation"]}, "help_text": "Source of feedback", "order_index": 1},
                {"name": "metrics", "label": "Metrics", "type": "json", "required": False, "config": {}, "help_text": "Performance metrics JSON", "default_value": {}, "order_index": 2},
                {"name": "recommended_changes", "label": "Recommendations", "type": "text", "required": False, "config": {"maxLength": 2000}, "help_text": "Suggested improvements", "order_index": 3}
            ]),
            
            ("VersionedArtifact", "Version metadata wrapper", "DocumentDuplicateIcon", [
                {"name": "artifact_type", "label": "Type", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Type of content", "order_index": 0},
                {"name": "artifact_id", "label": "Artifact ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "ID of versioned content", "order_index": 1},
                {"name": "version", "label": "Version", "type": "text", "required": True, "config": {"maxLength": 50}, "help_text": "Version number/tag", "order_index": 2},
                {"name": "change_summary", "label": "Changes", "type": "text", "required": False, "config": {"maxLength": 1000}, "help_text": "What changed", "order_index": 3},
                {"name": "approval_status", "label": "Status", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["draft", "review", "approved", "published"]}, "help_text": "Approval state", "order_index": 4}
            ]),
            
            ("MediaAsset", "Centralized media library", "PhotoIcon", [
                {"name": "title", "label": "Title", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Asset title", "order_index": 0},
                {"name": "file", "label": "File", "type": "media", "required": True, "config": {"maxSize": 52428800}, "help_text": "Upload file (50MB max)", "order_index": 1},
                {"name": "caption", "label": "Caption", "type": "text", "required": False, "config": {"maxLength": 500}, "help_text": "Caption text", "order_index": 2},
                {"name": "alt_text", "label": "Alt Text", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Accessibility alt text", "order_index": 3},
                {"name": "license", "label": "License", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["All Rights Reserved", "CC BY", "CC BY-SA", "Public Domain"]}, "help_text": "Usage license", "order_index": 4},
                {"name": "transcript", "label": "Transcript", "type": "text", "required": False, "config": {}, "help_text": "Audio/video transcript", "order_index": 5}
            ]),
            
            ("GlossaryTerm", "Subject vocabulary definitions", "BookOpenIcon", [
                {"name": "term", "label": "Term", "type": "text", "required": True, "config": {"minLength": 1, "maxLength": 100}, "help_text": "Vocabulary term", "order_index": 0},
                {"name": "definition", "label": "Definition", "type": "rich_text", "required": True, "config": {"minLength": 10}, "help_text": "Term definition", "order_index": 1},
                {"name": "grade_bands", "label": "Grade Bands", "type": "choice", "required": False, "config": {"multiple": True, "choices": ["K-2", "3-5", "6-8", "9-12"]}, "help_text": "Appropriate grades", "order_index": 2},
                {"name": "linked_concepts", "label": "Concepts", "type": "reference", "required": False, "config": {"contentType": "Concept", "multiple": True}, "help_text": "Related concepts", "order_index": 3}
            ]),
            
            ("PerformanceTask", "Complex cross-disciplinary project", "BriefcaseIcon", [
                {"name": "title", "label": "Title", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Project title", "order_index": 0},
                {"name": "scenario", "label": "Scenario", "type": "rich_text", "required": True, "config": {}, "help_text": "Task scenario/context", "order_index": 1},
                {"name": "roles", "label": "Roles", "type": "json", "required": False, "config": {}, "help_text": "Student roles array", "default_value": [], "order_index": 2},
                {"name": "steps", "label": "Steps", "type": "json", "required": True, "config": {}, "help_text": "Task steps array", "default_value": [], "order_index": 3},
                {"name": "rubric", "label": "Rubric", "type": "reference", "required": False, "config": {"contentType": "Rubric", "multiple": False}, "help_text": "Scoring rubric", "order_index": 4},
                {"name": "linked_standards", "label": "Standards", "type": "reference", "required": False, "config": {"contentType": "Standard", "multiple": True}, "help_text": "Aligned standards", "order_index": 5}
            ]),
            
            ("ProfessionalLearningModule", "Teacher PD content", "AcademicCapIcon", [
                {"name": "title", "label": "Title", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Module title", "order_index": 0},
                {"name": "learning_objectives", "label": "Objectives", "type": "json", "required": True, "config": {}, "help_text": "Teacher learning goals", "default_value": [], "order_index": 1},
                {"name": "resources", "label": "Resources", "type": "reference", "required": False, "config": {"contentType": "Resource", "multiple": True}, "help_text": "PD resources", "order_index": 2},
                {"name": "linked_standards", "label": "Student Standards", "type": "reference", "required": False, "config": {"contentType": "Standard", "multiple": True}, "help_text": "Student standards covered", "order_index": 3}
            ])
        ]
        
        for type_info in types_to_create:
            name, description, icon, attributes = type_info
            existing = db.query(ContentTypeModel).filter(ContentTypeModel.name == name).first()
            
            if existing:
                print(f"\n⚠ {name} already exists (skipping)")
                skipped_count += 1
            else:
                print(f"\n✓ Creating {name}...")
                new_type = ContentTypeModel(
                    id=str(uuid.uuid4()),
                    name=name,
                    description=description,
                    icon=icon,
                    is_system=True,
                    attributes=attributes,
                    created_by=1
                )
                db.add(new_type)
                db.commit()
                created_count += 1
                print(f"  ID: {new_type.id}, Attributes: {len(new_type.attributes)}")
        
        print("\n" + "=" * 60)
        print(f"Complete! Created: {created_count}, Skipped: {skipped_count}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_all_types()
