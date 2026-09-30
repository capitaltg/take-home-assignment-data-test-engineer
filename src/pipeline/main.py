"""Pipeline entry point. Interviewers will run, from the repo root:

    python -m pipeline.main --batch-date 2024-03-04

Exit with a non-zero status if the run fails (including a failed data quality check).
The starter code below just reads the batch so you can confirm your setup works.
Replace it with your pipeline; add modules as you see fit.
"""
import argparse
import sys

from pipeline import config
from pipeline.spark import get_spark


def run(batch_date: str) -> int:
    spark = get_spark()
    path = config.raw_filings_path(batch_date)
    if not path.exists():
        print(f"No raw batch found at {path}", file=sys.stderr)
        return 1

    raw = spark.read.option("header", True).csv(str(path))
    print(f"Batch {batch_date}: {raw.count()} raw rows")
    raw.show(5, truncate=False)

    # TODO: clean, validate, quarantine, de-duplicate, write curated output, check quality
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-date", required=True, help="YYYY-MM-DD")
    return run(parser.parse_args(argv).batch_date)


if __name__ == "__main__":
    sys.exit(main())
