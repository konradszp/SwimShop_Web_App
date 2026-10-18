from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
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
    category_id: int
    category_name: Optional[str] = None
    name: str
    brand: str
    price: float
    stock_quantity: int
    min_stock_level: Optional[int] = None
    size: str | None = None
    description: str | None = None
    low_stock: bool = False
    out_of_stock: bool = False

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProductResponse])
def get_all_products():
    products = product_repository.get_all()
    return products

@router.get("/search", response_model=List[ProductResponse])
def search_products(q: str = Query(..., min_length=1)):
    products = product_repository.search(q)
    return products

@router.get("/category/{category_id}", response_model=List[ProductResponse])
def get_by_category(category_id: int):
    products = product_repository.get_by_category(category_id)
    return products

@router.get("/low-stock", response_model=List[ProductResponse])
def get_low_stock_products():
    products = product_repository.get_all()
    result = []

    for product in products:
        if product.low_stock or product.out_of_stock:
            result.append(product)

    return result

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):

    product = product_repository.get_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
