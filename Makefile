PROJECT_NAME = book_hub
VENV_DIR = .venv


PIP = $(VENV_DIR)/bin/pip
POETRY = $(VENV_DIR)/bin/poetry

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

clean_dev: ## Clean up development environment
	rm -rf .venv/