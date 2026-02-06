from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class OrderStatus(str, enum.Enum):
    draft = 'draft'
    submitted = 'submitted'
    fulfilled = 'fulfilled'
    cancelled = 'cancelled'

class Branch(Base):
    __tablename__ = 'services_branches'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    location = Column(String(120), nullable=False)
    timezone = Column(String(64), nullable=False, default='UTC')

class Item(Base):
    __tablename__ = 'services_items'
    id = Column(Integer, primary_key=True)
    sku = Column(String(64), unique=True, nullable=False)
    name = Column(String(120), nullable=False)
    description = Column(String(255))
    unit = Column(String(32), nullable=False)
    min_stock_level = Column(Integer, nullable=False, default=0)

class Stock(Base):
    __tablename__ = 'services_stock'
    branch_id = Column(Integer, ForeignKey('services_branches.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('services_items.id'), primary_key=True)
    quantity = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Order(Base):
    __tablename__ = 'services_orders'
    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, ForeignKey('services_branches.id'), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.draft)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OrderLine(Base):
    __tablename__ = 'services_order_lines'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('services_orders.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('services_items.id'), nullable=False)
    requested_qty = Column(Integer, nullable=False)
    fulfilled_qty = Column(Integer, nullable=False, default=0)
    __table_args__ = (UniqueConstraint('order_id', 'item_id', name='uq_order_item'),)

class AuditLog(Base):
    __tablename__ = 'services_audit_logs'
    id = Column(Integer, primary_key=True)
    actor_user_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(50), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ip = Column(String(64))
    details = Column(JSON, nullable=False, default={})
