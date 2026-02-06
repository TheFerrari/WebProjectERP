from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import Item
from app.schemas.domain import ItemIn
from app.core.security import require_roles

router = APIRouter(prefix='/items', tags=['items'])


@router.get('')
def list_items(db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager', 'Worker'))):
    return db.query(Item).all()


@router.post('')
def create_item(payload: ItemIn, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager'))):
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get('/{item_id}')
def get_item(item_id: int, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager', 'Worker'))):
    return db.get(Item, item_id)


@router.put('/{item_id}')
def update_item(item_id: int, payload: ItemIn, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager'))):
    item = db.get(Item, item_id)
    for k, v in payload.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@router.delete('/{item_id}')
def delete_item(item_id: int, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager'))):
    item = db.get(Item, item_id)
    db.delete(item)
    db.commit()
    return {'deleted': True}
