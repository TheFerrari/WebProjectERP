from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import AuditLog
from app.core.security import require_roles

router = APIRouter(prefix='/audit', tags=['audit'])


@router.get('')
def get_audit(db: Session = Depends(get_db), _=Depends(require_roles('Admin', 'Auditor'))):
    return db.query(AuditLog).order_by(AuditLog.id.desc()).limit(100).all()
