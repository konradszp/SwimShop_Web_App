from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import products, categories, customers, orders

app = FastAPI(
    title="SwimShop API",
    description="POS & Inventory Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(customers.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "SwimShop API is running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}