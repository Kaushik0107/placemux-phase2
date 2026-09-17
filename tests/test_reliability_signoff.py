import pytest
from matching.reliability_signoff import execute_load_test_simulation, generate_reliability_signoff

def test_load_test_simulation_healthy():
    res = execute_load_test_simulation(target_rps=200, duration_sec=0.5, force_failure=False)
    assert res["slo_compliance"] is True
    assert res["fallback_status"]["fallback_engaged"] is False

def test_load_test_simulation_forced_failure():
    res = execute_load_test_simulation(target_rps=200, duration_sec=0.5, force_failure=True)
    assert res["slo_compliance"] is False
    assert res["fallback_status"]["fallback_engaged"] is True

def test_generate_reliability_signoff():
    load_res = execute_load_test_simulation(target_rps=200, duration_sec=0.5, force_failure=False)
    signoff = generate_reliability_signoff(load_res)
    assert signoff["signoff_status"] == "SIGNED_OFF_SCALE_READY"