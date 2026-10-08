# Data Engineer (SEC)

Your goal is to design and implement a small, automated PySpark data pipeline for ingesting and transforming financial data and demonstrate your approach during the technical interview.

You may use AI tools such as ChatGPT, GitHub Copilot, or similar tools. If you do, you should be prepared to explain what you used AI for, what you changed or validated yourself, and why you made your final implementation decisions.


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


## Context

You are a Data Engineer working on a team responsible for moving financial data from source systems into an analytical data warehouse.

Your team is building automated data pipelines that:
- Extract data from source systems.
- Transform and validate the data.
- Load the results into a data warehouse.
- Make the data available to downstream reporting and analytical applications.

The source systems contain information about financial securities.


## The task

Your task is to build an automated data pipeline that ingests SEC filing records, one batch at a time.

For this exercise, you have been provided with the files listed below:

| **File Name** | **Purpose** |
| --- | --- |
| data/raw/filings/ingest_date=2024-03-04/filings.csv | batch 1 |
| data/raw/filings/ingest_date=2024-03-05/filings.csv | batch 2 |
| data/raw/companies/companies.csv | company reference data |
| src/pipeline/main.py | entry point (start here) |
| src/pipeline/config.py, spark.py | paths and a local SparkSession |
| tests/ | pytest, with a shared `spark` fixture |
| NOTES.md | short questions to answer |

The repository contains two daily batches of SEC filing records (data/raw/filings/, about 400 rows each) and a list of companies (data/raw/companies/companies.csv). The data is synthetic and deliberately messy.

Write a PySpark pipeline that processes one batch per run as described below:

```
python -m pipeline.main --batch-date 2024-03-04
# or: make run BATCH=2024-03-04
```

Your pipeline should:
1. **Clean** the data to match the rules below, fixing values that can be fixed safely. 
2. **Quarantine** rows that break a rule: write them to output/quarantine/ with a reason. 
3. **Publish** `output/curated/` (Parquet) with exactly one row per accession_number: its newest version by updated_at. 
4. **Be safe to re-run.** Running a batch twice, or running the two batches in either order, must produce the same curated output. 
5. **Check itself.** Add a few data quality checks that stop the run with a non-zero exit code if they fail, and a few pytest tests, including one for point 4. 
Then answer the five short questions in `NOTES.md` (a few bullet points each).


## Data Rules

| **Column** | **Rule** |
| --- | --- |
| accession_number | Required. Identifies a filing. The same filing may appear more than once, and may be re-sent in a later batch. |
| cik | Required. Company identifier, stored as 10 digits with leading zeros (e.g. 0000320193). Must exist in the companies file. |
| form_type | Required. One of 10-K, 10-Q, 8-K, 4, S-1, DEF 14A. |
| filing_date | Required. A real date, stored as a date type, and not later than the batch date. |
| total_assets | Optional. If present, a number that is zero or more. |
| updated_at | Required. UTC timestamp of the record's last change. For the same filing, the latest updated_at is the current version. |


## What to submit

- Your completed assignment should be committed and pushed to the GitHub repo we sent you containing the initial set of files.
- Ensure the repository includes a `NOTES.md` file with your answers.
- Please make sure `make run-all` and `make test` (or their `docker-` versions) work from a fresh copy.
- If setup takes more than 15 minutes, or anything is unclear, email us. Setup time does not count.
- Reply to our HR team's email with the link to your repository to confirm completion.


## What we're looking at

We will evaluate the submission based on:

- Correct output: bad rows are caught, fixable rows are fixed, and nothing goes missing.
- A design that is safe to re-run and would still work if the data were much larger.
- Sensible data quality checks and tests.
- Clear explanations of your choices, and an understanding of the code you submit. There is no single right answer where the rules leave room for judgement; tell us what you chose and why.

You do not need prior experience with the SEC's AWS stack (Airflow, Glue, S3, Iceberg, Athena). We will simply ask how you think your design would carry over.


## Interview Discussion

During the interview, you will have approximately 10–15 minutes to walk us through your solution.

Be prepared to show the pipeline running, walk us through your approach, and then we will discuss it. No slides are needed.
