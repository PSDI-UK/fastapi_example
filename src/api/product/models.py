from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    quantity: Optional[int] = None
