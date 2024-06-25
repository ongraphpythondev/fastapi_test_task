from fastapi.testclient import TestClient
from fastapi import Depends
from custom_function import get_db
import pytest
from Product.apis import product_app
from sqlalchemy.orm import Session

@pytest.fixture
def test_client() -> TestClient:
  with TestClient(product_app) as client:
    yield client

async def test_get_all_products(test_client: TestClient, db: Session= Depends(get_db)):
    """
    Retrieves all products from the database.

    This function queries the database for all `Product` records and returns them in the response body.

    Args:
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON list containing all product data.
    """
    response = await test_client.get("/")
    assert response.status_code == 200


async def test_create_product_valid_data(test_client: TestClient, db: Session= Depends(get_db)):
    """
    Creates a new product in the database with valid data.

    This function takes a JSON object representing product data (`ProductCreate`) and adds a new product record to the database.

    Args:
        product: A JSON object containing product data (name, description, price, supplier_id, stock, warehouse_id).
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON object containing the newly created product details.

    Raises:
        HTTPException: If there's an error creating the product.
    """
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 10.99,
        "supplier_id": 1,
        "stock": 10,
        "warehouse_id": 1,
    }
    response = await test_client.post("/", json=product_data)
    assert response.status_code == 200


async def test_create_product_invalid_data(test_client: TestClient):
    """
    Creates a new product in the database with invalid data.

    This function takes a JSON object representing product data (`ProductCreate`) and adds a new product record to the database.

    Args:
        product: A JSON object containing product data (name, description, price, supplier_id, stock, warehouse_id).
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        Error message for "Unprocessable entity" with code 422.
    """
    product_data = {
        "description": "This is a test product",
        "price": 10.99,
    }
    response = await test_client.post("/", json=product_data)
    assert response.status_code == 422


async def test_get_product_by_id_existent(test_client: TestClient, db: Session= Depends(get_db)):
    """
    Retrieves a product by its ID which Exists.

    This function queries the database for a specific product based on the provided `product_id`.

    Args:
        product_id: The ID of the product to retrieve.
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON object containing the product data if found, or an error message if not found.

    Raises:
        HTTPException: If the product with the provided ID is not found.
    """
    product_id = 1
    response = await test_client.get(f"/{product_id}")
    assert response.status_code == 200


async def test_get_product_by_id_nonexistent(test_client: TestClient):
    """
    Retrieves a product by its ID which doesn't exists with in the database.

    This function queries the database for a specific product based on the provided `product_id`.

    Args:
        product_id: The ID of the product to retrieve.
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON object containing the product data if found, or an error message if not found.

    Raises:
        HTTPException: If the product with the provided ID is not found.
    """
    response = await test_client.get("/2")
    assert response.status_code == 404


async def test_update_product_valid_data(test_client: TestClient, db: Session= Depends(get_db)):
    """
    Updates an existing product in the database with valid data.

    This function takes an optional JSON object representing product updates (`ProductCreate`) and modifies the corresponding product record in the database.

    Args:
        product_id: The ID of the product to update.
        product_update: A JSON object containing updated product data (optional).
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating successful update.

    Raises:
        HTTPException: If the product with the provided ID is not found.
    """
    product_id = 1
    update_data = {"description": "Updated description"}
    response = await test_client.put(f"/{product_id}", json=update_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Updated"}


async def test_update_product_nonexistent(test_client: TestClient):
    """
    Updates an existing product in the database which doesn't Exists.

    This function takes an optional JSON object representing product updates (`ProductCreate`) and modifies the corresponding product record in the database.

    Args:
        product_id: The ID of the product to update.
        product_update: A JSON object containing updated product data (optional).
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating Product not found.

    Raises:
        HTTPException: If the product with the provided ID is not found.
    """
    update_data = {"description": "Updated description"}
    response = await test_client.put("/2", json=update_data)
    assert response.status_code == 404


async def test_delete_product_existent(test_client: TestClient, db: Session= Depends(get_db)):
    """
    Deletes a product from the database which exists.

    This function removes a product record from the database based on the provided `product_id`.

    Args:
        product_id: The ID of the product to delete.
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating successful deletion.

    Raises:
        HTTPException: If the product with the provided ID is not found.
    """
    product_id = 1
    response = await test_client.delete(f"/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}


async def test_delete_product_nonexistent(test_client: TestClient):
    """
    Deletes a product from the database which doesn't exists.

    This function removes a product record from the database based on the provided `product_id`.

    Args:
        product_id: The ID of the product to delete.
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating Product not found.

    Raises:
        HTTPException: If the product with the provided ID is not found.
    """
    response = await test_client.delete("/2")
    assert response.status_code == 404
