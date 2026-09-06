import pytest
from matching.rec_validation import validate_recommendation_quality, get_college_placement_portal_view

def test_validate_recommendation_quality():
    recs = [
        {"student_id": "S1", "recommended_job_ids": ["J1", "J2"], "relevant_job_ids": ["J1", "J2"]}
    ]
    res = validate_recommendation_quality(recs)
    assert res["mean_precision"] == 1.0
    assert res["status"] == "VALIDATED"

def test_tenant_data_isolation_success():
    candidates = [{"student_id": "S1", "college_id": "COL_A"}]
    res = get_college_placement_portal_view("COL_A", "COL_A", candidates)
    assert res["access_granted"] is True
    assert res["total_candidates"] == 1

def test_tenant_data_isolation_unauthorized_leak_prevented():
    candidates = [{"student_id": "S1", "college_id": "COL_A"}]
    res = get_college_placement_portal_view("COL_A", "COL_B", candidates)
    assert res["access_granted"] is False
    assert res["error_code"] == 403