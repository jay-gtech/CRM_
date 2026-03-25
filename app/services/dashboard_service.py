from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.lead import Lead
from app.models.deal import Deal
from app.models.activity import Activity
from app.models.meeting import Meeting

def get_dashboard_data(db: Session, user_id: int):
    # Retrieve aggregated counts
    # Since Lead/Deal/Activity don't have created_by yet, we count global records.
    # We keep user-scoping for Meeting where it was explicitly implemented.
    
    total_leads = db.query(func.count(Lead.id)).scalar() or 0
    
    active_deals = db.query(func.count(Deal.id)).filter(
        Deal.stage.notin_(["Won", "Lost"])
    ).scalar() or 0
    
    won_deals = db.query(func.count(Deal.id)).filter(
        Deal.stage == "Won"
    ).scalar() or 0
    
    tasks_count = db.query(func.count(Activity.id)).filter(
        Activity.activity_type == "Task"
    ).scalar() or 0
    
    meetings_count = db.query(func.count(Meeting.id)).filter(Meeting.created_by == user_id).scalar() or 0
    
    # Retrieve top 5 recent activities and meetings
    recent_activities = db.query(Activity).order_by(Activity.created_at.desc()).limit(5).all()
    recent_meetings = db.query(Meeting).filter(Meeting.created_by == user_id).order_by(Meeting.created_at.desc()).limit(5).all()
    
    return {
        "total_leads": total_leads,
        "active_deals": active_deals,
        "won_deals": won_deals,
        "tasks_count": tasks_count,
        "meetings_count": meetings_count,
        "recent_activities": recent_activities,
        "recent_meetings": recent_meetings
    }
