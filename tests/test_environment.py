"""Smoke tests that pass out of the box. Add your own tests in new files."""
from pyspark.sql import functions as F

from pipeline import config


def test_spark_runs(spark):
    assert spark.range(10).count() == 10


def test_raw_data_present():
    batches = sorted(p.name for p in config.RAW_FILINGS_DIR.iterdir() if p.is_dir())
    assert batches == ["ingest_date=2024-03-04", "ingest_date=2024-03-05"]
    assert config.RAW_COMPANIES_PATH.exists()


def test_example(spark):
    df = spark.createDataFrame([(" 10-k ",)], ["form_type"])
    assert df.select(F.upper(F.trim("form_type"))).first()[0] == "10-K"
