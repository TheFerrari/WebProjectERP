# Inventory Platform Monorepo

Hybrid architecture with Django Portal + FastAPI Services for multi-branch inventory and order management.

## Quick start
1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Build and start:
   ```bash
   docker compose up --build
   ```
3. Access:
   - Django portal: http://localhost:8000
   - Django admin: http://localhost:8000/admin
   - FastAPI docs: http://localhost:8001/docs

## Migrations and seed data
Django migrations + seed run at container startup (`python manage.py migrate && python manage.py seed_data`).
FastAPI Alembic migrations run at startup (`alembic upgrade head`).

## Authentication strategy (Option A)
- Portal users authenticate with Django session auth.
- Portal endpoint `/accounts/api/token` issues JWT containing `sub`, `username`, `roles`.
- FastAPI validates JWT signature via `FASTAPI_JWT_SECRET` and enforces RBAC.

## Run tests
```bash
cd portal_django && pytest
cd ../services_fastapi && pytest
```

## WAN-latency strategy
Portal -> FastAPI calls use timeout + retry (`PORTAL_REQUEST_TIMEOUT`, `PORTAL_REQUEST_RETRIES`) and degrade gracefully on outage.

## Seed users and roles
Roles are created: `Admin`, `Manager`, `Worker`, `Auditor`.
Create a superuser with `.env` variables or via:
```bash
docker compose exec portal_django python manage.py createsuperuser
```
