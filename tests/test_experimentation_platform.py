import pytest
from matching.experimentation_platform import assign_user_to_variant, evaluate_experiment_guardrails

def test_deterministic_user_routing():
    res1 = assign_user_to_variant("USER_500", "Exp1")
    res2 = assign_user_to_variant("USER_500", "Exp1")
    assert res1["variant"] == res2["variant"]  # Sticky routing
    assert res1["variant"] in ["CONTROL", "TREATMENT", "PERMANENT_HOLDOUT"]

def test_guardrails_healthy():
    metrics = {"variant": "TREATMENT", "mean_relevance_score": 0.85, "error_rate": 0.001}
    res = evaluate_experiment_guardrails(metrics)
    assert res["guardrail_status"] == "HEALTHY"
    assert res["auto_halt_triggered"] is False

def test_guardrails_auto_halt():
    metrics = {"variant": "TREATMENT", "mean_relevance_score": 0.40, "error_rate": 0.05}
    res = evaluate_experiment_guardrails(metrics)
    assert res["guardrail_status"] == "HALTED"
    assert res["auto_halt_triggered"] is True