from sqlalchemy import Column, Integer, String
from custom_function import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    contact_info = Column(String(255))
