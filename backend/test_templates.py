"""Test workflow templates access."""
from database.session import SessionLocal
from models.user import User
from models.agent import AgentJob
from models.content import Content
from models.workflow import AgentWorkflow

db = SessionLocal()

# Query templates
templates = db.query(AgentWorkflow).filter(
    AgentWorkflow.is_template == True
).all()

print(f"Found {len(templates)} workflow templates:\n")

for template in templates:
    print(f"  {template.id}. {template.name}")
    print(f"     Status: {template.status}")
    print(f"     Steps: {len(template.steps)}")
    print(f"     Public: {template.is_public}")
    print()

db.close()
