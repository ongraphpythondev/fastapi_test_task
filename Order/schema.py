from pydantic import BaseModel
from datetime import datetime

class StatusUpdate(BaseModel):
    status: int


class OrderCreate(BaseModel):
    customer_name: str
    customer_address: str
    order_date: datetime
    status: str
