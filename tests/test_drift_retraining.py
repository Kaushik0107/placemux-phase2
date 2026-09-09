import pytest
from matching.drift_retraining import detect_feature_drift, execute_model_retraining

def test_detect_feature_drift_no_drift():
    ref = [0.1, 0.2, 0.3, 0.4, 0.5] * 10
    curr = [0.11, 0.21, 0.31, 0.41, 0.51] * 10
    res = detect_feature_drift(ref, curr)
    assert res["drift_detected"] == False

def test_detect_feature_drift_with_drift():
    ref = [0.1, 0.2, 0.3, 0.4, 0.5] * 10
    curr = [0.9, 0.92, 0.95, 0.98, 0.99] * 10
    res = detect_feature_drift(ref, curr)
    assert res["drift_detected"] == True

def test_execute_model_retraining():
    samples = [{"feature_val": 0.1, "label": 0}, {"feature_val": 0.9, "label": 1}] * 10
    res = execute_model_retraining(samples)
    assert res["retrain_status"] == "SUCCESS"
    assert res["samples_trained"] == 20