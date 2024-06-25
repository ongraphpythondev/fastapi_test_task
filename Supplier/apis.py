from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from custom_function import get_db

from .schema import SupplierCreate
from .models import Supplier 

supplier_app = APIRouter()

@supplier_app.post("/")
async def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    new_supplier = Supplier(**supplier.dict())
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier
