from fastapi.testclient import TestClient


async def test_get_item(client: TestClient) -> None:
    assert client.get("/").json() == {"message": "Hello"}
