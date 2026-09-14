import pytest
from matching.slo_observability import evaluate_inference_slos

def test_evaluate_inference_slos_passed():
    logs = [
        {"latency_ms": 20.0, "is_error": False, "prediction_score": 0.2},
        {"latency_ms": 30.0, "is_error": False, "prediction_score": 0.8}
    ]
    res = evaluate_inference_slos(logs, p95_target_ms=100.0)
    assert res["slo_status"] == "PASSED"
    assert len(res["alerts_triggered"]) == 0

def test_evaluate_inference_slos_latency_breach():
    logs = [{"latency_ms": 150.0, "is_error": False, "prediction_score": 0.5}] * 10
    res = evaluate_inference_slos(logs, p95_target_ms=100.0)
    assert res["slo_status"] == "BREACHED"
    assert any("LATENCY_BREACH" in alert for alert in res["alerts_triggered"])

def test_evaluate_inference_slos_degenerate_output():
    logs = [{"latency_ms": 20.0, "is_error": False, "prediction_score": 0.77}] * 10
    res = evaluate_inference_slos(logs)
    assert res["slo_status"] == "BREACHED"
    assert any("DEGENERATE_OUTPUT_ALERT" in alert for alert in res["alerts_triggered"])