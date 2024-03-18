from datetime import datetime
import time

from fastapi.testclient import TestClient

from src.utils.common_models import PyObjectId
from src.api.item.models import Item, ItemNew, ItemUpdate


async def test_get_item(client: TestClient) -> None:
    """
    Manually create a new Item in the database and then test the get item endpoint to ensure it
    returns the item.
    """
    test_item = Item(
        _id=PyObjectId(),   # unused but mandatory field
        name="Test Item",
        type="Test Type",
        created_time=datetime.utcnow(),
        updated_time=datetime.utcnow()
    )
    # Manually insert a test item into the database
    result = await client.app.state.db["itemcollection"].insert_one(test_item.model_dump(exclude={"id"}))

    # Query MongoDB to find the item we just created
    created_item = Item(**await client.app.state.db["itemcollection"].find_one({"_id": result.inserted_id}))

    # Test the get item endpoint and check it correctly returns the item we just inserted
    response = client.get(f"/item/{result.inserted_id}")

    assert response.status_code == 200
    assert response.json() == created_item.model_dump(mode='json')


async def test_get_items(client: TestClient) -> None:
    """
    Manually create a list of new Items in the database and then test the get item endpoint to
    ensure it returns the item.
    """
    test_item1 = Item(
        _id=PyObjectId(),
        name="Test Item 1",
        type="Test Type 1",
        created_time=datetime.utcnow(),
        updated_time=datetime.utcnow()
    )
    test_item2 = Item(
        _id=PyObjectId(),
        name="Test Item 2",
        type="Test Type 2",
        created_time=datetime.utcnow(),
        updated_time=datetime.utcnow()
    )

    # Manually insert test items into the database
    result1 = await client.app.state.db["itemcollection"].insert_one(test_item1.model_dump(exclude={"id"}))
    result2 = await client.app.state.db["itemcollection"].insert_one(test_item2.model_dump(exclude={"id"}))

    # Query MongoDB to get the items we just created
    created_item1 = Item(**await client.app.state.db["itemcollection"].find_one({"_id": result1.inserted_id}))
    created_item2 = Item(**await client.app.state.db["itemcollection"].find_one({"_id": result2.inserted_id}))

    # Test the get item endpoint and check it correctly returns a list of Items
    response = client.get("/item/")

    assert response.status_code == 200
    assert response.json() == [created_item1.model_dump(mode='json'), created_item2.model_dump(mode='json')]


async def test_get_item_not_found(client: TestClient) -> None:
    """
    Test the get item endpoint with a random id to ensure it returns a message when the item is not
    found.
    """
    item_id = PyObjectId()
    response = client.get(f"/item/{item_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Item {item_id} not found"}


async def test_delete_item(client: TestClient):
    """
    Manually create a new Item in the database and then test the delete item endpoint to ensure it
    deletes the item successfully.
    """
    test_item = Item(
        _id=PyObjectId(),
        name="Test Item",
        type="Test Type",
        created_time=datetime.utcnow(),
        updated_time=datetime.utcnow()
    )
    # Manually insert a test item into the database
    result = await client.app.state.db["itemcollection"].insert_one(test_item.model_dump(exclude={"id"}))

    # Delete the test item
    response = client.delete(f"/item/{result.inserted_id}")

    # A search for the item should return None
    deleted_item = await client.app.state.db["itemcollection"].find_one({"_id": result.inserted_id})

    assert response.status_code == 200
    assert deleted_item is None


async def test_delete_item_not_found(client: TestClient) -> None:
    """
    Test the delete item endpoint to ensure it returns a message when the item is not found.
    """
    item_id = PyObjectId()
    response = client.delete(f"/item/{item_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Item {item_id} not found"}


async def test_create_item(client: TestClient) -> None:
    """
    Test the create item endpoint to ensure it creates the item successfully.
    """
    test_item = ItemNew(
        name="Test Item",
        type="Test Type"
    )
    response = client.post("/item", json=test_item.model_dump(mode='json'))

    # Query MongoDB to find the item we just created
    item_id = PyObjectId(response.json()["id"])
    created_item = Item(**await client.app.state.db["itemcollection"].find_one({"_id": item_id}))

    # Check the response matches the item we just read from the database
    assert response.status_code == 200
    assert response.json() == created_item.model_dump(mode='json')

    # Check the response matches fields in the original ItemNew model we created
    assert response.json()["name"] == test_item.name
    assert response.json()["type"] == test_item.type


async def test_update_item(client: TestClient) -> None:
    """
    Test the update item endpoint to ensure it updates the item successfully.
    """
    test_item = Item(
        _id=PyObjectId(),
        name="Test Item",
        type="Test Type",
        created_time=datetime.utcnow(),
        updated_time=datetime.utcnow()
    )
    # Manually insert a test item into the database
    result = await client.app.state.db["itemcollection"].insert_one(test_item.model_dump(exclude_none=True))

    # We have to pause for a moment to ensure the updated_time timestamp is different between
    # test_item and update
    time.sleep(0.05)

    # Update the name of the item
    update = ItemUpdate(name="Updated Item Name")

    # Update the item
    response = client.put(f"/item/{result.inserted_id}", json=update.model_dump(mode='json'))

    # Query MongoDB to find the item we just updated
    item_id = PyObjectId(response.json()["id"])
    updated_item = Item(**await client.app.state.db["itemcollection"].find_one({"_id": item_id}))

    # Check updated_time timestamp in updated_item is different to the initial test_item timestamp
    assert test_item.updated_time != updated_item.updated_time

    # Check the response matches the updated item
    assert response.status_code == 200
    assert response.json() == updated_item.model_dump(mode='json')


async def test_update_item_not_found(client: TestClient) -> None:
    """
    Test the update item endpoint to ensure it returns a message when the item is not found.
    """
    item_id = PyObjectId()
    update = ItemUpdate(name="Updated Item Name")
    response = client.put(f"/item/{item_id}", json=update.model_dump(mode='json'))

    assert response.status_code == 404
    assert response.json() == {"detail": f"Item {item_id} not found"}
