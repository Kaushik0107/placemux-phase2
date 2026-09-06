import pytest
from matching.item_bank_onboarding import bulk_onboard_students, analyze_item_bank_quality

def test_bulk_onboard_students():
    students = [{"student_id": "S1", "skills": ["Python"]}, {"student_id": "S2", "skills": ["SQL"]}]
    res = bulk_onboard_students(students)
    assert res["total_onboarded"] == 2
    assert res["status"] == "SUCCESS"

def test_analyze_item_bank_quality():
    items = [
        {"item_id": "Q1", "discrimination_index": 0.5, "error_rate": 0.3},
        {"item_id": "Q2", "discrimination_index": 0.1, "error_rate": 0.88}
    ]
    res = analyze_item_bank_quality(items)
    assert res["total_items_analyzed"] == 2
    assert res["weak_items_count"] == 1
    assert res["weak_item_flags"][0]["item_id"] == "Q2"