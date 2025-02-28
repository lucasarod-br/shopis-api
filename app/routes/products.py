from fastapi import APIRouter, Depends
from app.database import SessionDep
from app.auth.auth import oauth2_scheme
from app.catalog import product
from app.schemas.product import ProductCreate, ProductResponse
from fastapi import APIRouter, Depends

router = APIRouter(
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: SessionDep):
    return product.create_product(db=db, product=product)

@router.get("/products/", response_model=list[ProductResume])
def read_products(db: SessionDep, skip: int = 0, limit: int = 10):
    return product.get_products(db=db, skip=skip, limit=limit)

@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: SessionDep):
    return product.get_product(db=db, product_id=product_id)

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: SessionDep):
    return product.update_product(db=db, product_id=product_id, product=product)

@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: SessionDep):
    return product.delete_product(db=db, product_id=product_id)