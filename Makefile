.DEFAULT_GOAL := help
SHELL := /bin/bash

# Determine this makefile's path.
# Be sure to place this BEFORE `include` directives, if any.
DEFAULT_BRANCH := main
VERSION := 0.0.0
COMMIT := $(shell git rev-parse HEAD)

CURRENT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
DEFAULT_BRANCH := main

help: ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

clean-venv: ## re-create virtual env
	[[ -e .venv ]] && rm -rf .venv; \
	python3 -m venv .venv; \
	( \
       . .venv/bin/activate; \
       pip install --upgrade pip; \
       pip install -r requirements.txt; \
    )

pylint: ## run pylint on python files
	( \
       . .venv/bin/activate; \
       find . -type f -name "*.py"  -not -path "./.venv/*" | xargs pylint --max-line-length=90; \
    )

black: ## use black to format python files
	( \
       . .venv/bin/activate; \
       find . -type f -name "*.py" -not -path "./.venv/*" | xargs black; \
    )

unittest: ## run test that don't require deployed resources
	( \
       source .venv/bin/activate; \
       python3 -m pytest -v -m "not deployment" tests/; \
    )

clean-cache: ## clean python adn pytest cache data
	@find . -type f -name "*.py[co]" -delete -not -path "./.venv/*"
	@find . -type d -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} \;
	@rm -rf .pytest_cache

git-status: ## require status is clean so we can use undo_edits to put things back
	@status=$$(git status --porcelain); \
	if [ ! -z "$${status}" ]; \
	then \
		echo "Error - working directory is dirty. Commit those changes!"; \
		exit 1; \
	fi



.PHONY: build static test artifact
