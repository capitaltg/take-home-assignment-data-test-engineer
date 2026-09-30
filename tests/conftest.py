"""Shared fixtures. Use pytest's built-in `tmp_path` for tests that write files."""
import pytest

from pipeline.spark import get_spark


@pytest.fixture(scope="session")
def spark():
    session = get_spark("pytest")
    yield session
    session.stop()
