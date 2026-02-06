from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Order, OrderLine, OrderStatus
from app.schemas.domain import OrderIn
from app.core.security import require_roles, get_current_user
from app.services.order_service import fulfill_order

router = APIRouter(prefix='/orders', tags=['orders'])

@router.get('', dependencies=[Depends(require_roles('Admin', 'Manager', 'Worker'))])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@router.get('/recent', dependencies=[Depends(require_roles('Admin', 'Manager', 'Worker'))])
def recent_orders(db: Session = Depends(get_db)):
    return db.query(Order).order_by(Order.created_at.desc()).limit(10).all()

@router.get('/{order_id}', dependencies=[Depends(require_roles('Admin', 'Manager', 'Worker'))])
def get_order(order_id: int, db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if not o: raise HTTPException(404, 'Order not found')
    lines = db.query(OrderLine).filter_by(order_id=order_id).all()
    return {'order': o, 'lines': lines}

@router.post('', dependencies=[Depends(require_roles('Admin', 'Manager', 'Worker'))])
def create_order(payload: OrderIn, user=Depends(get_current_user), db: Session = Depends(get_db)):
    o = Order(branch_id=payload.branch_id, created_by=int(user['sub']), status=OrderStatus.draft)
    db.add(o); db.flush()
    for line in payload.lines:
        db.add(OrderLine(order_id=o.id, item_id=line.item_id, requested_qty=line.requested_qty, fulfilled_qty=0))
    db.commit(); db.refresh(o)
    return o

@router.put('/{order_id}', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def update_order(order_id: int, payload: OrderIn, db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if not o: raise HTTPException(404, 'Order not found')
    if o.status != OrderStatus.draft: raise HTTPException(400, 'Only draft orders can be updated')
    o.branch_id = payload.branch_id
    db.query(OrderLine).filter_by(order_id=order_id).delete()
    for line in payload.lines:
        db.add(OrderLine(order_id=order_id, item_id=line.item_id, requested_qty=line.requested_qty, fulfilled_qty=0))
    db.commit(); return {'status':'updated'}

@router.delete('/{order_id}', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def delete_order(order_id: int, db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if not o: raise HTTPException(404, 'Order not found')
    db.query(OrderLine).filter_by(order_id=order_id).delete()
    db.delete(o); db.commit(); return {'status':'deleted'}

@router.post('/{order_id}/submit', dependencies=[Depends(require_roles('Admin', 'Manager', 'Worker'))])
def submit_order(order_id: int, db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if not o: raise HTTPException(404, 'Order not found')
    o.status = OrderStatus.submitted
    db.commit()
    return {'status': 'submitted'}

@router.post('/{order_id}/fulfill', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def fulfill(order_id: int, request: Request, override_negative: bool = False, user=Depends(get_current_user), db: Session = Depends(get_db)):
    fulfilled = fulfill_order(db, order_id, int(user['sub']), request.client.host, override_negative)
    return {'status': fulfilled.status}
