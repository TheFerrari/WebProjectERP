.PHONY: up down logs migrate seed test test-portal test-services

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f

migrate:
	docker compose run --rm portal_django python manage.py migrate
	docker compose run --rm services_fastapi alembic upgrade head

seed:
	docker compose run --rm services_fastapi python -m app.services.seed

test: test-portal test-services

test-portal:
	docker compose run --rm portal_django pytest

test-services:
	docker compose run --rm services_fastapi pytest
