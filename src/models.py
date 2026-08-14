from sqlalchemy import Column, String, Float, JSON, Boolean, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    attributes = Column(JSON, nullable=True)   # store extra facets as JSONB
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class OutboxEventType(enum.Enum):
    PRODUCT_CREATED = "product.created"
    PRODUCT_UPDATED = "product.updated"
    PRODUCT_DELETED = "product.deleted"

class Outbox(Base):
    __tablename__ = "outbox"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(Enum(OutboxEventType), nullable=False)
    payload = Column(JSON, nullable=False)   # {"product_id": "...", "data": {...} (optional)}
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    processed_at = Column(DateTime, nullable=True)
