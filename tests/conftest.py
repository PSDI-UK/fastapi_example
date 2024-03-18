from collections.abc import AsyncGenerator

import pytest_asyncio
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from src.main import app


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator:
    """
    Fixture that provides a TestClient for each test, using a mock database. The mock database is
    destroyed after each test.
    """
    database_connection = AsyncMongoMockClient()
    app.state.db = database_connection["testdatabase"]
    with TestClient(app) as client:
        yield client
    database_connection.close()
    app.state.db = None
