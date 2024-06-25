from sqlalchemy import Column, Integer, String, ForeignKey, Float
from custom_function import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    price = Column(Float)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    stock = Column(Integer)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
