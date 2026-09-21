import pytest
from matching.experiment_readout import pre_register_hypothesis, evaluate_ab_test_readout

def test_pre_register_hypothesis():
    res = pre_register_hypothesis("EXP_1", "Test hypothesis", "ctr")
    assert res["status"] == "SUCCESS"
    assert res["data"]["experiment_id"] == "EXP_1"

def test_evaluate_ab_test_readout_ship():
    pre_register_hypothesis("EXP_WIN", "Win test", "ctr")
    res = evaluate_ab_test_readout("EXP_WIN", 100, 1000, 180, 1000)
    assert res["decision"] == "SHIP_TO_PRODUCTION"
    assert res["ship_recommended"] is True
    assert res["metrics"]["statistically_significant"] is True

def test_evaluate_ab_test_readout_guardrail_breach():
    pre_register_hypothesis("EXP_FAIL", "Fail test", "ctr")
    res = evaluate_ab_test_readout("EXP_FAIL", 100, 1000, 180, 1000, guardrail_breached=True)
    assert res["decision"] == "DO_NOT_SHIP_GUARDRAIL_BREACH"
    assert res["ship_recommended"] is False