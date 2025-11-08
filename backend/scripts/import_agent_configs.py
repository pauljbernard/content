#!/usr/bin/env python3
"""
Import Example Agent Configurations

This script imports example agent configurations as content instances
into the Agent Configuration content type.

Usage:
    python scripts/import_agent_configs.py
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from database.session import SessionLocal
from models.content_type import ContentTypeModel, ContentInstanceModel


def get_agent_configuration_content_type(db: Session) -> ContentTypeModel:
    """Get or create the Agent Configuration content type."""

    # Check if it exists
    content_type = db.query(ContentTypeModel).filter(
        ContentTypeModel.name == "Agent Configuration"
    ).first()

    if content_type:
        print("✓ Agent Configuration content type found")
        return content_type

    # Create it
    print("Creating Agent Configuration content type...")

    attributes = [
        {
            "name": "agent_id",
            "label": "Agent ID",
            "type": "text",
            "required": True,
            "help_text": "Unique identifier for this agent (e.g., 'lesson-generator', 'objective-writer')",
            "config": {"maxLength": 100},
            "order_index": 0,
        },
        {
            "name": "agent_name",
            "label": "Agent Name",
            "type": "text",
            "required": True,
            "help_text": "Display name for this agent (e.g., 'Lesson Content Generator')",
            "config": {"maxLength": 200},
            "order_index": 1,
        },
        {
            "name": "description",
            "label": "Description",
            "type": "long_text",
            "required": False,
            "help_text": "Detailed description of what this agent does",
            "config": {},
            "order_index": 2,
        },
        {
            "name": "target_content_types",
            "label": "Target Content Types",
            "type": "json",
            "required": True,
            "help_text": "Array of content type IDs where this agent can be used",
            "config": {},
            "order_index": 3,
        },
        {
            "name": "target_fields",
            "label": "Target Fields",
            "type": "json",
            "required": True,
            "help_text": "Array of field names this agent can populate",
            "config": {},
            "order_index": 4,
        },
        {
            "name": "retrieval_config",
            "label": "Retrieval Configuration",
            "type": "json",
            "required": True,
            "help_text": "Configuration for RAG retrieval: content_types, knowledge_base_paths, filters",
            "config": {},
            "order_index": 5,
        },
        {
            "name": "prompt_template",
            "label": "Prompt Template",
            "type": "long_text",
            "required": True,
            "help_text": "System prompt template with {placeholders} for context and user inputs",
            "config": {"maxLength": 10000},
            "order_index": 6,
        },
        {
            "name": "required_user_inputs",
            "label": "Required User Inputs",
            "type": "json",
            "required": False,
            "help_text": "Array of field names that must be provided before agent execution",
            "config": {},
            "order_index": 7,
        },
        {
            "name": "field_dependencies",
            "label": "Field Dependencies",
            "type": "json",
            "required": False,
            "help_text": "Array of field names that must be populated before this agent can run",
            "config": {},
            "order_index": 8,
        },
        {
            "name": "validation_rules",
            "label": "Validation Rules",
            "type": "json",
            "required": False,
            "help_text": "Rules to validate generated content",
            "config": {},
            "order_index": 9,
        },
        {
            "name": "model_config",
            "label": "Model Configuration",
            "type": "json",
            "required": True,
            "help_text": "AI model configuration: model, temperature, max_tokens",
            "config": {},
            "order_index": 10,
        },
        {
            "name": "examples",
            "label": "Few-Shot Examples",
            "type": "json",
            "required": False,
            "help_text": "Array of example inputs/outputs for few-shot learning",
            "config": {},
            "order_index": 11,
        },
        {
            "name": "active",
            "label": "Active",
            "type": "boolean",
            "required": True,
            "help_text": "Whether this agent configuration is active",
            "config": {},
            "order_index": 12,
        },
        {
            "name": "trigger_mode",
            "label": "Trigger Mode",
            "type": "choice",
            "required": True,
            "help_text": "How this agent should be triggered",
            "config": {
                "choices": ["manual", "auto_suggest", "auto_populate"],
                "multiple": False,
            },
            "order_index": 13,
        },
        {
            "name": "confidence_threshold",
            "label": "Confidence Threshold",
            "type": "number",
            "required": False,
            "help_text": "Minimum confidence score (0-1) to auto-accept suggestions",
            "config": {"min": 0, "max": 1, "step": 0.1},
            "order_index": 14,
        },
    ]

    content_type = ContentTypeModel(
        name="Agent Configuration",
        description="AI agent configuration for automated content generation",
        icon="sparkles",
        is_system=False,
        attributes=attributes,
    )

    db.add(content_type)
    db.commit()
    db.refresh(content_type)

    print(f"✓ Created Agent Configuration content type (ID: {content_type.id})")
    return content_type


def import_agent_config(db: Session, content_type_id: str, config_file: Path):
    """Import a single agent configuration from JSON file."""

    print(f"\nImporting {config_file.name}...")

    # Load JSON
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    agent_id = config_data.get("agent_id")

    # Check if already exists
    existing = db.query(ContentInstanceModel).filter(
        ContentInstanceModel.content_type_id == content_type_id,
        ContentInstanceModel.data["agent_id"].as_string() == agent_id
    ).first()

    if existing:
        print(f"  ⚠ Agent config '{agent_id}' already exists (ID: {existing.id}), skipping")
        return existing

    # Create instance
    instance = ContentInstanceModel(
        content_type_id=content_type_id,
        data=config_data,
        status="published",  # Agent configs should be published by default
    )

    db.add(instance)
    db.commit()
    db.refresh(instance)

    print(f"  ✓ Imported '{config_data.get('agent_name')}' (ID: {instance.id})")
    return instance


def main():
    """Main import function."""

    print("=" * 60)
    print("Agent Configuration Import")
    print("=" * 60)

    # Get database session
    db = SessionLocal()

    try:
        # Get or create Agent Configuration content type
        content_type = get_agent_configuration_content_type(db)

        # Find all config files
        config_dir = Path(__file__).parent / "example_agent_configs"
        config_files = list(config_dir.glob("*.json"))

        if not config_files:
            print(f"\n⚠ No config files found in {config_dir}")
            return

        print(f"\nFound {len(config_files)} configuration file(s)")

        # Import each config
        imported = []
        for config_file in config_files:
            instance = import_agent_config(db, content_type.id, config_file)
            imported.append(instance)

        print("\n" + "=" * 60)
        print(f"✓ Import complete: {len(imported)} agent configurations")
        print("=" * 60)
        print("\nAgent Configuration IDs:")
        for instance in imported:
            print(f"  - {instance.data.get('agent_id')}: {instance.id}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
