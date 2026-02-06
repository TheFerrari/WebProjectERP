from pydantic import BaseModel
from typing import Optional, List

class BranchIn(BaseModel):
    name: str
    location: str
    timezone: str = 'UTC'

class BranchOut(BranchIn):
    id: int
    class Config:
        from_attributes = True

class ItemIn(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    unit: str
    min_stock_level: int = 0

class ItemOut(ItemIn):
    id: int
    class Config:
        from_attributes = True

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
