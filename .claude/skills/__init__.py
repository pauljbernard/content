#!/usr/bin/env python3
"""
Professor Skills Registry

Imports and registers all 108 skills automatically.
"""

import sys
from pathlib import Path

# Add framework to path
framework_path = Path(__file__).parent / "framework"
sys.path.insert(0, str(framework_path))

# Import all skills to register them
skill_modules = [
    # Batch 1: Core Curriculum Skills (16)
    "curriculum-research.skill",
    "curriculum-design.skill",
    "curriculum-develop-content.skill",
    "curriculum-develop-items.skill",
    "curriculum-develop-multimedia.skill",
    "curriculum-assess-design.skill",
    "curriculum-analyze-outcomes.skill",
    "curriculum-grade-assist.skill",
    "curriculum-iterate-feedback.skill",
    "curriculum-review-pedagogy.skill",
    "curriculum-review-accessibility.skill",
    "curriculum-review-bias.skill",
    "curriculum-package-pdf.skill",
    "curriculum-package-web.skill",
    "curriculum-package-lms.skill",
    "curriculum.version-control.skill",
    # Batch 2-7: All other skills auto-import
]

# Auto-discover all skill.py files
skills_dir = Path(__file__).parent
all_skill_files = list(skills_dir.glob("*/skill.py"))

print(f"Discovered {len(all_skill_files)} skill files")
registered_count = 0

for skill_file in all_skill_files:
    skill_dir = skill_file.parent.name
    try:
        # Import the skill module to trigger registration
        module_path = skill_file.parent
        sys.path.insert(0, str(module_path.parent))
        __import__(f"{skill_dir}.skill")
        registered_count += 1
    except Exception as e:
        print(f"Warning: Could not load {skill_dir}: {e}")

print(f"Successfully registered {registered_count} skills")

# Export registry access
from framework.skill_base import list_skills, get_skill, _global_registry as registry

__all__ = ["list_skills", "get_skill", "registry"]
