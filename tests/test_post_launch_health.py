import pytest
from matching.post_launch_health import generate_model_health_report, triage_intelligence_defects

def test_generate_model_health_report():
    logs = [
        {"student_id": "S1", "job_id": "J1", "predicted_match": 1, "user_accepted": 1},
        {"student_id": "S2", "job_id": "J1", "predicted_match": 1, "user_accepted": 0},
    ]
    res = generate_model_health_report(logs, offline_f1_baseline=0.90)
    assert res["health_status"] == "DEGRADED"
    assert res["offline_online_gap"] > 0

def test_triage_intelligence_defects():
    logs = [
        {"student_id": "S1", "job_id": "J1", "predicted_match": 1, "user_accepted": 0, "missing_skill": "Docker"}
    ]
    res = triage_intelligence_defects(logs)
    assert res["total_defects_found"] == 1
    assert res["ranked_defects"][0]["defect_type"] == "HIGH_CONFIDENCE_FALSE_POSITIVE"
    assert len(res["phase3_backlog_items"]) > 0