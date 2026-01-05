# The Continuum Report - Docker Makefile
# Convenient commands for Docker operations

.PHONY: help build start stop restart logs shell test pipeline clean

help:
	@echo "The Continuum Report - Docker Management"
	@echo ""
	@echo "Build targets:"
	@echo "  make build              Build Docker image"
	@echo "  make build-no-cache     Build without cache"
	@echo ""
	@echo "Container management:"
	@echo "  make start              Start all services"
	@echo "  make start-dev          Start development environment"
	@echo "  make stop               Stop all services"
	@echo "  make restart            Restart all services"
	@echo "  make status             Show container status"
	@echo ""
	@echo "Logging:"
	@echo "  make logs               View all logs"
	@echo "  make logs-continuum     View Continuum logs"
	@echo "  make logs-paperless     View Paperless logs"
	@echo "  make logs-ollama        View Ollama logs"
	@echo ""
	@echo "Shell access:"
	@echo "  make shell              Open shell in Continuum"
	@echo "  make shell-dev          Open development shell"
	@echo ""
	@echo "Testing and operations:"
	@echo "  make test-all           Test all connections"
	@echo "  make test-paperless     Test Paperless"
	@echo "  make test-ollama        Test Ollama"
	@echo "  make pipeline           Run pipeline"
	@echo "  make entity-discovery   Run entity discovery"
	@echo ""
	@echo "Data management:"
	@echo "  make backup             Backup data"
	@echo "  make entity-count       Show entity count"
	@echo "  make reports            Show reports"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean              Stop and remove containers"
	@echo "  make clean-volumes      Remove containers and volumes"
	@echo "  make prune-images       Prune unused images"
	@echo ""

# Build commands

build:
	docker compose build

build-no-cache:
	docker compose build --no-cache

# Container management

start:
	docker compose up -d
	docker compose ps

start-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	docker compose -f docker-compose.yml -f docker-compose.dev.yml ps

stop:
	docker compose down

restart:
	docker compose restart
	docker compose ps

status:
	docker compose ps

# Logging

logs:
	docker compose logs -f

logs-continuum:
	docker compose logs -f continuum

logs-paperless:
	docker compose logs -f paperless

logs-ollama:
	docker compose logs -f ollama

# Shell access

shell:
	docker compose exec continuum sh

shell-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml run cli bash

# Testing

test-all:
	@echo "Testing Paperless..."
	@docker compose exec continuum python -c "from lib import PaperlessClient; PaperlessClient().get_documents(limit=1); print('✓ Paperless OK')" || echo "✗ Paperless FAILED"
	@echo "Testing Ollama..."
	@docker compose exec continuum python -c "from lib import OllamaClient; OllamaClient().generate('test'); print('✓ Ollama OK')" || echo "✗ Ollama FAILED"

test-paperless:
	docker compose exec continuum python -c "from lib import PaperlessClient; PaperlessClient().get_documents(limit=1); print('✓ Paperless connected')"

test-ollama:
	docker compose exec continuum python -c "from lib import OllamaClient; OllamaClient().generate('test'); print('✓ Ollama connected')"

# Pipeline operations

pipeline:
	docker compose exec continuum python -m scripts.continuum_pipeline

entity-discovery:
	docker compose exec continuum python -m scripts.entity_discovery

dossier-gen:
	docker compose exec continuum python -m scripts.generate_dossiers

# Data management

entity-count:
	@docker compose exec continuum python -c "import json; data=json.load(open('/continuum/entity_data/entity_database.json')); print(f'Total entities: {len(data)}')" || echo "No entities found"

reports:
	@docker compose exec continuum ls -lh /continuum/reports/ || echo "No reports found"

backup:
	@mkdir -p backups
	@docker run --rm -v continuum-entity-data:/data -v "$$(pwd)/backups":/backup \
		alpine tar czf "/backup/continuum-backup-$$(date +%Y%m%d-%H%M%S).tar.gz" -C /data .
	@echo "Backup created in backups/"

# Cleanup

clean:
	docker compose down

clean-volumes:
	@echo "WARNING: This will delete all data!"
	@read -p "Continue? (yes/no) " REPLY; \
	if [ "$$REPLY" = "yes" ]; then \
		docker compose down -v; \
		echo "Cleaned"; \
	fi

prune-images:
	docker image prune -a --force

prune-all: clean-volumes prune-images
	@echo "Full cleanup complete"
