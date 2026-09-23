import pytest
from matching.personalization_engine import recommend_jobs_for_candidate, evaluate_offline_recommendation_quality

def test_recommend_jobs_for_candidate():
    cand = {"candidate_id": "STU_1", "skills": ["Python", "FastAPI"], "preferred_category": "Backend"}
    res = recommend_jobs_for_candidate(cand, top_k=2)
    assert len(res["recommendations"]) == 2
    assert res["slo_met"] is True
    assert "reasons" in res["recommendations"][0]

def test_evaluate_offline_recommendation_quality():
    res = evaluate_offline_recommendation_quality()
    assert res["metrics"]["precision_at_k"] > res["metrics"]["baseline_precision"]
    assert res["popularity_collapse_detected"] is False