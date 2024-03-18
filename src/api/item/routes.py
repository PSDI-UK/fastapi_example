from datetime import datetime
import logging
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException

from src.utils.common_models import MessageResponse, PyObjectId
from src.api.item.models import Item, ItemNew, ItemUpdate
from src.utils.database import get_db, MongoDB


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/item",
    tags=["Items"],
)


@router.get(
    "/",
    response_description="List all items",
    response_model=List[Item],
)
async def get_items(db: MongoDB = Depends(get_db)) -> List[Item]:
    result = await db["itemcollection"].find().to_list(100)
    return [Item(**item) for item in result]


@router.get(
    "/{id}",
    response_description="View single item",
    response_model=Item,
    responses={404: {"description": "Item not found", "model": MessageResponse}}
)
async def get_item(id: PyObjectId, db: MongoDB = Depends(get_db)) -> Item:
    logger.debug("Getting item...")
    result = await db["itemcollection"].find_one({"_id": id})
    if result is None:
        raise HTTPException(status_code=404, detail=f"Item {id} not found")
    return Item(**result)


@router.post(
    "/",
    response_description="Create a new item and return it",
    response_model=Item
)
async def create_item(item: ItemNew = Body(...), db: MongoDB = Depends(get_db)) -> Item:
    item_new = item.model_dump(by_alias=True)
    item_new.update({
        "created_time": datetime.utcnow(),
        "updated_time": datetime.utcnow()
    })
    result = await db["itemcollection"].insert_one(item_new)
    created_item = await db["itemcollection"].find_one({"_id": result.inserted_id})
    return Item(**created_item)


@router.put(
    "/{id}",
    response_description="Update an existing item and return it",
    responses={404: {"description": "Item not found", "model": MessageResponse}},
    response_model=Item
)
async def update_item(id: PyObjectId, item: ItemUpdate = Body(...), db: MongoDB = Depends(get_db)) -> Item:
    """
    Update individual fields of an existing item record.
    """
    item_update = item.model_dump(exclude_none=True)
    item_update.update({"updated_time": datetime.utcnow()})

    result = await db["itemcollection"].update_one(
        {"_id": id},
        {"$set": item_update}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Item {id} not found")

    updated_item = await db["itemcollection"].find_one({"_id": id})
    return Item(**updated_item)


@router.delete(
    "/{id}",
    response_description="Delete an existing item",
    responses={404: {"description": "Item not found", "model": MessageResponse}},
    response_model=MessageResponse
)
async def delete_item(id: PyObjectId, db: MongoDB = Depends(get_db)) -> MessageResponse:
    result = await db["itemcollection"].delete_one({"_id": id})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"Item {id} not found")
    return MessageResponse(detail=f"Item {id} deleted successfully")
