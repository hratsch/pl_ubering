.PHONY: setup run test docker-up docker-down lint backup tunnel

setup:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

lint:
	black . && isort .

backup:
	docker exec postgres pg_dump uberpl_db > backups/db_$(date +%Y%m%d).sql

tunnel:
	cloudflared tunnel --config config.yml run uberpl-tunnel &