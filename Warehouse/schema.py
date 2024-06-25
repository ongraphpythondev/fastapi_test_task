from pydantic import BaseModel

class WareHouseCreate(BaseModel):
    location: str
    capacity: str
