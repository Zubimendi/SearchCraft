.PHONY: up down migrate seed test

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	docker-compose exec web python -m alembic upgrade head || \
	docker-compose exec web psql -U searchcraft -d searchcraft -f /app/migrations/001_initial.sql

seed:
	docker-compose exec web python -c "from src.seed import seed; seed()"

test:
	docker-compose exec web pytest tests/

logs:
	docker-compose logs -f
