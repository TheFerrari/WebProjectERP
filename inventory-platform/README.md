# Inventory Platform (Hybrid Django + FastAPI)

Production-style monorepo scaffold for a multi-branch inventory and order management system.

## Stack
- Django 5 portal (session auth, admin, role management)
- FastAPI services (JWT auth + RBAC + transactional domain operations)
- PostgreSQL 15 shared database, table ownership split by service
- Docker Compose orchestration + health checks

## Quick start
```bash
cp .env.example .env
docker compose up --build
```

Endpoints:
- Portal: http://localhost:8000
- FastAPI docs: http://localhost:8001/docs
- Reverse proxy: http://localhost:8080

## Migrations
```bash
docker compose run --rm portal_django python manage.py migrate
docker compose run --rm services_fastapi alembic upgrade head
```

## Seed demo data
```bash
docker compose run --rm services_fastapi python -m app.services.seed
```

## Tests
```bash
docker compose run --rm portal_django pytest
docker compose run --rm services_fastapi pytest
```

## Integration Notes
Portal authenticates users via Django session and calls `/accounts/api/token/` to mint JWT claims (roles from Django groups). Portal then calls FastAPI over internal Docker DNS (`http://services_fastapi:8000`) with timeout/retry behavior to tolerate WAN-like latency.
