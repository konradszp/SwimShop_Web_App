from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel, EmailStr

from app.repositories.customer import CustomerRepository

from fastapi import Depends
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

customer_repository = CustomerRepository()

class CustomerResponse(BaseModel):
    customer_id: int
    full_name: str
    email: str
    phone: str
    address: str

    class Config:
        from_attributes = True

class CustomerCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    address: str

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

@router.get("/", response_model=List[CustomerResponse])
def get_all_customers():
    return customer_repository.get_all()

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int):
    customer = customer_repository.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(customer: CustomerCreate, current_user: User = Depends(get_current_user)):
    customer_id = customer_repository.create(
        full_name=customer.full_name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
    )

    if not customer_id:
        raise HTTPException(status_code=400, detail="Could not create customer")

    new_customer = customer_repository.get_by_id(customer_id)
    if not new_customer:
        raise HTTPException(status_code=500, detail="Customer created but could not be found")

    return new_customer

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerCreate, current_user: User = Depends(get_current_user)):
    existing_customer = customer_repository.get_by_id(customer_id)
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    success = customer_repository.update(
        customer_id=customer_id,
        full_name=customer.full_name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
    )
    if not success:
        raise HTTPException(status_code=400, detail="Could not update customer")

    return customer_repository.get_by_id(customer_id)

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, current_user: User = Depends(get_current_user)):
    existing_customer = customer_repository.get_by_id(customer_id)
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    success = customer_repository.delete(customer_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not delete customer")

    return {"message": "Customer deleted"}