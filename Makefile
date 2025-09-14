PY ?= python3
PIP ?= pip3
VENv := .venv
ACT := . $(VENv)/bin/activate

.PHONY: setup dev test lint fmt build clean

setup:
	$(PY) -m venv $(VENv)
	$(ACT) && $(PIP) install -U pip
	$(ACT) && $(PIP) install -r requirements.txt

dev:
	$(ACT) && uvicorn src.adapters.api.main:app --reload --port 8000

test:
	$(ACT) && pytest -q

lint:
	$(ACT) && ruff check . && black --check .

fmt:
	$(ACT) && black . && ruff check --fix .

build:
	@echo "No binary build. The API serves OpenAPI at /docs and /openapi.json."

clean:
	rm -rf $(VENv) __pycache__ .pytest_cache .ruff_cache
	find . -name "*.pyc" -delete

