.PHONY: help install dev-install test lint format clean run seed docker-up docker-down migrate

help:
	@echo "Available commands:"
	@echo "  make install        - Install production dependencies"
	@echo "  make dev-install    - Install development dependencies"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linters"
	@echo "  make format         - Format code with black and ruff"
	@echo "  make clean          - Remove build artifacts and cache"
	@echo "  make run            - Run the application"
	@echo "  make seed           - Seed the database with sample data"
	@echo "  make docker-up      - Start docker containers"
	@echo "  make docker-down    - Stop docker containers"
	@echo "  make migrate        - Run database migrations"

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pre-commit install

test:
	pytest

lint:
	ruff check .
	black --check .

format:
	ruff check --fix .
	black .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.db" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf dist build

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

seed:
	python scripts/seed_database.py

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

migrate:
	alembic upgrade head

migrate-create:
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"
