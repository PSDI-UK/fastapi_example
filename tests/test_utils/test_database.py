from fastapi.testclient import TestClient


async def test_database_connection_issue(client: TestClient) -> None:
    """
    Test the '/item' endpoint when the database connection is not available.
    """
    client.app.state.db = None
    response = client.get("/item")

    assert response.status_code == 500
    assert response.json() == {'detail': 'Database Connection Error'}
