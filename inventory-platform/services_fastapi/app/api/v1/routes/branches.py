from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import Branch
from app.schemas.domain import BranchIn
from app.core.security import require_roles

router = APIRouter(prefix='/branches', tags=['branches'])


@router.get('')
def list_branches(db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager', 'Worker'))):
    return db.query(Branch).all()


@router.post('')
def create_branch(payload: BranchIn, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager'))):
    branch = Branch(**payload.model_dump())
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch


@router.get('/{branch_id}')
def get_branch(branch_id: int, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager', 'Worker'))):
    return db.get(Branch, branch_id)


@router.put('/{branch_id}')
def update_branch(branch_id: int, payload: BranchIn, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager'))):
    branch = db.get(Branch, branch_id)
    for k, v in payload.model_dump().items():
        setattr(branch, k, v)
    db.commit()
    db.refresh(branch)
    return branch


@router.delete('/{branch_id}')
def delete_branch(branch_id: int, db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Manager'))):
    branch = db.get(Branch, branch_id)
    db.delete(branch)
    db.commit()
    return {'deleted': True}
