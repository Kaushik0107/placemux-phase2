import pytest
from matching.latency_profiler import profile_unoptimized_inference_path, profile_optimized_inference_path

def test_profile_unoptimized_inference_path():
    res = profile_unoptimized_inference_path(num_candidates=50)
    assert res["pipeline_mode"] == "UNOPTIMIZED_BASELINE"
    assert res["total_p95_latency_ms"] > 50.0

def test_profile_optimized_inference_path():
    res = profile_optimized_inference_path(num_candidates=50)
    assert res["pipeline_mode"] == "OPTIMIZED_PRODUCTION"
    assert res["total_p95_latency_ms"] < 50.0
    assert res["quality_score_retained"] is True