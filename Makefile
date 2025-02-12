# Определение операционной системы
ifeq ($(OS),Windows_NT)
    PYTHON := python
    PIP := pip
    CD := cd /d
else
    PYTHON := python3
    PIP := pip3
    CD := cd
endif

GIT = git
POETRY_VERSION := 1.8.3
POETRY := poetry
POETRY_PATH := --directory src/backend

# Проверка наличия Poetry
CHECK_POETRY := $(shell command -v poetry 2> /dev/null)

# Ветка для обновления
UPDATE_BRANCH := dev

# Pytest команда
PYTEST := $(POETRY) run python -m pytest

# Команда help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "make help      						Show this help message"
	@echo "make poetry      					Show current env info"
	@echo "make poetry-add      			Install python package in current environment"
	@echo "    Usage: make poetry-add  p=package_name v=version"
	@echo "make install   						Install dependencies using Poetry"
	@echo "make install-front					Install front dependencies"
	@echo "make migrate   						Run migrations"
	@echo "make generate-migration   	Create a new Alembic migration"
	@echo "    Usage: make generate-migration message=init_migration"
	@echo "make update    						Update from $(UPDATE_BRANCH), merge into current branch"
	@echo "make test      						Run pytest"
	@echo "make git-init  						Initialize Git repository"
	@echo "make pre-commit-install  	Install pre-commit hooks"
	@echo "make docker-up 						Start project with docker-compose"
	@echo "make celery-beat    				Start Celery Beat scheduler"
	@echo "make celery-worker  				Start Celery worker"
	@echo "    Usage: make celery-worker queue=periodic_queue"
	@echo "make init      						Init project"
	@echo "make dev       						Update from $(UPDATE_BRANCH), install dependencies, run migrations"



# Проверка и установка Poetry
ensure-poetry:
ifndef CHECK_POETRY
	@echo "Poetry not found. Installing Poetry..."
	$(PIP) install poetry==$(POETRY_VERSION)
else
	@echo "Poetry is already installed"
endif
	@poetry --version

# Команда получения информации о вирутальном окружении
poetry-info:
	$(POETRY) $(POETRY_PATH) env info


# Команда установки python пакета
poetry-add:
	$(POETRY) $(POETRY_PATH) add $(p)==$(v)


# Команда установки зависимостей
install: ensure-poetry
	@echo "Installing dependencies..."
	$(POETRY) $(POETRY_PATH) install --with dev --no-root
	@echo "Dependencies installed"

# Команда для установки зависимостей фронтенда
install-front:
	@echo "Installing front dependencies..."
	$(CD) src/frontend && yarn install --no-progress --non-interactive
	@echo "Dependencies installed"

# Команда запуска миграции
migrate: install
	@echo "Running migrations..."
	$(CD) src/backend/infrastructure/repositories/psql && $(POETRY) --directory ../../../ run alembic upgrade head
	@echo "Migrations completed"

# Команда для генерации миграции
generate-migration:
	@echo "Running generate migration..."
	$(CD) src/backend/infrastructure/repositories/psql && $(POETRY) --directory ../../../ run alembic revision --autogenerate -m $(message)
	@echo "Migration generation completed"

# Команда для обновления из удаленной ветки dev
.PHONY: update-dev
update: git-init
	@echo Updating from $(UPDATE_BRANCH) and merging into current branch...
	@$(GIT) fetch -p --all
	@$(GIT) fetch origin $(UPDATE_BRANCH):$(UPDATE_BRANCH)
	@$(GIT) pull --ff-only -q
	@$(GIT) merge $(UPDATE_BRANCH)
	@echo Merge completed. Please resolve any conflicts if they occurred.

# Команда для запуска тестов
test:
	@echo "Running tests with pytest..."
	$(CD) src/backend/ && $(PYTEST)
	@echo "Tests completed"

# Команда инициализации Git репозитория
git-init:
	$(GIT) init

# Команда установки автоматического запуска проверки кода перед каждым коммитом
pre-commit-install: install git-init
	@echo "Running pre commit install..."
	$(POETRY) $(POETRY_PATH) run pre-commit install
	@echo "Install completed"

# Команда для запуска проекта в docker через docker-compose
docker-up:
	@echo "Start project with docker-compose"
	$(POETRY) $(POETRY_PATH) run docker-compose -f devops/docker-compose/docker-compose.yml up --build

# Команда для запуска celery beat
celery-beat:
	@echo "Start Celery beat scheduler"
	$(CD) src/backend/ && $(POETRY) run celery -A infrastructure.celery.celery_app.celery beat

# Команда для запуска celery worker
celery-worker:
	@echo "Start Celery worker"
	$(CD) src/backend/ && $(POETRY) run celery -A infrastructure.celery.celery_app.celery worker -P solo -Q $(queue)

# команда для инициализации
init: install install-front migrate pre-commit-install

# команда для обновления
dev: update-dev install install-front migrate

# Устанавливаем help как команду по умолчанию
.DEFAULT_GOAL := help
