.PHONY: setup run test migrate-up migrate-down docker-up docker-down

setup:
	pip install -r requirements.txt
	alembic init migrations  # Run once

run:
	uvicorn app.main:app --reload

test:
	pytest

migrate-up:
	alembic upgrade head

migrate-down:
	alembic downgrade -1

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

lint:
	black . && isort .