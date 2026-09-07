import pytest
from matching.fairness_audit import run_fairness_bias_audit, process_dpdp_data_erasure

def test_run_fairness_bias_audit_fair():
    candidates = [
        {"student_id": "S1", "group": "A", "is_shortlisted": 1},
        {"student_id": "S2", "group": "A", "is_shortlisted": 0},
        {"student_id": "S3", "group": "B", "is_shortlisted": 1},
        {"student_id": "S4", "group": "B", "is_shortlisted": 0},
    ]
    res = run_fairness_bias_audit(candidates, "group")
    assert res["passes_four_fifths_rule"] is True
    assert res["audit_status"] == "FAIR"

def test_process_dpdp_data_erasure():
    res = process_dpdp_data_erasure("STU_99")
    assert res["erasure_status"] == "COMPLETED"
    assert "profile" in res["records_purged"]