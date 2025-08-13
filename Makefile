# Makefile for Suna/Kortix AI Platform
# Provides convenient commands for deployment and management

.PHONY: help setup start stop restart status logs build deploy-local deploy-prod clean

# Default target
help:
	@echo "🚀 Suna/Kortix AI Platform - Deployment Commands"
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup           Run the interactive setup wizard"
	@echo "  env             Create environment files from examples"
	@echo ""
	@echo "Development Commands:"
	@echo "  start           Start all services with Docker Compose"
	@echo "  stop            Stop all services"
	@echo "  restart         Restart all services"
	@echo "  status          Check deployment status"
	@echo "  logs            Show service logs"
	@echo ""
	@echo "Build Commands:"
	@echo "  build           Build Docker images"
	@echo "  build-no-cache  Build Docker images without cache"
	@echo ""
	@echo "Deployment Commands:"
	@echo "  deploy-local    Deploy for local development"
	@echo "  deploy-prod     Deploy for production"
	@echo ""
	@echo "Maintenance Commands:"
	@echo "  clean           Clean up Docker resources"
	@echo "  reset           Reset all data and restart"

# Setup commands
setup:
	python setup.py

env:
	@if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env && echo "Created backend/.env"; fi
	@if [ ! -f frontend/.env.local ]; then cp frontend/.env.example frontend/.env.local && echo "Created frontend/.env.local"; fi

# Development commands
start: env
	python start.py -f

stop:
	docker compose down

restart: stop start

status:
	python status.py

logs:
	docker compose logs -f --tail=100

# Build commands
build:
	docker compose build

build-no-cache:
	docker compose build --no-cache

# Deployment commands
deploy-local: env
	python deploy.py --method local

deploy-prod: env
	python deploy.py --method production

# Maintenance commands
clean:
	docker system prune -f
	docker volume prune -f

reset: stop clean
	docker compose up -d --build

# Quick development workflow
dev: env build start status

# Production workflow  
prod: env deploy-prod status