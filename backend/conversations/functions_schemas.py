# tools/schemas.py
from pydantic import BaseModel
from typing import Dict

class GetOrdersInput(BaseModel):
    user_id: str

class UpdateProfileInput(BaseModel):
    user_id: str
    data: Dict[str, str]  # Example: {"name": "John", "email": "john@example.com"}

class GetOrderInput(BaseModel):
    order_id: str

class GetProductsInput(BaseModel):
    pass