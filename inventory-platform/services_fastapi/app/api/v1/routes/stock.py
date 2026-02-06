from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Stock, Branch, Item, AuditLog
from app.schemas.domain import StockUpdate
from app.core.security import require_roles, get_current_user

router = APIRouter(prefix='/stock', tags=['stock'])

@router.get('', dependencies=[Depends(require_roles('Admin', 'Manager', 'Worker'))])
def list_stock(db: Session = Depends(get_db)):
    return db.query(Stock).all()

@router.get('/summary', dependencies=[Depends(require_roles('Admin', 'Manager', 'Worker'))])
def stock_summary(db: Session = Depends(get_db)):
    rows = db.query(Stock, Branch, Item).join(Branch, Branch.id == Stock.branch_id).join(Item, Item.id == Stock.item_id).all()
    return [{'branch_name': b.name, 'item_name': i.name, 'quantity': s.quantity} for s, b, i in rows]

@router.put('', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def adjust_stock(payload: StockUpdate, request: Request, user=Depends(get_current_user), db: Session = Depends(get_db)):
    stock = db.query(Stock).filter_by(branch_id=payload.branch_id, item_id=payload.item_id).first()
    if not stock:
        stock = Stock(branch_id=payload.branch_id, item_id=payload.item_id, quantity=0)
        db.add(stock)
    if payload.quantity < 0 and not payload.override_negative:
        raise HTTPException(400, 'Negative stock denied')
    stock.quantity = payload.quantity
    db.add(AuditLog(actor_user_id=int(user['sub']), action='stock_adjust', entity_type='Stock', entity_id=f'{payload.branch_id}:{payload.item_id}', ip=request.client.host, details={'new_quantity': payload.quantity}))
    db.commit()
    return {'status': 'ok'}
