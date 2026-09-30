# Common tasks. Run `make help` to list them.
PYTHON ?= python3
VENV   := .venv
BIN    := $(VENV)/bin
BATCH  ?= 2024-03-04
BATCHES := 2024-03-04 2024-03-05
DOCKER := docker compose run --rm spark

.PHONY: help setup check test run run-all clean docker-build docker-check docker-test docker-run docker-run-all docker-shell

help:           ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-16s %s\n", $$1, $$2}'

# ---------- Local (needs Python 3.10-3.11 and Java 17 on your machine) ----------
setup:          ## Create .venv and install dependencies
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt

check:          ## Verify Java + PySpark work (runs a tiny Spark job)
	PYTHONPATH=src $(BIN)/python scripts/check_env.py

test:           ## Run the test suite
	$(BIN)/pytest

run:            ## Run the pipeline for one batch: make run BATCH=2024-03-05
	PYTHONPATH=src $(BIN)/python -m pipeline.main --batch-date $(BATCH)

run-all:        ## Run the pipeline for all three batches in order
	@for b in $(BATCHES); do PYTHONPATH=src $(BIN)/python -m pipeline.main --batch-date $$b || exit 1; done

clean:          ## Delete pipeline outputs
	rm -rf output spark-warehouse metastore_db derby.log

# ---------- Docker (only needs Docker Desktop / Docker Engine) ----------
docker-build:   ## Build the container image
	docker compose build

docker-check:   ## Verify the environment inside Docker
	$(DOCKER) python scripts/check_env.py

docker-test:    ## Run tests inside Docker
	$(DOCKER) pytest

docker-run:     ## Run one batch inside Docker: make docker-run BATCH=2024-03-05
	$(DOCKER) python -m pipeline.main --batch-date $(BATCH)

docker-run-all: ## Run all batches inside Docker
	@for b in $(BATCHES); do $(DOCKER) python -m pipeline.main --batch-date $$b || exit 1; done

docker-shell:   ## Open a shell in the container
	$(DOCKER) bash
