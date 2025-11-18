.PHONY: help start stop build clean logs test

help:
	@echo "FeelInk Development Commands"
	@echo "============================"
	@echo "make start    - Start all services (Docker Compose)"
	@echo "make stop     - Stop all services"
	@echo "make build    - Build all Docker images"
	@echo "make clean    - Remove all containers and volumes"
	@echo "make logs     - View logs from all services"
	@echo "make test     - Run tests"
	@echo "make migrate  - Run database migrations"

start:
	docker-compose up -d
	@echo "✅ FeelInk is starting..."
	@echo "Frontend: http://localhost:5173"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

stop:
	docker-compose down
	@echo "✅ FeelInk stopped"

build:
	docker-compose build
	@echo "✅ Images built successfully"

clean:
	docker-compose down -v
	@echo "✅ Cleaned up containers and volumes"

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

migrate:
	docker-compose exec backend alembic upgrade head
	@echo "✅ Migrations applied"

migrate-create:
	@read -p "Enter migration message: " message; \
	docker-compose exec backend alembic revision --autogenerate -m "$$message"

test:
	@echo "Running tests..."
	docker-compose exec backend pytest
	docker-compose exec frontend npm run test

shell-backend:
	docker-compose exec backend bash

shell-frontend:
	docker-compose exec frontend sh

db-shell:
	docker-compose exec postgres psql -U feelink_user -d feelink_db
