from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    sku: str
    status: bool
    image_url: Optional[HttpUrl] = None
    category_id: int
    brand_id: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductUpdate(ProductBase):
    pass


class ProductResume(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    image_url: Optional[HttpUrl] = None
    category_id: int
    brand_id: int

    class Config:
        from_attributes = True