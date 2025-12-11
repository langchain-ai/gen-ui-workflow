# List available commands
default:
    @just --list

# Install all dependencies
install: install-backend install-frontend

# Install backend dependencies
install-backend:
    cd backend && uv venv && uv pip install -r pyproject.toml

# Install frontend dependencies
install-frontend:
    cd frontend && pnpm install

# Run both backend and frontend in parallel
dev:
    #!/usr/bin/env bash
    just dev-backend & just dev-frontend & wait

# Run backend development server
dev-backend:
    cd backend && uv run uvicorn main:app --reload --port 8000

# Run frontend development server
dev-frontend:
    cd frontend && pnpm run dev

# Build frontend for production
build:
    cd frontend && pnpm run build

# Run backend tests (placeholder)
test-backend:
    cd backend && uv run pytest

# Run frontend tests (placeholder)
test-frontend:
    cd frontend && pnpm test

# Clean build artifacts and dependencies
clean:
    rm -rf backend/venv backend/__pycache__ backend/*.pyc
    rm -rf frontend/node_modules frontend/dist

# Format backend code
format-backend:
    cd backend && uv run black . && uv run isort .

# Format frontend code
format-frontend:
    cd frontend && pnpm run format

# Lint backend code
lint-backend:
    cd backend && uv run flake8 .

# Lint frontend code
lint-frontend:
    cd frontend && pnpm run lint
