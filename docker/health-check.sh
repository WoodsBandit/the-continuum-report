#!/bin/bash
# The Continuum Report - Docker Health Check Script
# Comprehensive health check for all services and integrations

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Helper functions

print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# Docker checks

check_docker_running() {
    print_header "Docker Environment"

    if command -v docker &> /dev/null; then
        check_pass "Docker is installed"
    else
        check_fail "Docker is not installed"
        exit 1
    fi

    if docker ps &> /dev/null; then
        check_pass "Docker daemon is running"
    else
        check_fail "Docker daemon is not running"
        exit 1
    fi

    if command -v docker-compose &> /dev/null; then
        check_pass "Docker Compose is installed"
    else
        check_fail "Docker Compose is not installed"
        exit 1
    fi
}

# Container checks

check_containers() {
    print_header "Container Status"

    local running=$(docker compose ps --services --filter "status=running" 2>/dev/null | wc -l)
    local total=$(docker compose ps --services 2>/dev/null | wc -l)

    if [ "$running" -eq "$total" ] && [ "$total" -gt 0 ]; then
        check_pass "All containers running ($total/$total)"
    elif [ "$running" -gt 0 ]; then
        check_warn "Some containers running ($running/$total)"
    else
        check_fail "No containers running"
    fi

    # Check specific containers
    if docker compose ps continuum 2>/dev/null | grep -q "Up"; then
        check_pass "Continuum container is running"
    else
        check_fail "Continuum container is not running"
    fi

    if docker compose ps paperless 2>/dev/null | grep -q "Up"; then
        check_pass "Paperless container is running"
    else
        check_warn "Paperless container is not running (required for full functionality)"
    fi

    if docker compose ps ollama 2>/dev/null | grep -q "Up"; then
        check_pass "Ollama container is running"
    else
        check_warn "Ollama container is not running (required for full functionality)"
    fi
}

# Network checks

check_network() {
    print_header "Network Configuration"

    if docker network ls 2>/dev/null | grep -q "continuum-network"; then
        check_pass "Continuum network exists"
    else
        check_fail "Continuum network not found"
    fi
}

# Service connectivity checks

check_paperless() {
    print_header "Paperless-ngx Service"

    # Check if container is running
    if ! docker compose ps paperless 2>/dev/null | grep -q "Up"; then
        check_warn "Paperless container not running"
        return
    fi

    # Test HTTP connectivity
    if docker compose exec paperless curl -s http://localhost:8000/ &> /dev/null; then
        check_pass "Paperless HTTP port responsive"
    else
        check_fail "Paperless HTTP port not responsive"
    fi

    # Test from continuum container
    if docker compose exec continuum curl -s http://paperless:8000/api/ &> /dev/null; then
        check_pass "Continuum can reach Paperless API"
    else
        check_fail "Continuum cannot reach Paperless API"
    fi

    # Test API token (if available)
    if docker compose exec continuum python -c "
from lib import PaperlessClient
try:
    client = PaperlessClient()
    client.get_documents(limit=1)
    print('OK')
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)
" 2>/dev/null | grep -q "OK"; then
        check_pass "Paperless API authentication works"
    else
        check_fail "Paperless API authentication failed (check PAPERLESS_TOKEN)"
    fi
}

check_ollama() {
    print_header "Ollama Service"

    # Check if container is running
    if ! docker compose ps ollama 2>/dev/null | grep -q "Up"; then
        check_warn "Ollama container not running"
        return
    fi

    # Test HTTP connectivity
    if docker compose exec ollama curl -s http://localhost:11434/api/tags &> /dev/null; then
        check_pass "Ollama HTTP port responsive"
    else
        check_fail "Ollama HTTP port not responsive"
    fi

    # Test from continuum container
    if docker compose exec continuum curl -s http://ollama:11434/api/tags &> /dev/null; then
        check_pass "Continuum can reach Ollama API"
    else
        check_fail "Continuum cannot reach Ollama API"
    fi

    # List available models
    local models=$(docker compose exec ollama ollama list 2>/dev/null | grep -v "NAME" | wc -l)
    if [ "$models" -gt 0 ]; then
        check_pass "Ollama has $models model(s) available"
    else
        check_warn "No Ollama models installed (use: docker compose exec ollama ollama pull mistral)"
    fi

    # Test model inference
    if docker compose exec continuum python -c "
from lib import OllamaClient
try:
    client = OllamaClient()
    response = client.generate('test prompt', stream=False)
    if response and len(response) > 0:
        print('OK')
    else:
        print('EMPTY_RESPONSE')
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)
" 2>/dev/null | grep -q "OK"; then
        check_pass "Ollama model inference works"
    elif docker compose exec continuum python -c "
from lib import OllamaClient
try:
    client = OllamaClient()
    client.generate('test')
except Exception as e:
    exit(1)
" 2>/dev/null; then
        check_pass "Ollama model inference works (streaming)"
    else
        check_fail "Ollama model inference failed (model not loaded or misconfigured)"
    fi
}

# Data checks

check_data() {
    print_header "Data Persistence"

    # Check entity database
    if docker compose exec continuum test -f /continuum/entity_data/entity_database.json; then
        local count=$(docker compose exec continuum python -c "
import json
data = json.load(open('/continuum/entity_data/entity_database.json'))
print(len(data))
" 2>/dev/null || echo "0")
        check_pass "Entity database exists ($count entities)"
    else
        check_warn "Entity database not yet created"
    fi

    # Check checkpoint directory
    if docker compose exec continuum test -d /continuum/checkpoints; then
        check_pass "Checkpoint directory exists"
    else
        check_fail "Checkpoint directory missing"
    fi

    # Check reports directory
    if docker compose exec continuum test -d /continuum/reports; then
        check_pass "Reports directory exists"
    else
        check_fail "Reports directory missing"
    fi

    # Check volumes
    local volumes=$(docker volume ls | grep continuum | wc -l)
    if [ "$volumes" -gt 0 ]; then
        check_pass "Data volumes exist ($volumes volumes)"
    else
        check_fail "No data volumes found"
    fi
}

# Configuration checks

check_config() {
    print_header "Configuration"

    # Check .env file
    if [ -f .env ]; then
        check_pass ".env file exists"

        # Check required variables
        if grep -q "PAPERLESS_TOKEN=" .env && grep "PAPERLESS_TOKEN=" .env | grep -qv "^#"; then
            check_pass "PAPERLESS_TOKEN is configured"
        else
            check_warn "PAPERLESS_TOKEN not configured"
        fi

        if grep -q "PAPERLESS_SECRET_KEY=" .env && grep "PAPERLESS_SECRET_KEY=" .env | grep -qv "^#"; then
            check_pass "PAPERLESS_SECRET_KEY is configured"
        else
            check_warn "PAPERLESS_SECRET_KEY not configured"
        fi
    else
        check_fail ".env file not found (copy from .env.example)"
    fi

    # Check docker-compose files
    if [ -f docker-compose.yml ]; then
        check_pass "docker-compose.yml exists"
    else
        check_fail "docker-compose.yml not found"
    fi

    if [ -f docker-compose.dev.yml ]; then
        check_pass "docker-compose.dev.yml exists"
    else
        check_warn "docker-compose.dev.yml not found"
    fi
}

# Resource checks

check_resources() {
    print_header "System Resources"

    # Check disk space
    local available=$(df / | awk 'NR==2 {print $4}')
    if [ "$available" -gt 5242880 ]; then  # 5GB in KB
        check_pass "Sufficient disk space available ($(($available / 1024 / 1024))GB)"
    else
        check_warn "Low disk space available ($(($available / 1024 / 1024))GB)"
    fi

    # Check Docker memory limits
    if docker compose ps continuum &>/dev/null; then
        local memory=$(docker inspect continuum 2>/dev/null | grep -o '"Memory": [^,]*' | cut -d' ' -f2 || echo "0")
        if [ "$memory" -gt 0 ]; then
            check_pass "Continuum memory limit: $(($memory / 1024 / 1024))MB"
        fi
    fi
}

# Summary

print_summary() {
    print_header "Health Check Summary"

    echo -e "${GREEN}Passed:${NC} $PASSED"
    echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
    echo -e "${RED}Failed:${NC} $FAILED"

    if [ "$FAILED" -eq 0 ]; then
        echo -e "\n${GREEN}All checks passed!${NC}"
        return 0
    else
        echo -e "\n${RED}Some checks failed. See above for details.${NC}"
        return 1
    fi
}

# Main execution

main() {
    echo -e "${BLUE}The Continuum Report - Health Check${NC}"
    echo "$(date)"

    check_docker_running
    check_containers
    check_network
    check_config
    check_paperless
    check_ollama
    check_data
    check_resources

    print_summary
}

main "$@"
