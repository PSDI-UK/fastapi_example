import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError, OperationFailure

from src.utils.settings import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    """
    Manages the lifecycle of the database connection stored in `app.state.db`. The connection is
    established on app start and closed on app stop.
    """
    try:
        logger.info("Connecting to database...")
        client = AsyncIOMotorClient(settings.mongodb_url)
        # Check if the database is available
        await client.get_database().command("ping")
        app.state.db = client.get_database()
        logger.info("Database connection successful")
        yield
    except (ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError, OperationFailure) as e:
        logger.error(f"Error connecting to database: {e}")
        app.state.db = None
        yield
    finally:
        client.close()
        logger.info("Database connection closed")


class MongoDB(AsyncIOMotorDatabase):
    """
    A type hint for MongoDB database objects, subclassing AsyncIOMotorClient. Used with get_db()
    method.
    """
    pass


def get_db(request: Request) -> MongoDB:
    """
    Dependency returning the database connection from `app.state.db`. Raises a 500 error if the
    connection is not established.
    """
    if request.app.state.db is None:
        logging.error("Database Connection Error")
        raise HTTPException(status_code=500, detail="Database Connection Error")
    return request.app.state.db
