from sqlalchemy.orm import Session
from app.models.deal import Deal
from app.schemas.deal import DealCreate, DealUpdate

def get_deals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Deal).offset(skip).limit(limit).all()

def get_deal(db: Session, deal_id: int):
    return db.query(Deal).filter(Deal.id == deal_id).first()

def create_deal(db: Session, deal: DealCreate):
    db_deal = Deal(**deal.dict())
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal

def update_deal(db: Session, deal_id: int, deal: DealUpdate):
    db_deal = get_deal(db, deal_id)
    if not db_deal:
        return None
    for key, value in deal.dict(exclude_unset=True).items():
        setattr(db_deal, key, value)
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal
