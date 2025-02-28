from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class PhoneResponse(BaseModel):
    id: int
    number: str
    is_verified: bool

class AddressResponse(BaseModel):
    id: int
    street: str
    city: str
    state: str
    postal_code: str
    country: str

class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    cpf: Optional[str] = None
    password: str
    name: str
    full_name: Optional[str] = None
    role_id: Optional[int] = 1

    @field_validator('cpf')
    def cpf_must_have_11_digits(cls, v):
        if len(v) != 11:
            raise ValueError('must have 11 digits')
        return v
    
    @field_validator('phone')
    def phone_must_have_11_digits(cls, v):
        if len(v) != 11:
            raise ValueError('must have 11 digits')
        return v
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    cpf: Optional[str] = None
    full_name: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None

class UserResponse(BaseModel):
    id: UUID
    email: Optional[EmailStr] = None
    is_email_verified: Optional[bool] = None
    phone: Optional[str] = None
    is_phone_verified: Optional[bool] = None
    name: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    addresses: List[AddressResponse] = []

class UserToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: UUID
    name: str
    exp: datetime

