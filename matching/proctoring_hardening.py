import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

def evaluate_proctoring_hardening(sample_data: list[dict]):
    """
    Evaluates baseline rule vs. hardened machine learning model 
    for proctoring flags to demonstrate False Positive Rate (FPR) reduction.
    """
    df = pd.DataFrame(sample_data)
    
    # Required signals for proctoring analysis
    feature_cols = ['gaze_off_screen_ratio', 'audio_anomaly_count', 'tab_switches', 'session_duration']
    X = df[feature_cols]
    y = df['is_flagged_cheating']

    # Held-out split for objective metrics evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Baseline rule-based evaluation (simple threshold triggering)
    baseline_preds = (X_test['tab_switches'] > 2) | (X_test['gaze_off_screen_ratio'] > 0.25)
    tn_b, fp_b, fn_b, tp_b = confusion_matrix(y_test, baseline_preds).ravel()
    baseline_fpr = fp_b / (fp_b + tn_b) if (fp_b + tn_b) > 0 else 0.0

    # Train Hardened Model
    model = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate Hardened Model
    y_pred = model.predict(X_test)
    tn_m, fp_m, fn_m, tp_m = confusion_matrix(y_test, y_pred).ravel()
    model_fpr = fp_m / (fp_m + tn_m) if (fp_m + tn_m) > 0 else 0.0

    print("=== PROCTORING HARDENING EVALUATION ===")
    print(f"Baseline False Positive Rate (FPR): {baseline_fpr:.2%}")
    print(f"Hardened Model False Positive Rate (FPR): {model_fpr:.2%}")
    print("\nDetailed Classification Metrics:")
    print(classification_report(y_test, y_pred))

    return model

if __name__ == "__main__":
    # Sample real-shaped synthetic test data for local verification
    np.random.seed(42)
    n_samples = 200
    mock_data = []
    for i in range(n_samples):
        tab_switches = np.random.randint(0, 8)
        gaze_off = np.random.uniform(0.0, 0.6)
        audio_anomalies = np.random.randint(0, 5)
        duration = np.random.randint(1800, 3600)
        
        # Ground truth flag definition
        is_cheating = 1 if (tab_switches > 4 and gaze_off > 0.35) else 0
        
        mock_data.append({
            "student_id": f"STU_{i+1000}",
            "tab_switches": tab_switches,
            "gaze_off_screen_ratio": gaze_off,
            "audio_anomaly_count": audio_anomalies,
            "session_duration": duration,
            "is_flagged_cheating": is_cheating
        })

    evaluate_proctoring_hardening(mock_data)