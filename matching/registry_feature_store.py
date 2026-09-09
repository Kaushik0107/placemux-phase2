import time

# In-memory persistence for Feature Store and Model Registry
FEATURE_STORE = {}
MODEL_REGISTRY = {}

def store_entity_features(entity_id: str, features: dict) -> dict:
    """
    Stores offline/online feature sets for candidates or job descriptions.
    """
    FEATURE_STORE[entity_id] = {
        "features": features,
        "updated_at": time.time()
    }
    return {
        "entity_id": entity_id,
        "status": "STORED",
        "feature_count": len(features),
        "explanation": f"Stored {len(features)} features for entity '{entity_id}' in feature store."
    }

def get_entity_features(entity_id: str) -> dict:
    """
    Retrieves entity features from the Feature Store.
    """
    if entity_id not in FEATURE_STORE:
        return {"found": False, "features": {}}
    return {"found": True, "entity_id": entity_id, "features": FEATURE_STORE[entity_id]["features"]}

def register_model_version(model_name: str, version: str, metrics: dict, stage: str = "STAGING") -> dict:
    """
    Registers model versions and stage promotions in the central Model Registry.
    """
    if model_name not in MODEL_REGISTRY:
        MODEL_REGISTRY[model_name] = {}

    MODEL_REGISTRY[model_name][version] = {
        "metrics": metrics,
        "stage": stage,
        "registered_at": time.time()
    }
    
    return {
        "model_name": model_name,
        "version": version,
        "stage": stage,
        "status": "REGISTERED",
        "explanation": f"Model '{model_name}' v{version} registered in stage '{stage}'."
    }

if __name__ == "__main__":
    # Test Feature Store
    res_feat = store_entity_features("STU_1029", {"verified_skill_score": 92, "experience_years": 3})
    print("--- FEATURE STORE OUTPUT ---")
    print(res_feat)

    # Test Model Registry
    res_reg = register_model_version("RankingModel", "1.2.0", {"f1_score": 0.94}, stage="PRODUCTION")
    print("\n--- MODEL REGISTRY OUTPUT ---")
    print(res_reg)