import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix, classification_report

def evaluate_fp_reduction(session_data: list[dict]):
    """
    Evaluates rule baseline vs. FP-reduced model on flagged-session data.
    """
    df = pd.DataFrame(session_data)
    feature_cols = ['gaze_off_screen_ratio', 'audio_anomaly_count', 'tab_switches', 'session_duration']
    X = df[feature_cols]
    y = df['is_truly_flagged']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 1. Rule Baseline (Prone to high false positives)
    baseline_preds = (X_test['tab_switches'] > 1) | (X_test['gaze_off_screen_ratio'] > 0.20)
    tn_b, fp_b, fn_b, tp_b = confusion_matrix(y_test, baseline_preds).ravel()
    baseline_fpr = fp_b / (fp_b + tn_b) if (fp_b + tn_b) > 0 else 0.0

    # 2. Hardened FP Reduction Model
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    tn_m, fp_m, fn_m, tp_m = confusion_matrix(y_test, y_pred).ravel()
    model_fpr = fp_m / (fp_m + tn_m) if (fp_m + tn_m) > 0 else 0.0

    print("=== TASK 13: FP REDUCTION EVALUATION ===")
    print(f"Baseline False Positive Rate (FPR): {baseline_fpr:.2%}")
    print(f"Hardened FP-Reduced Model FPR:     {model_fpr:.2%}")
    print("\nDetailed Metrics:")
    print(classification_report(y_test, y_pred))

    return model

def schedule_interview(student_id: str, job_id: str, slot: str) -> dict:
    """
    Schedules an interview slot for verified candidates.
    """
    return {
        "schedule_id": f"SCHED_{hash(student_id + slot) % 10000}",
        "student_id": student_id,
        "job_id": job_id,
        "slot": slot,
        "status": "CONFIRMED"
    }

if __name__ == "__main__":
    np.random.seed(42)
    mock_sessions = []
    for i in range(150):
        tab_switches = np.random.randint(0, 6)
        gaze_off = np.random.uniform(0.0, 0.5)
        audio_anomalies = np.random.randint(0, 4)
        duration = np.random.randint(1800, 3600)
        
        # Ground truth flag definition
        is_truly_flagged = 1 if (tab_switches >= 4 and gaze_off > 0.35) else 0

        mock_sessions.append({
            "session_id": f"SESS_{i+100}",
            "tab_switches": tab_switches,
            "gaze_off_screen_ratio": gaze_off,
            "audio_anomaly_count": audio_anomalies,
            "session_duration": duration,
            "is_truly_flagged": is_truly_flagged
        })

    evaluate_fp_reduction(mock_sessions)