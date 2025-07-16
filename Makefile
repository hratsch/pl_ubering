.PHONY: setup run test migrate-up migrate-down docker-up docker-down

setup:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

lint:
	black . && isort .