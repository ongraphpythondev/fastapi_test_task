from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str = None
    price: float
    supplier_id: int
    stock: int
    warehouse_id: int


class StockUpdate(BaseModel):
    stock: int
