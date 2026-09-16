import pytest
from matching.scale_load_test import execute_concurrency_load_test, get_horizontal_scaling_plan

def test_execute_load_test_within_capacity():
    res = execute_concurrency_load_test(target_qps=300, breaking_point_qps=500)
    assert res["system_degraded"] is False
    assert res["fallback_activated"] is False

def test_execute_load_test_exceeding_capacity():
    res = execute_concurrency_load_test(target_qps=700, breaking_point_qps=500)
    assert res["system_degraded"] is True
    assert res["fallback_activated"] is True
    assert res["fallback_mode"] == "RULE_BASED_PRECOMPUTE_CACHE"

def test_get_horizontal_scaling_plan():
    res = get_horizontal_scaling_plan()
    assert res["devops_hand-off_ready"] is True
    assert res["scaling_architecture"]["min_replicas"] == 3