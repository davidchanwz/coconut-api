# app/models.py

from pydantic import BaseModel, Field
from typing import List

class ReceiptRequest(BaseModel):
    text: str = Field(..., example="Chicken Rice 5.50\nFries 3.50\nDrink 2.00")

class ReceiptItem(BaseModel):
    item: str
    amount: float

class ReceiptResponse(BaseModel):
    items: List[ReceiptItem]