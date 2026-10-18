from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

from app.repositories.product import ProductRepository
from app.models.product import Product

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

product_repository = ProductRepository()

class ProductResponse(BaseModel):
    product_id: int
    name: str
    brand: str
    price: float
    stock_quantity: int
    category_name: str | None = None
    size: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProductResponse])
def get_all_products():

    products = product_repository.get_all()

    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):

    products = product_repository.get_all()

    product = None
    for p in products:
        if p.product_id == product_id:
            product = p
            break

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product