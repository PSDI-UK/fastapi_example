from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.utils.common_models import IdMixin


class Item(IdMixin, BaseModel):
    """
    Represents an item returned from the database. Uses IdMixin to handle the id field
    automatically.
    """
    created_time: datetime = Field(...)
    updated_time: datetime = Field(...)
    name: str = Field(...)
    type: str = Field(...)


class ItemNew(BaseModel):
    """
    Model for creating a new item.
    """
    name: str = Field(...)
    type: str = Field(...)


class ItemUpdate(BaseModel):
    """
    Model for updating an existing item.
    """
    name: Optional[str] = None
    type: Optional[str] = None
