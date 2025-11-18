PROJECT_NAME = book_hub
TEST_PATH = ./tests
VENV_DIR = .venv

APP_WORKERS ?= 1

PIP = $(VENV_DIR)/bin/pip
POETRY = $(VENV_DIR)/bin/poetry
PYTEST = $(VENV_DIR)/bin/pytest
COVERAGE = $(VENV_DIR)/bin/coverage
RUFF = $(VENV_DIR)/bin/ruff

MANAGE_PY = python manage.py

.PHONY: develop app


develop: clean_dev
	python3.12 -m venv $(VENV_DIR)
	$(PIP) install -U pip poetry
	$(POETRY) config virtualenvs.create false
	$(POETRY) install
	$(POETRY) run pre-commit install


app:
	$(MANAGE_PY) runserver
