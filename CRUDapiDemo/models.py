from typing import Optional

from database import Base
from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel, Field

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price_per_unit = Column(Float)
    base_unit = Column(String)
    stock = Column(Integer)

class ProductRequest(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=50)
    price_per_unit: float = Field(gt=0)
    base_unit: str = Field(min_length=1)
    stock: int = Field(gt=-1)

    class Config:
        json_schema_extra = {
            'example': {
                'name': 'Refigerator',
                'description': 'A cooling device to keep food to live longer',
                'price_per_unit': 58000,
                'base_unit': 'No.',
                'stock': 100
            }
        }


