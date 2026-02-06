from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Order, OrderLine, Stock, AuditLog, OrderStatus


def fulfill_order(db: Session, order_id: int, actor_user_id: int, ip: str, override_negative: bool = False):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(404, 'Order not found')
    lines = db.query(OrderLine).filter_by(order_id=order_id).all()

    with db.begin_nested():
        for line in lines:
            stock = db.query(Stock).filter_by(branch_id=order.branch_id, item_id=line.item_id).first()
            if not stock:
                raise HTTPException(400, 'Stock row missing')
            new_qty = stock.quantity - line.requested_qty
            if new_qty < 0 and not override_negative:
                raise HTTPException(400, 'Negative stock denied')
            stock.quantity = new_qty
            line.fulfilled_qty = line.requested_qty
            db.add(AuditLog(actor_user_id=actor_user_id, action='stock_adjust', entity_type='Stock', entity_id=f'{stock.branch_id}:{stock.item_id}', ip=ip, details={'delta': -line.requested_qty}))
        order.status = OrderStatus.fulfilled
        db.add(AuditLog(actor_user_id=actor_user_id, action='order_fulfill', entity_type='Order', entity_id=str(order.id), ip=ip, details={'override_negative': override_negative}))
    db.commit()
    return order
