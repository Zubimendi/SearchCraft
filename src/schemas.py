from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    brand: str
    attributes: Optional[Dict[str, Any]] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

class ProductOut(ProductBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    hits: List[Dict[str, Any]]
    total: int
    page: int
    per_page: int
    facets: Dict[str, Dict[str, int]]  # field -> value -> count
