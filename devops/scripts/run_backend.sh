#!/bin/sh
set -e

cd /opt/project/app/infrastructure/repositories/psql
poetry --directory /opt/project/app/ run alembic upgrade head

cd /opt/project/app
poetry run python run_func_before_starting_app.py
poetry run uvicorn infrastructure.web.app:app --host 0.0.0.0 --port 5000
