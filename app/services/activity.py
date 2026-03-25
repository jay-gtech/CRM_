from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate

def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Activity).order_by(Activity.created_at.desc()).offset(skip).limit(limit).all()

def get_activities_by_deal(db: Session, deal_id: int):
    return db.query(Activity).filter(Activity.deal_id == deal_id).order_by(Activity.created_at.desc()).all()

def create_activity(db: Session, activity: ActivityCreate, user_id: int):
    db_activity = Activity(**activity.model_dump(), user_id=user_id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity
