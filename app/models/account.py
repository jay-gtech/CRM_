from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    website = Column(String)
    industry = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    deals = relationship("Deal", back_populates="account", foreign_keys="Deal.account_id")
