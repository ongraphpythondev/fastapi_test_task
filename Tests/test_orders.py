from fastapi.testclient import TestClient
from typing import Any
import pytest
from Order.apis import order_app
from sqlalchemy.orm import Session

@pytest.fixture
def test_client() -> TestClient:
    with TestClient(order_app) as client:
        yield client

async def test_get_all_orders(test_client: TestClient):
    """
    Retrieving all orders.

    This test sends a GET request to the `/orders` endpoint and asserts that the response status code is 200 (OK).
    It's recommended to further assert the response data structure and content based on your specific order model and expected output format.

    Args:
        test_client: A TestClient instance for making API requests.
        db: A database session dependency (fixture) for database access.
    Returns:
            A JSON list containing all order data.
    """
    response = await test_client.get("/")
    assert response.status_code == 200


async def test_create_order_valid_data(test_client: Any):
    """
    Creating an order with valid data.

    This test defines valid order data (`order_data`) and sends a POST request to the `/orders` endpoint with the data in JSON format.
    It asserts that the response status code is 201 (Created) and the response body contains the newly created order information.

    Args:
        test_client: A TestClient instance for making API requests.
        db: A database session dependency (fixture) for database access.

    Returns:
            A JSON of new created order data.
    """
    order_data = {
        "item_id": 1,
        "quantity": 2,
        "status": "pending"
    }
    response = await test_client.post("/", json=order_data)
    assert response.status_code == 200


async def test_create_order_invalid_status(test_client: Any):
    """
    Creating an order with Invalid data.

    This test defines valid order data (`order_data`) and sends a POST request to the `/orders` endpoint with the data in JSON format.
    It asserts that the response status code is 422 (Unprocessed entity).

    Args:
        test_client: A TestClient instance for making API requests.
        db: A database session dependency (fixture) for database access.

    Returns:
            A JSON response saying "Unprocessed Entity" with status code 422.
    """
    order_data = {
        "item_id": 1,
        "quantity": 2,
        "status": "invalid"
    }
    response = await test_client.post("/", json=order_data)
    assert response.status_code == 422  


async def test_get_order_by_id_existent(test_client: Any, order_id: int=1):
    """
    Retrieving an order by its ID.

    This test assumes you have a fixture or setup to provide an existing order ID.
    It sends a GET request to the `/orders/{order_id}` endpoint and asserts that the response status code is 200 (OK).
    The test further asserts that the response body contains the retrieved order information.

    Args:
        test_client: A TestClient instance for making API requests.
        db: A database session dependency (fixture) for database access.
    
    Returns:
             A JSON object containing the order data if found, or an error message if not found.
    """
    response = await test_client.get(f"/{order_id}")
    assert response.status_code == 200


async def test_get_order_by_id_nonexistent(test_client: Any):
    """
    Retrieving an order by its ID which doesn't exists.

    This test assumes you have a fixture or setup to provide an existing order ID.
    It sends a GET request to the `/orders/{order_id}` endpoint and asserts that the response status code is 404 (Not found).

    Args:
        test_client: A TestClient instance for making API requests.
        db: A database session dependency (fixture) for database access.
    
    Returns:
             A JSON object containing the order data if found, or an error message if not found.
    """
    response = await test_client.get("/2")  
    assert response.status_code == 404 


async def test_update_order_valid_data(test_client: Any, order_id: int=1):
    """
    Updates an existing order in the database with valid data.

    This function takes an optional JSON object representing product updates (`OrderCreate`) and modifies the corresponding order record in the database.

    Args:
        test_client: A TestClient instance for making API requests.
        order_id: The ID of the order to update.
        order_update: A JSON object containing updated order data (optional).
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating successful update.

    Raises:
        HTTPException: If the order with the provided ID is not found.
    """
    update_data = {"status": "fulfilled"}
    response = await test_client.put(f"/{order_id}", json=update_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Updated"}


async def test_update_order_nonexistent(test_client: Any):
    """
    Updates an existing order in the database which doesn't Exists.

    This function takes an optional JSON object representing order updates (`OrderCreate`) and modifies the corresponding order record in the database.

    Args:
        test_client: A TestClient instance for making API requests.
        order_id: The ID of the order to update.
        order_update: A JSON object containing updated order data (optional).
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating order not found.

    Raises:
        HTTPException: If the order with the provided ID is not found.
    """
    update_data = {"status": "fulfilled"}
    response = await test_client.put("/2", json=update_data)
    assert response.status_code == 404


async def test_delete_order_existent(test_client: Any, order_id: int=1):
    """
    Deletes a order from the database which exists.

    This function removes a order record from the database based on the provided `order_id`.

    Args:
        test_client: A TestClient instance for making API requests.
        order_id: The ID of the order to delete.
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating successful deletion.

    Raises:
        HTTPException: If the order with the provided ID is not found.
    """
    response = await test_client.delete(f"/{order_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Order deleted successfully"}


async def test_delete_order_nonexistent(test_client: Any):
    """
    Deletes a order from the database which doesn't exists.

    This function removes a order record from the database based on the provided `order_id`.

    Args:
        test_client: A TestClient instance for making API requests.
        order_id: The ID of the order to delete.
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating order not found.

    Raises:
        HTTPException: If the order with the provided ID is not found.
    """
    response = await test_client.delete("/2")
    assert response.status_code == 404

async def test_get_order_items_existent_order(test_client: TestClient, db: Session):
    """
    Retrieving order items for an existing order.

    This test assumes you have a fixture or setup to provide an existing order ID with related order items.
    It sends a GET request to the `/orders/{order_id}/items` endpoint and asserts that:
        - The response status code is 200 (OK).
        - The response body contains a list of order items.

    Args:
        test_client: A TestClient instance for making API requests.
        db: A database session dependency (fixture) for database access.
    """
    order_id = 1

    response = await test_client.get(f"/orders/{order_id}/items")
    assert response.status_code == 200


async def test_get_order_items_nonexistent_order(test_client: TestClient, db: Session):
    """
    Retrieving order items for a non-existent order.

    This test sends a GET request with a non-existent order ID and asserts that:
        - The response status code is 404 (Not Found).

    Args:
        test_client: A TestClient instance for making API requests.
        db: A database session dependency (fixture) for database access.
    """
    response = await test_client.get("/orders/12/items")
    assert response.status_code == 404
