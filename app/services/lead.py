from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.schemas.lead import LeadCreate
from app.services.workflow import on_lead_created

def get_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Lead).offset(skip).limit(limit).all()

def get_lead(db: Session, lead_id: int):
    return db.query(Lead).filter(Lead.id == lead_id).first()

def create_lead(db: Session, lead: LeadCreate):
    db_lead = Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    # Simple Workflow Hook: On lead creation assign default user or task
    on_lead_created(db, db_lead)
    
    return db_lead

def get_lead_by_email(db: Session, email: str):
    return db.query(Lead).filter(Lead.email == email).first()

def get_lead_by_phone(db: Session, phone: str):
    return db.query(Lead).filter(Lead.phone == phone).first()

def bulk_update_status(db: Session, lead_ids: list[int], status: str):
    db.query(Lead).filter(Lead.id.in_(lead_ids)).update({Lead.status: status}, synchronize_session=False)
    db.commit()

def bulk_delete(db: Session, lead_ids: list[int]):
    db.query(Lead).filter(Lead.id.in_(lead_ids)).delete(synchronize_session=False)
    db.commit()
