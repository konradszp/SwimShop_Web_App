from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

from app.repositories.category import CategoryRepository

from fastapi import Depends
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

category_repository = CategoryRepository()

class CategoryResponse(BaseModel):
    category_id: int
    name: str

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str

@router.get("/", response_model=List[CategoryResponse])
def get_all_categories():
    return category_repository.get_all()

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int):
    category = category_repository.get_by_id(category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category

@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, current_user: User = Depends(get_current_user)):
    success = category_repository.create(category.name)

    if not success:
        raise HTTPException(status_code=400, detail="Could not create category")

    categories = category_repository.get_all()
    for c in categories:
        if c.name == category.name:
            return c

    raise HTTPException(status_code=500, detail="Category created but could not be retrieved")

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryCreate, current_user: User = Depends(get_current_user)):
    existing = category_repository.get_by_id(category_id)

    if not existing:
        raise HTTPException(status_code=404, detail="Category not found")

    success = category_repository.update(category_id, category.name)

    if not success:
        raise HTTPException(status_code=400, detail="Could not update category")

    return category_repository.get_by_id(category_id)

@router.delete("/{category_id}")
def delete_category(category_id: int, current_user: User = Depends(get_current_user)):
    existing = category_repository.get_by_id(category_id)

    if not existing:
        raise HTTPException(status_code=404, detail="Category not found")

    success = category_repository.delete(category_id)

    if not success:
        raise HTTPException(status_code=400, detail="Could not delete Category")

    return {"message": "Category deleted"}