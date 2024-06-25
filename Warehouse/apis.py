from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from custom_function import get_db

from .schema import WareHouseCreate
from .models import Warehouse 

warehouse_app = APIRouter()

@warehouse_app.post("/warehouse")
async def create_warehouse(warehouse: WareHouseCreate, db: Session = Depends(get_db)):
    new_warehouse = Warehouse(**warehouse.dict())
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    return new_warehouse
