from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional
from app.database import Base 
from sqlalchemy.dialects.postgresql import UUID


class Address(Base):
    __tablename__ = 'address'
    
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)

    user = relationship("User", back_populates="addresses")