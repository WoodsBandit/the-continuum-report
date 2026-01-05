#!/bin/bash
# The Continuum Report - Docker Helper Scripts
# Provides convenient commands for managing containers

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Build Commands

build_image() {
    print_header "Building Continuum Docker Image"
    docker compose build
    print_success "Image built successfully"
}

build_image_no_cache() {
    print_header "Building Continuum Docker Image (no cache)"
    docker compose build --no-cache
    print_success "Image built successfully"
}

# Container Management

start_services() {
    print_header "Starting All Services"
    docker compose up -d
    print_success "Services started"
    docker compose ps
}

start_dev() {
    print_header "Starting Development Environment"
    docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    print_success "Development environment started"
    docker compose -f docker-compose.yml -f docker-compose.dev.yml ps
}

stop_services() {
    print_header "Stopping All Services"
    docker compose down
    print_success "Services stopped"
}

restart_services() {
    print_header "Restarting All Services"
    docker compose restart
    print_success "Services restarted"
    docker compose ps
}

# Logging

logs_continuum() {
    docker compose logs -f continuum
}

logs_paperless() {
    docker compose logs -f paperless
}

logs_ollama() {
    docker compose logs -f ollama
}

logs_all() {
    docker compose logs -f
}

# Shell Access

shell_continuum() {
    print_header "Opening Shell in Continuum Container"
    docker compose exec continuum sh
}

shell_dev() {
    print_header "Opening Development Shell"
    docker compose -f docker-compose.yml -f docker-compose.dev.yml run cli bash
}

# Testing

run_tests() {
    print_header "Running Tests"
    docker compose -f docker-compose.yml -f docker-compose.dev.yml run tests
}

# Pipeline Operations

run_pipeline() {
    print_header "Running Continuum Pipeline"
    docker compose exec continuum python -m scripts.continuum_pipeline
}

run_entity_discovery() {
    print_header "Running Entity Discovery"
    docker compose exec continuum python -m scripts.entity_discovery
}

run_dossier_generation() {
    print_header "Running Dossier Generation"
    docker compose exec continuum python -m scripts.generate_dossiers
}

# Debugging

test_paperless() {
    print_header "Testing Paperless Connection"
    docker compose exec continuum python -c "
from lib import PaperlessClient
try:
    client = PaperlessClient()
    docs = client.get_documents(limit=1)
    print(f'✓ Paperless connected: {len(docs)} documents found')
except Exception as e:
    print(f'✗ Paperless error: {e}')
    exit(1)
"
}

test_ollama() {
    print_header "Testing Ollama Connection"
    docker compose exec continuum python -c "
from lib import OllamaClient
try:
    client = OllamaClient()
    result = client.generate('test prompt')
    print(f'✓ Ollama connected: model working')
except Exception as e:
    print(f'✗ Ollama error: {e}')
    exit(1)
"
}

test_all_connections() {
    test_paperless
    test_ollama
    print_success "All connections working"
}

list_models() {
    print_header "Available Ollama Models"
    docker compose exec ollama ollama list
}

pull_model() {
    if [ -z "$1" ]; then
        print_error "Usage: ./scripts.sh pull-model <model-name>"
        echo "Examples: mistral, llama2, neural-chat, zephyr"
        exit 1
    fi

    print_header "Pulling Model: $1"
    docker compose exec ollama ollama pull "$1"
    print_success "Model $1 pulled successfully"
}

# Data Management

show_entity_count() {
    print_header "Entity Database Stats"
    docker compose exec continuum python -c "
import json
from pathlib import Path
db_file = Path('/continuum/entity_data/entity_database.json')
if db_file.exists():
    data = json.load(open(db_file))
    print(f'Total entities: {len(data)}')
    print(f'Sample entities: {list(data.keys())[:5]}')
else:
    print('Entity database not found')
"
}

show_reports() {
    print_header "Generated Reports"
    docker compose exec continuum ls -lh /continuum/reports/ || echo "No reports found"
}

show_checkpoints() {
    print_header "Processing Checkpoints"
    docker compose exec continuum ls -lh /continuum/checkpoints/ || echo "No checkpoints found"
}

# Volume Management

list_volumes() {
    print_header "Docker Volumes"
    docker volume ls | grep continuum
}

backup_data() {
    print_header "Backing Up Entity Data"
    BACKUP_FILE="continuum-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
    docker run --rm -v continuum-entity-data:/data -v "$(pwd)":/backup \
        alpine tar czf "/backup/$BACKUP_FILE" -C /data .
    print_success "Backup created: $BACKUP_FILE"
}

restore_data() {
    if [ -z "$1" ]; then
        print_error "Usage: ./scripts.sh restore-data <backup-file>"
        exit 1
    fi

    if [ ! -f "$1" ]; then
        print_error "Backup file not found: $1"
        exit 1
    fi

    print_header "Restoring Entity Data from $1"
    docker run --rm -v continuum-entity-data:/data -v "$(pwd)":/backup \
        alpine tar xzf "/backup/$1" -C /data
    print_success "Data restored"
}

# Cleanup

cleanup() {
    print_header "Cleaning Up"
    docker compose down
    print_success "Containers stopped and removed"
}

cleanup_volumes() {
    print_warning "This will delete all data in volumes!"
    read -p "Continue? (yes/no) " -n 3 -r
    echo
    if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        docker compose down -v
        print_success "Containers and volumes removed"
    fi
}

prune_images() {
    print_header "Pruning Unused Images"
    docker image prune -a --force
    print_success "Pruned"
}

# Help

show_help() {
    cat << EOF
${BLUE}The Continuum Report - Docker Helper${NC}

Usage: ./docker/scripts.sh <command> [arguments]

${BLUE}Build Commands:${NC}
  build                 Build Continuum Docker image
  build-no-cache        Build image without using cache

${BLUE}Container Management:${NC}
  start                 Start all services
  start-dev             Start development environment
  stop                  Stop all services
  restart               Restart all services
  status                Show container status

${BLUE}Logging:${NC}
  logs                  View all logs (streaming)
  logs-continuum        View Continuum logs (streaming)
  logs-paperless        View Paperless logs (streaming)
  logs-ollama           View Ollama logs (streaming)

${BLUE}Shell Access:${NC}
  shell                 Open shell in Continuum container
  shell-dev             Open development shell with bash

${BLUE}Testing:${NC}
  test-all              Test all service connections
  test-paperless        Test Paperless connection
  test-ollama           Test Ollama connection
  tests                 Run test suite

${BLUE}Pipeline Operations:${NC}
  pipeline              Run Continuum pipeline
  entity-discovery      Run entity discovery
  dossier-gen           Generate dossiers

${BLUE}Ollama Management:${NC}
  list-models           List available models
  pull-model <name>     Pull Ollama model

${BLUE}Data Management:${NC}
  entity-count          Show entity database stats
  reports               List generated reports
  checkpoints           List processing checkpoints
  backup                Backup entity data
  restore <file>        Restore entity data from backup

${BLUE}Volume Management:${NC}
  volumes               List Docker volumes

${BLUE}Cleanup:${NC}
  cleanup               Stop and remove containers
  cleanup-volumes       Remove containers and volumes (WARNING: deletes data)
  prune-images          Remove unused images

${BLUE}Other:${NC}
  help                  Show this help message

${BLUE}Examples:${NC}
  ./docker/scripts.sh build
  ./docker/scripts.sh start
  ./docker/scripts.sh logs-continuum
  ./docker/scripts.sh shell
  ./docker/scripts.sh test-all
  ./docker/scripts.sh pipeline
  ./docker/scripts.sh pull-model mistral
  ./docker/scripts.sh backup

EOF
}

# Main

main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi

    case "$1" in
        build)
            build_image
            ;;
        build-no-cache)
            build_image_no_cache
            ;;
        start)
            start_services
            ;;
        start-dev)
            start_dev
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        status)
            docker compose ps
            ;;
        logs)
            logs_all
            ;;
        logs-continuum)
            logs_continuum
            ;;
        logs-paperless)
            logs_paperless
            ;;
        logs-ollama)
            logs_ollama
            ;;
        shell)
            shell_continuum
            ;;
        shell-dev)
            shell_dev
            ;;
        tests)
            run_tests
            ;;
        pipeline)
            run_pipeline
            ;;
        entity-discovery)
            run_entity_discovery
            ;;
        dossier-gen)
            run_dossier_generation
            ;;
        test-all)
            test_all_connections
            ;;
        test-paperless)
            test_paperless
            ;;
        test-ollama)
            test_ollama
            ;;
        list-models)
            list_models
            ;;
        pull-model)
            pull_model "$2"
            ;;
        entity-count)
            show_entity_count
            ;;
        reports)
            show_reports
            ;;
        checkpoints)
            show_checkpoints
            ;;
        volumes)
            list_volumes
            ;;
        backup)
            backup_data
            ;;
        restore)
            restore_data "$2"
            ;;
        cleanup)
            cleanup
            ;;
        cleanup-volumes)
            cleanup_volumes
            ;;
        prune-images)
            prune_images
            ;;
        help)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
