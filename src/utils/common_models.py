from typing import Any, Dict
from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    """
    Custom field type for the bson ObjectId. Provides validation and support for ObjectId in
    Pydantic models and FastAPI routes.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return cls(v)

    @classmethod
    def __get_pydantic_json_schema__(self, schema, handler):  # pragma: no cover
        field_schema = {
            "type": "string",
            "format": "string",
            "description": "A special type used by MongoDB as the primary key for the documents in a collection."
        }
        return field_schema


class IdMixin(BaseModel):
    """
    A mixin for models that requires an 'id' field. It handles the translation between the MongoDB
    '_id' field and the model's 'id' field. Models populated from MongoDB queries should use this
    mixin.
    """
    id: str = Field(...)

    def __init__(self, **data: Dict[str, Any]):
        # check if an '_id' field is present, convert it to a string named 'id'
        if '_id' in data:
            _id = data.pop('_id')
            if isinstance(_id, ObjectId):
                data['id'] = str(_id)
            else:
                raise ValueError("_id must be an instance of PyObjectId")
        # id should be a string that is a valid ObjectId representation
        if not ObjectId.is_valid(data["id"]):
            raise ValueError("_id must be an instance of PyObjectId")
        super().__init__(**data)


class MessageResponse(BaseModel):
    detail: str
