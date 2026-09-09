import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.ensemble import GradientBoostingClassifier

def detect_feature_drift(reference_data: list[float], current_data: list[float], threshold: float = 0.05) -> dict:
    """
    Performs Kolmogorov-Smirnov (KS) test to detect statistical feature distribution drift.
    """
    ks_stat, p_value = ks_2samp(reference_data, current_data)
    drift_detected = bool(p_value < threshold)  # Cast np.bool_ to standard Python bool

    return {
        "ks_statistic": round(float(ks_stat), 4),
        "p_value": round(float(p_value), 4),
        "drift_threshold": threshold,
        "drift_detected": drift_detected,
        "explanation": f"KS statistic is {ks_stat:.4f} (p-value: {p_value:.4f}). " +
                       ("Significant feature drift detected! Retraining recommended." if drift_detected else "Feature distribution remains stable.")
    }

def execute_model_retraining(new_training_data: list[dict]) -> dict:
    """
    Executes automated model retraining on newly acquired production data.
    """
    df = pd.DataFrame(new_training_data)
    if 'feature_val' not in df.columns or 'label' not in df.columns:
        return {"status": "ERROR", "message": "Missing required fields for retraining."}

    X = df[['feature_val']]
    y = df['label']

    model = GradientBoostingClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    acc = model.score(X, y)

    return {
        "retrain_status": "SUCCESS",
        "samples_trained": len(df),
        "retrained_accuracy": round(float(acc), 4),
        "explanation": f"Model successfully retrained on {len(df)} new samples with accuracy of {acc:.2%}."
    }

if __name__ == "__main__":
    np.random.seed(42)
    ref_data = np.random.normal(0.5, 0.1, 100).tolist()
    curr_data_stable = np.random.normal(0.51, 0.1, 100).tolist()
    curr_data_drifted = np.random.normal(0.80, 0.1, 100).tolist()

    print("--- DRIFT MONITORING (STABLE DATA) ---")
    print(detect_feature_drift(ref_data, curr_data_stable))

    print("\n--- DRIFT MONITORING (DRIFTED DATA) ---")
    print(detect_feature_drift(ref_data, curr_data_drifted))

    mock_train = [{"feature_val": x, "label": 1 if x > 0.5 else 0} for x in curr_data_drifted]
    print("\n--- AUTOMATED RETRAINING ---")
    print(execute_model_retraining(mock_train))