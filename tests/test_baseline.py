"""
Baseline health checks for the Greenland REE dashboard.

These must pass on the bench-baseline tag and after every benchmark task.
Run from the repo root with:  pytest
"""
import importlib.util
import re
import sys
import warnings
from pathlib import Path

import pytest

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]

EXPECTED_COLUMNS = {
    "deposit_name", "latitude", "longitude", "resource_mt", "treo_grade_pct",
    "heavy_ree_pct", "owner", "chinese_stake_pct", "status", "uranium_ppm",
    "strategic_score", "geological_score", "regulatory_score", "ownership_score",
    "infrastructure_score", "geopolitical_score",
}


@pytest.fixture(scope="module")
def app_module():
    if "app_baseline" in sys.modules:
        del sys.modules["app_baseline"]
    spec = importlib.util.spec_from_file_location("app_baseline", ROOT / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_app_imports_without_error(app_module):
    assert hasattr(app_module, "load_data")


def test_load_data_shape(app_module):
    df = app_module.load_data()
    assert len(df) == 15, f"expected 15 deposits, got {len(df)}"
    missing = EXPECTED_COLUMNS - set(df.columns)
    assert not missing, f"missing columns: {missing}"


def test_scores_within_range(app_module):
    df = app_module.load_data()
    assert df["strategic_score"].between(0, 100).all()
    for col in ("geological_score", "regulatory_score", "ownership_score",
                "infrastructure_score", "geopolitical_score"):
        assert df[col].between(0, 100).all(), col


def test_requirements_cover_imports():
    src = (ROOT / "app.py").read_text(encoding="utf-8")
    imported = set(re.findall(r"^(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_]*)", src, re.M))
    reqs = {line.split("==")[0].split(">=")[0].split("<")[0].strip().lower()
            for line in (ROOT / "requirements.txt").read_text().splitlines() if line.strip()}
    aliases = {"streamlit": "streamlit", "plotly": "plotly", "pandas": "pandas", "numpy": "numpy"}
    for mod in imported:
        if mod in aliases:
            assert aliases[mod] in reqs, f"{mod} is imported but not in requirements.txt"


def test_app_runs_under_streamlit():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    assert not at.exception, f"app raised: {[e.value for e in at.exception]}"
