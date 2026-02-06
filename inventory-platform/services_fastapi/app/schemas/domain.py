from pydantic import BaseModel
from typing import Optional, List


class BranchIn(BaseModel):
    name: str
    location: str
    timezone: str = 'UTC'


class ItemIn(BaseModel):
    sku: str
    name: str
    description: str = ''
    unit: str = 'pcs'
    min_stock_level: int = 0


class StockUpdate(BaseModel):
    branch_id: int
    item_id: int
    quantity: int
    override_negative: bool = False


class OrderLineIn(BaseModel):
    item_id: int
    requested_qty: int


class OrderIn(BaseModel):
    branch_id: int
    lines: List[OrderLineIn] = []


class OrderLineOut(BaseModel):
    item_id: int
    requested_qty: int
    fulfilled_qty: int


class OrderOut(BaseModel):
    id: int
    branch_id: int
    status: str
    created_by: int
    lines: List[OrderLineOut]


class AuditOut(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: int
