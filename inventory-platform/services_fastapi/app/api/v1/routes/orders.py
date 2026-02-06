from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import Order, OrderLine, Stock, OrderStatus
from app.schemas.domain import OrderIn
from app.core.security import require_roles, get_current_user
from app.services.audit import write_audit

router = APIRouter(prefix='/orders', tags=['orders'])


@router.get('')
def list_orders(db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager', 'Worker'))):
    return db.query(Order).all()


@router.get('/recent')
def recent_orders(db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager', 'Worker'))):
    return db.query(Order).order_by(Order.id.desc()).limit(10).all()


@router.post('')
def create_order(payload: OrderIn, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(require_roles('Admin', 'Manager', 'Worker'))):
    order = Order(branch_id=payload.branch_id, created_by=int(user['sub']))
    for line in payload.lines:
        order.lines.append(OrderLine(item_id=line.item_id, requested_qty=line.requested_qty))
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.post('/{order_id}/submit')
def submit_order(order_id: int, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager'))):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    order.status = OrderStatus.submitted
    db.commit()
    return {'status': 'submitted'}


@router.post('/{order_id}/fulfill')
def fulfill_order(order_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(require_roles('Admin', 'Manager'))):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    if order.status not in (OrderStatus.submitted, OrderStatus.draft):
        raise HTTPException(status_code=400, detail='Order cannot be fulfilled')

    try:
        for line in order.lines:
            stock = db.query(Stock).filter_by(branch_id=order.branch_id, item_id=line.item_id).with_for_update().first()
            if not stock or stock.quantity < line.requested_qty:
                raise HTTPException(status_code=400, detail='Insufficient stock')
            stock.quantity -= line.requested_qty
            line.fulfilled_qty = line.requested_qty
            write_audit(db, int(user['sub']), 'stock_decrement', 'Stock', stock.id, request.client.host if request.client else 'unknown', {'order_id': order.id, 'qty': line.requested_qty})
        order.status = OrderStatus.fulfilled
        write_audit(db, int(user['sub']), 'order_fulfilled', 'Order', order.id, request.client.host if request.client else 'unknown', {'branch_id': order.branch_id})
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {'status': 'fulfilled'}


@router.get('/{order_id}')
def get_order(order_id: int, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager', 'Worker'))):
    return db.get(Order, order_id)


@router.delete('/{order_id}')
def delete_order(order_id: int, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager'))):
    order = db.get(Order, order_id)
    db.delete(order)
    db.commit()
    return {'deleted': True}
