from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.schemas.lead import LeadCreate
from app.services.workflow import on_lead_created

def get_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Lead).offset(skip).limit(limit).all()

def get_lead(db: Session, lead_id: int):
    return db.query(Lead).filter(Lead.id == lead_id).first()

from app.models.contact import Contact
from app.models.account import Account
from app.models.deal import Deal
from app.services import deal as deal_service
from app.schemas.deal import DealCreate

def create_lead(db: Session, lead: LeadCreate):
    db_lead = Lead(**lead.model_dump())
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

def convert_lead_to_deal(db: Session, lead_id: int, owner_id: int, deal_name: str, deal_amount: float):
    lead = get_lead(db, lead_id)
    if not lead or lead.status == "Converted":
        return None
    
    # 1. Create/Get Account
    account = db.query(Account).filter(Account.name == lead.company).first()
    if not account:
        account = Account(name=lead.company)
        db.add(account)
        db.flush()
    
    # 2. Create Contact
    contact = Contact(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        phone=lead.phone,
        company=lead.company,
        lead_id=lead.id
    )
    db.add(contact)
    db.flush()
    
    # 3. Create Deal
    deal_in = DealCreate(
        name=deal_name,
        amount=deal_amount,
        stage="New",
        contact_id=contact.id,
        account_id=account.id,
        lead_id=lead.id,
        owner_id=owner_id
    )
    deal = deal_service.create_deal(db, deal_in, owner_id)
    
    # 4. Update Lead Status
    lead.status = "Converted"
    db.add(lead)
    db.commit()
    
    return deal
