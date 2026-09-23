import pytest
from matching.ltr_ranking_v2 import train_and_eval_ltr_model, apply_position_bias_correction, calculate_ndcg_at_k

def test_position_bias_correction():
    weight_p1 = apply_position_bias_correction(1)
    weight_p4 = apply_position_bias_correction(4)
    assert weight_p4 > weight_p1  # Lower positions receive higher IPS weight boost

def test_calculate_ndcg_at_k():
    ndcg = calculate_ndcg_at_k([1.0, 1.0, 0.0, 0.0], k=3)
    assert 0.0 <= ndcg <= 1.0

def test_train_and_eval_ltr_model():
    sample = [
        {"position": 1, "skill_match_score": 0.9, "experience_match_score": 0.8, "role_category_fit": 1.0, "conversion_label": 1.0},
        {"position": 2, "skill_match_score": 0.7, "experience_match_score": 0.9, "role_category_fit": 1.0, "conversion_label": 1.0},
        {"position": 3, "skill_match_score": 0.4, "experience_match_score": 0.2, "role_category_fit": 0.0, "conversion_label": 0.0}
    ]
    res = train_and_eval_ltr_model(sample, k=3)
    assert res["ranking_model"] == "GradientBoosted_LTR_v2"
    assert "ltr_ndcg_at_k" in res["eval_metrics"]
    assert res["ready_for_online_ab_test"] is True