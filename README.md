# SEC Data Engineering Take-Home

The task is described in the assignment document. This repository gives you a
working local PySpark environment, the sample data and a skeleton to start from.

```
data/raw/filings/ingest_date=2024-03-04/filings.csv   batch 1
data/raw/filings/ingest_date=2024-03-05/filings.csv   batch 2
data/raw/companies/companies.csv                      company reference data
src/pipeline/main.py                                  entry point (start here)
src/pipeline/config.py, spark.py                      paths and a local SparkSession
tests/                                                pytest, with a shared `spark` fixture
NOTES.md                                              short questions to answer
```

## Setup (pick one, about 10 minutes)

**Docker** (recommended; any OS):

```bash
make docker-build && make docker-check    # ends with "Environment looks good."
make docker-run BATCH=2024-03-04
make docker-test
```

Without `make`: `docker compose build`, then
`docker compose run --rm spark python -m pipeline.main --batch-date 2024-03-04`
and `docker compose run --rm spark pytest`.

**Local Python** (needs Python 3.10-3.12 and Java 17; on Windows use Docker or WSL2):

```bash
make setup && make check
make run BATCH=2024-03-04
make test
```

`make run-all` / `make docker-run-all` runs both batches in order. `make clean` deletes `output/`.

If setup takes more than 15 minutes, email us; that time will not count.

## Submitting

Zip the repository (without `.venv/` and `output/`) or share a private Git repository.
