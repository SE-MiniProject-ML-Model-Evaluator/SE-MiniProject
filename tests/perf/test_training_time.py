"""NFR-02 / TC-13 step 2: every catalogue model trains on 10,000 x 20 rows within 60 s.

Slow, so excluded from the default run. Run it with:  pytest -m perf
"""
import importlib.util
import pathlib

import pytest

spec = importlib.util.spec_from_file_location(
    "benchmark_training", pathlib.Path(__file__).resolve().parents[2] / "scripts" / "benchmark_training.py")
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


@pytest.mark.perf
@pytest.mark.django_db
def test_each_model_trains_within_60_seconds():
    results = benchmark.run_benchmark(use_test_db=True)
    assert len(results) == 8
    for task, label, seconds, status in results:
        assert status == "completed", f"{label} {status}"
        assert seconds <= benchmark.LIMIT_S, f"{label} took {seconds} s"
