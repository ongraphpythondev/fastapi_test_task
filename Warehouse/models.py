from sqlalchemy import Column, Integer, String
from custom_function import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer)
