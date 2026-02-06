import enum
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, JSON, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class OrderStatus(str, enum.Enum):
    draft = 'draft'
    submitted = 'submitted'
    fulfilled = 'fulfilled'
    cancelled = 'cancelled'


class Branch(Base):
    __tablename__ = 'services_branches'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    location: Mapped[str] = mapped_column(String(255))
    timezone: Mapped[str] = mapped_column(String(64))


class Item(Base):
    __tablename__ = 'services_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(500), default='')
    unit: Mapped[str] = mapped_column(String(16), default='pcs')
    min_stock_level: Mapped[int] = mapped_column(Integer, default=0)


class Stock(Base):
    __tablename__ = 'services_stock'
    __table_args__ = (UniqueConstraint('branch_id', 'item_id'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey('services_branches.id'))
    item_id: Mapped[int] = mapped_column(ForeignKey('services_items.id'))
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Order(Base):
    __tablename__ = 'services_orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey('services_branches.id'))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.draft)
    created_by: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    lines = relationship('OrderLine', back_populates='order', cascade='all, delete-orphan')


class OrderLine(Base):
    __tablename__ = 'services_order_lines'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('services_orders.id'))
    item_id: Mapped[int] = mapped_column(ForeignKey('services_items.id'))
    requested_qty: Mapped[int] = mapped_column(Integer)
    fulfilled_qty: Mapped[int] = mapped_column(Integer, default=0)
    order = relationship('Order', back_populates='lines')


class AuditLog(Base):
    __tablename__ = 'services_audit_logs'
    id: Mapped[int] = mapped_column(primary_key=True)
    actor_user_id: Mapped[int] = mapped_column(Integer)
    action: Mapped[str] = mapped_column(String(120))
    entity_type: Mapped[str] = mapped_column(String(120))
    entity_id: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ip: Mapped[str] = mapped_column(String(64), default='unknown')
    details: Mapped[dict] = mapped_column(JSON, default={})
