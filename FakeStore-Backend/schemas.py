from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    product_id: int
    product_name: str
    product_price: float
    quantity: int = 1

class PurchaseCreate(BaseModel):
    items: List[ProductBase]

class PurchaseItemSchema(ProductBase):
    id: int
    purchase_id: int

    class Config:
        orm_mode = True # Enable ORM mode for SQLAlchemy models

class PurchaseSchema(BaseModel):
    id: int
    total_amount: float
    items: List[PurchaseItemSchema] = []

    class Config:
        orm_mode = True