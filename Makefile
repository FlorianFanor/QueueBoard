.PHONY: up down seed fmt
up:
	docker compose up --build
down:
	docker compose down -v
seed:
	python scripts/seed_demo.py
fmt:
	ruff check --fix || true
	black . || true
