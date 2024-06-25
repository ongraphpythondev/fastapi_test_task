from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from Product.models import Product
from custom_function import get_db

from .schema import OrderCreate, StatusUpdate
from .models import Order

order_app = APIRouter()

@order_app.get("/")
async def get_all_orders(db: Session = Depends(get_db)):
    """
    Retrieving all orders

    Args:
        db: A database session dependency (fixture) for database access.
    
    Returns:
         A list of JSON objects containing the order data else en empty list.
    """
    orders = db.query(Order).all()
    return orders


@order_app.post("/")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Creating an order.

    Args:
        orders: A JSON object of (`OrderCreate`) schema.
        db: A database session dependency (fixture) for database access.

    Returns:
            A JSON of new created order data.
    """
    if order.status not in ("pending", "fulfilled", "cancelled"):
        return {"message": 'pick status from these ("pending", "fulfilled", "cancelled")'}

    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order) 
    return new_order


@order_app.get("/{order_id}")
async def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieving an order by its ID.

    Args:
        order_id: An ID for which the order has to be search.
        db: A database session dependency (fixture) for database access.
    
    Returns:
             A JSON object containing the order data if found, or an error message if not found.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        return {"message": "Order not found"}
    return order


@order_app.put("/{order_id}")
async def update_product(order_id: int, order_update: OrderCreate = None, db: Session = Depends(get_db)):
    """
    Updates an existing order in the database.

    This function takes an optional JSON object representing order updates (`OrderCreate`) and modifies the corresponding order record in the database.

    Args:
        order_id: The ID of the order to update.
        order_update: A JSON object containing updated order data (optional).
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating successful update.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order_update:
        for field, value in order_update.dict().items():
            if value is not None:
                setattr(order, field, value)

    db.commit()
    return {"message": 'Updated'}


@order_app.delete("/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    """
    Deletes a order from the database.

    This function removes a order record from the database based on the provided `order_id`.

    Args:
        order_id: The ID of the order to delete.
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating successful deletion.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order deleted successfully"}


@order_app.patch("/{order_id}/status")
async def update_order_status(order_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    """
    Updating order status with a valid status.

    Args:
        order_id: An Integer if order id for which we have to change the stock
        db: A database session dependency (fixture) for database access.
    """
    if status_update.status not in ("pending", "fulfilled", "cancelled"):
        return {"message": 'Choose status from these "pending", "fulfilled", "cancelled" '}
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    order.status = status_update.status
    db.commit()
    return {"message": "ORder status updated successfully"}


@order_app.get("/{order_id}/items")
async def get_order_items(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the order items associated with a specific order.

    Args:
        order_id: The ID of the order to retrieve items for.
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A list of order items, potentially including product details.

    Raises:
        HTTPException: If the order with the provided ID is not found.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    order_items = order.order_items

    if Product:
        for item in order_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            item.product = product

    return order_items
