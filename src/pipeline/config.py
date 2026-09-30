"""Input and output paths, relative to the repository root.
In production these would be S3 URIs; keeping them here makes that a config change."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_FILINGS_DIR = REPO_ROOT / "data" / "raw" / "filings"   # ingest_date=YYYY-MM-DD/filings.csv
RAW_COMPANIES_PATH = REPO_ROOT / "data" / "raw" / "companies" / "companies.csv"

OUTPUT_DIR = REPO_ROOT / "output"
CURATED_DIR = OUTPUT_DIR / "curated"          # required: cleaned filings, one row per filing
QUARANTINE_DIR = OUTPUT_DIR / "quarantine"    # required: rejected rows + reason


def raw_filings_path(batch_date: str) -> Path:
    return RAW_FILINGS_DIR / f"ingest_date={batch_date}"
