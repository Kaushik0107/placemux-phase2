import pytest
from matching.cold_start_recommendation import generate_cold_start_recommendations, evaluate_cold_start_lift

def test_generate_cold_start_recommendations():
    user = {"user_id": "NEW_1", "preferred_role": "Software Engineering", "skills": ["Python"]}
    res = generate_cold_start_recommendations(user, top_k=2)
    assert len(res["recommendations"]) == 2
    assert res["fallback_activated"] is False
    assert res["recommendations"][0]["relevance_score"] > 0

def test_generate_cold_start_recommendations_sparse_profile():
    user = {"user_id": "NEW_2", "preferred_role": None, "skills": []}
    res = generate_cold_start_recommendations(user, top_k=2)
    assert len(res["recommendations"]) == 2
    assert res["recommendations"][0]["job_id"] is not None

def test_evaluate_cold_start_lift():
    res = evaluate_cold_start_lift(0.10, 0.25)
    assert res["conversion_lift_percent"] == 150.0