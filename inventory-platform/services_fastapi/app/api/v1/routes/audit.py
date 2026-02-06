from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import AuditLog
from app.core.security import require_roles

router = APIRouter(prefix='/audit', tags=['audit'])

@router.get('', dependencies=[Depends(require_roles('Admin', 'Auditor'))])
def list_audit(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(200).all()
