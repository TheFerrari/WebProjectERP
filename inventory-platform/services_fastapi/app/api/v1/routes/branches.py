from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Branch
from app.schemas.domain import BranchIn
from app.core.security import require_roles

router = APIRouter(prefix='/branches', tags=['branches'])

@router.get('', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def list_branches(db: Session = Depends(get_db)):
    return db.query(Branch).all()

@router.post('', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def create_branch(payload: BranchIn, db: Session = Depends(get_db)):
    b = Branch(**payload.model_dump())
    db.add(b); db.commit(); db.refresh(b)
    return b

@router.get('/{branch_id}', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def get_branch(branch_id: int, db: Session = Depends(get_db)):
    b = db.get(Branch, branch_id)
    if not b: raise HTTPException(404, 'Branch not found')
    return b

@router.put('/{branch_id}', dependencies=[Depends(require_roles('Admin', 'Manager'))])
def update_branch(branch_id: int, payload: BranchIn, db: Session = Depends(get_db)):
    b = db.get(Branch, branch_id)
    if not b: raise HTTPException(404, 'Branch not found')
    for k,v in payload.model_dump().items(): setattr(b,k,v)
    db.commit(); db.refresh(b); return b

@router.delete('/{branch_id}', dependencies=[Depends(require_roles('Admin'))])
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    b = db.get(Branch, branch_id)
    if not b: raise HTTPException(404, 'Branch not found')
    db.delete(b); db.commit(); return {'status':'deleted'}
