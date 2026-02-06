from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import Stock, Item, Branch
from app.schemas.domain import StockUpdate
from app.core.security import require_roles, get_current_user
from app.services.audit import write_audit

router = APIRouter(prefix='/stock', tags=['stock'])


@router.get('')
def get_stock(db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager', 'Worker'))):
    return db.query(Stock).all()


@router.get('/summary')
def stock_summary(db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager', 'Worker'))):
    rows = db.query(Stock, Item, Branch).join(Item, Stock.item_id == Item.id).join(Branch, Stock.branch_id == Branch.id).all()
    return [{'branch_name': b.name, 'item_name': i.name, 'quantity': s.quantity} for s, i, b in rows]


@router.put('')
def put_stock(payload: StockUpdate, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(require_roles('Admin', 'Manager'))):
    record = db.query(Stock).filter_by(branch_id=payload.branch_id, item_id=payload.item_id).first()
    if not record:
        record = Stock(branch_id=payload.branch_id, item_id=payload.item_id, quantity=0)
        db.add(record)
    if payload.quantity < 0 and not payload.override_negative and 'Admin' not in user.get('roles', []):
        raise HTTPException(status_code=400, detail='Negative stock requires admin override')
    record.quantity = payload.quantity
    write_audit(db, int(user['sub']), 'stock_adjustment', 'Stock', record.id or 0, request.client.host if request.client else 'unknown', payload.model_dump())
    db.commit()
    db.refresh(record)
    return record
