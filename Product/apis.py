from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from Supplier.models import Supplier
from custom_function import get_db

from .schema import ProductCreate, StockUpdate
from .models import Product

product_app = APIRouter()

@product_app.get("/")
async def get_all_products(db: Session = Depends(get_db)):
    """
    Retrieving all products

    Args:
        db: A database session dependency (fixture) for database access.
    
    Returns:
         A list of JSON objects containing the product data else en empty list.
    """
    products = db.query(Product).all()
    return products


@product_app.post("/")
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Creating an product.

    Args:
        product: A JSON object of (`ProductCreate`) schema.
        db: A database session dependency (fixture) for database access.

    Returns:
            A JSON of new created product data.
    """
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)  # Refresh to get the generated ID
    return new_product


@product_app.get("/{product_id}")
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieving an product by its ID.

    Args:
        product_id: An ID for which the product has to be search.
        db: A database session dependency (fixture) for database access.
    
    Returns:
             A JSON object containing the product data if found, or an error message if not found.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return {"message": "Product not found"}  # Handle non-existent product
    return product


@product_app.put("/{product_id}")
async def update_product(product_id: int, product_update: ProductCreate = None, db: Session = Depends(get_db)):
    """
    Updates an existing product in the database.

    This function takes an optional JSON object representing product updates (`ProductCreate`) and modifies the corresponding product record in the database.

    Args:
        product_id: The ID of the product to update.
        product_update: A JSON object containing updated product data (optional).
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating successful update.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product_update:
        for field, value in product_update.dict().items():
            if value is not None:
                setattr(product, field, value)
    db.commit()
    return {"message": 'Updated'}


@product_app.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Deletes a product from the database.

    This function removes a product record from the database based on the provided `product_id`.

    Args:
        product_id: The ID of the product to delete.
        db: A database session dependency injected using `Depends(get_db)`.

    Returns:
        A JSON message indicating successful deletion.
    """
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}


@product_app.get("/search/")
async def search_products(name: str = None, supplier_name: str = None, db: Session = Depends(get_db)):
    """
    Search product with name and supplier_name.

    Args:
        name: Product Name for which have to search
        supplier_name: Supplier name related to product
        db: A database session dependency (fixture) for database access.

    Returns:
        A JSON response if product found else a message with not found.
    """
    query = db.query(Product)
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))

    if supplier_name:
        supplier_id = db.query(Supplier).filter(Supplier.name == supplier_name).first()
        if supplier_id:
            query = query.filter(Product.supplier_id == supplier_id.id)
        else:
            return []

    products = query.all()
    return products

@product_app.patch("/{product_id}/stock")
async def update_product_stock(product_id: int, stock_update: StockUpdate, db: Session = Depends(get_db)):
    """
    Updating product stock with a valid status.

    Args:
        product_id: An Integer if product id for which we have to change the stock
        db: A database session dependency (fixture) for database access.

    Returns:
        A JSON message indicating stock is updated or not.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    product.stock = stock_update.stock
    db.commit()
    return {"message": "Product stock updated successfully"}
