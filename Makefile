.PHONY: up down migrate seed test

up:
	sudo docker-compose up -d

down:
	sudo docker-compose down

migrate:
	sudo docker-compose exec -T postgres psql -U searchcraft -d searchcraft < migrations/001_initial.sql

seed:
	sudo docker-compose exec web python -c "from src.seed import seed; seed()"

test:
	sudo docker-compose exec web pytest tests/

logs:
	sudo docker-compose logs -f
