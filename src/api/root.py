
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    logger.debug("Hello")
    return {"message": "Hello"}
