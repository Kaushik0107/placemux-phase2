import pytest
from matching.launch_signoff import execute_fairness_close_and_signoff

def test_launch_signoff_pass():
    candidates = [
        {"student_id": "S1", "group": "A", "is_shortlisted": 1},
        {"student_id": "S2", "group": "B", "is_shortlisted": 1}
    ]
    res = execute_fairness_close_and_signoff(candidates, "TestModel")
    assert res["launch_ready"] is True
    assert res["signoff_status"] == "SIGNED_OFF"

def test_launch_signoff_fail():
    candidates = [
        {"student_id": "S1", "group": "A", "is_shortlisted": 1},
        {"student_id": "S2", "group": "A", "is_shortlisted": 1},
        {"student_id": "S3", "group": "B", "is_shortlisted": 0},
        {"student_id": "S4", "group": "B", "is_shortlisted": 0}
    ]
    res = execute_fairness_close_and_signoff(candidates, "TestModel")
    assert res["launch_ready"] is False
    assert res["signoff_status"] == "REJECTED_BIAS_THRESHOLD"