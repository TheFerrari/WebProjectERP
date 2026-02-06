# Threat Model

| Threat | Risk | Mitigation |
|---|---|---|
| Credential theft | Account takeover | Django hashed passwords, session security, rotate secrets |
| JWT forgery | Unauthorized API access | HS256 signature validation with env-managed secret |
| Excessive permissions | Insider misuse | RBAC with Admin/Manager/Worker/Auditor claims |
| Sensitive data leakage in logs | Privacy breach | Structured logging with token/password redaction policy |
| SQL injection | Data corruption | ORM parameterization (Django ORM + SQLAlchemy) |
| Replay on WAN links | Session hijack | TLS, short JWT expiry, request-id tracing |
| Service outage / WAN latency | Operational delays | retries/timeouts and graceful dashboard fallback |
| Unauthorized stock edits | Inventory fraud | Role checks + immutable audit log entries |
