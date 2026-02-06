from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Item
from app.schemas.domain import ItemIn
from app.core.security import require_roles

router = APIRouter(prefix='/items', tags=['items'])

@router.get('', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@router.post('', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def create_item(payload: ItemIn, db: Session = Depends(get_db)):
    i = Item(**payload.model_dump())
    db.add(i); db.commit(); db.refresh(i)
    return i

@router.get('/{item_id}', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def get_item(item_id: int, db: Session = Depends(get_db)):
    i = db.get(Item, item_id)
    if not i: raise HTTPException(404, 'Item not found')
    return i

@router.put('/{item_id}', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def update_item(item_id: int, payload: ItemIn, db: Session = Depends(get_db)):
    i = db.get(Item, item_id)
    if not i: raise HTTPException(404, 'Item not found')
    for k,v in payload.model_dump().items(): setattr(i,k,v)
    db.commit(); db.refresh(i); return i

@router.delete('/{item_id}', dependencies=[Depends(require_roles('Admin'))])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    i = db.get(Item, item_id)
    if not i: raise HTTPException(404, 'Item not found')
    db.delete(i); db.commit(); return {'status':'deleted'}
