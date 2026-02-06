# Threat model

| Threat | Risk | Mitigation |
|---|---|---|
| Token theft in transit | Unauthorized API access | TLS in WAN/VPN links; short JWT expiry; no token logging |
| Privilege escalation | Unauthorized stock manipulation | Django groups to JWT roles, FastAPI RBAC dependency checks |
| SQL injection | Data corruption/exfiltration | ORM parameterization in Django + SQLAlchemy |
| Insider abuse | Silent data tampering | Mandatory audit log on stock adjustments and fulfillment |
| Service outage | Branch operations disruption | Health/readiness checks, retry strategy in portal, fallback UX |
| Sensitive data leakage in logs | Compliance/privacy issue | Structured logging with minimization, exclude secrets/passwords |
