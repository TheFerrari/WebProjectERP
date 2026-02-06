from app.models.domain import AuditLog


def write_audit(db, actor_user_id: int, action: str, entity_type: str, entity_id: int, ip: str, details: dict):
    event = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        ip=ip,
        details=details,
    )
    db.add(event)
