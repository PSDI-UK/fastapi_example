from fastapi.testclient import TestClient

from src.api.product.models import Product


async def test_get_product(client: TestClient) -> None:
    """
    A test to check the get product endpoint returns the correct hardcoded product
    """
    response = client.get("/product")

    assert response.status_code == 200
    assert response.json() == Product(quantity=1).model_dump(mode='json')