"""Sanity check: confirms Java, PySpark and the sample data are all usable.

Run with `make check` (local) or `make docker-check` (Docker).
"""
import platform
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pipeline import config  # noqa: E402
from pipeline.spark import get_spark  # noqa: E402


def main() -> int:
    print(f"Python  : {sys.version.split()[0]} ({platform.system()} {platform.machine()})")
    java = shutil.which("java")
    if not java:
        print("Java    : NOT FOUND. Install Java 17 or use the Docker workflow (see README).")
        return 1
    ver = subprocess.run([java, "-version"], capture_output=True, text=True).stderr.splitlines()[0]
    print(f"Java    : {ver}")

    spark = get_spark("env-check")
    print(f"PySpark : {spark.version}")
    total = spark.range(1_000_000).selectExpr("sum(id) AS total").collect()[0]["total"]
    assert total == 499999500000, total
    print("Spark   : local job OK")

    batches = sorted(p.name for p in config.RAW_FILINGS_DIR.iterdir() if p.is_dir())
    print(f"Data    : {len(batches)} filings batches -> {', '.join(batches)}")
    found = "found" if config.RAW_COMPANIES_PATH.exists() else "MISSING"
    print(f"Data    : companies reference {found}")
    spark.stop()
    print("\nEnvironment looks good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
