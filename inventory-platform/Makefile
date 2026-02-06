.PHONY: up down test lint

up:
	docker compose up --build

down:
	docker compose down -v

test:
	docker compose exec portal_django pytest
	docker compose exec services_fastapi pytest

migrate:
	docker compose exec portal_django python manage.py migrate
	docker compose exec services_fastapi alembic upgrade head
