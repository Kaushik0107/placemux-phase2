import pytest
from matching.registry_feature_store import store_entity_features, get_entity_features, register_model_version

def test_feature_store_flow():
    res_store = store_entity_features("STU_100", {"score": 88})
    assert res_store["status"] == "STORED"

    res_get = get_entity_features("STU_100")
    assert res_get["found"] is True
    assert res_get["features"]["score"] == 88

def test_model_registry_flow():
    res_reg = register_model_version("ProctorModel", "2.0.0", {"accuracy": 0.99}, "PRODUCTION")
    assert res_reg["status"] == "REGISTERED"
    assert res_reg["stage"] == "PRODUCTION"