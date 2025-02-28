import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from app.mixin.soft_delete import SoftDeleteMixin

class User(Base, SoftDeleteMixin):
    __tablename__ = 'user'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    is_email_verified = Column(Boolean, default=False)
    phone = Column(String(20), unique=True, nullable=True)
    is_phone_verified = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String(100))
    full_name = Column(String(100), nullable=True)
    cpf = Column(String(11), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    # Relationships
    addresses = relationship("Address", back_populates="user")
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, default=1)
    role = relationship("Role", back_populates="users")
    activation_tokens = relationship("ActivationToken", back_populates="user")