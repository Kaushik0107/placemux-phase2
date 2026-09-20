import pytest
from matching.churn_prediction import train_and_eval_churn_model, generate_at_risk_list

def test_churn_model_evaluation():
    sample = [
        {"entity_id": "U1", "days_since_last_login": 25, "applications_last_30d": 0, "profile_completeness_pct": 40, "churn_label": 1},
        {"entity_id": "U2", "days_since_last_login": 1, "applications_last_30d": 10, "profile_completeness_pct": 90, "churn_label": 0}
    ]
    res = train_and_eval_churn_model(sample)
    assert res["model_type"] == "RandomForest_14Day_Churn_Classifier"
    assert "model_pr_auc" in res["metrics"]

def test_generate_at_risk_list():
    sample = [
        {"entity_id": "U1", "days_since_last_login": 25, "applications_last_30d": 0, "profile_completeness_pct": 40, "churn_label": 1},
        {"entity_id": "U2", "days_since_last_login": 1, "applications_last_30d": 10, "profile_completeness_pct": 90, "churn_label": 0}
    ]
    res = generate_at_risk_list(sample, threshold=0.40)
    assert res["total_at_risk"] >= 1
    assert res["prioritized_at_risk_list"][0]["risk_level"] in ["CRITICAL", "HIGH"]