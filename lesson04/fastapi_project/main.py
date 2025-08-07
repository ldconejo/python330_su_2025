# main.py

from fastapi import FastAPI

# Pydantic imports
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to our store full of wonderful products!"}

@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int):
    return {"product_id": product_id}

# Pydantic model for product
class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool

@app.post("/products")
async def create_product(product: Product):
    return product