import pytest
from matching.live_monitoring import record_inference_telemetry, evaluate_production_health, TELEMETRY_LOGS

def test_live_monitoring_healthy():
    TELEMETRY_LOGS.clear()
    for i in range(20):
        record_inference_telemetry("/matching", 25.0, False)
    
    res = evaluate_production_health()
    assert res["health_status"] == "HEALTHY"
    assert res["cutover_signoff"] is True
    assert res["total_requests"] == 20

def test_live_monitoring_unhealthy():
    TELEMETRY_LOGS.clear()
    for i in range(20):
        record_inference_telemetry("/matching", 250.0, True)
    
    res = evaluate_production_health()
    assert res["health_status"] == "UNHEALTHY_DEGRADED"
    assert res["cutover_signoff"] is False