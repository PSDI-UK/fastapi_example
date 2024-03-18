import logging
from typing import List

from fastapi import APIRouter

from src.api.product.models import Product

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/product",
    tags=["Products"],
)


@router.get(
    "/",
    response_description="Return an example product",
    response_model=Product,
)
async def get_product() -> List[Product]:
    return Product(quantity=1)
