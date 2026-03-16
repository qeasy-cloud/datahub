.PHONY: install run test check-docs

install:
	pip install -e ".[dev]"

run:
	uvicorn app.main:app --app-dir src --reload

test:
	pytest

check-docs:
	python scripts/check_markdown_links.py
