from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.schemas.activity import ActivityCreate
from app.services import activity as activity_service

def on_lead_created(db: Session, lead: Lead):
    """
    Simple Workflow Automation: Trigger -> Condition -> Action
    Trigger: New Lead Created
    Action: Auto-generate a follow-up task
    """
    # Action: Create an automatic task
    activity_service.create_activity(db, ActivityCreate(
        activity_type="Task",
        description=f"Auto-assigned: Follow up with new lead {lead.first_name} {lead.last_name}",
        lead_id=lead.id
    ))
