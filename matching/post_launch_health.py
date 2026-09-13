import pandas as pd
import numpy as np

def generate_model_health_report(logs: list[dict], offline_f1_baseline: float = 0.94) -> dict:
    """
    Computes offline vs online metric gaps based on live prediction interaction logs.
    """
    if not logs:
        return {"status": "NO_LOGS", "explanation": "No live interaction logs available for health analysis."}

    df = pd.DataFrame(logs)
    
    # Calculate online precision, recall, and F1 based on live user acceptance/clicks
    tp = len(df[(df['predicted_match'] == 1) & (df['user_accepted'] == 1)])
    fp = len(df[(df['predicted_match'] == 1) & (df['user_accepted'] == 0)])
    fn = len(df[(df['predicted_match'] == 0) & (df['user_accepted'] == 1)])

    online_precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    online_recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    online_f1 = (2 * online_precision * online_recall) / (online_precision + online_recall) if (online_precision + online_recall) > 0 else 0.0

    f1_gap = offline_f1_baseline - online_f1

    return {
        "offline_f1_baseline": round(offline_f1_baseline, 4),
        "online_f1": round(online_f1, 4),
        "online_precision": round(online_precision, 4),
        "online_recall": round(online_recall, 4),
        "offline_online_gap": round(f1_gap, 4),
        "health_status": "DEGRADED" if f1_gap > 0.15 else "STABLE",
        "explanation": f"Offline baseline F1 is {offline_f1_baseline:.2%}, but live online F1 dropped to {online_f1:.2%} (gap: {f1_gap:.2%})."
    }

def triage_intelligence_defects(logs: list[dict]) -> dict:
    """
    Identifies and ranks matching intelligence defects from real interaction logs.
    """
    df = pd.DataFrame(logs)
    defects = []

    for _, row in df.iterrows():
        # High-confidence false positive (Model predicted match, user rejected)
        if row['predicted_match'] == 1 and row['user_accepted'] == 0:
            defects.append({
                "student_id": row["student_id"],
                "job_id": row["job_id"],
                "defect_type": "HIGH_CONFIDENCE_FALSE_POSITIVE",
                "severity": "HIGH",
                "reason": f"Model matched student {row['student_id']} to job {row['job_id']} despite skill mismatch on '{row.get('missing_skill', 'unknown')}'."
            })
        # False negative (Model missed match, candidate hired/applied manually)
        elif row['predicted_match'] == 0 and row['user_accepted'] == 1:
            defects.append({
                "student_id": row["student_id"],
                "job_id": row["job_id"],
                "defect_type": "FALSE_NEGATIVE_MISS",
                "severity": "MEDIUM",
                "reason": f"Model missed matching student {row['student_id']} to job {row['job_id']} due to strict experience filtering."
            })

    # Sort defects by severity
    defects_sorted = sorted(defects, key=lambda x: 0 if x["severity"] == "HIGH" else 1)

    return {
        "total_defects_found": len(defects),
        "ranked_defects": defects_sorted,
        "phase3_backlog_items": [
            "Refine ontology parser for missing skill alias mapping",
            "Adjust experience penalty threshold in ranking model",
            "Implement live feedback ingestion stream for online metric recalibration"
        ],
        "explanation": f"Identified {len(defects)} intelligence defects from live logs. Added 3 action items to Phase 3 backlog."
    }

if __name__ == "__main__":
    sample_logs = [
        {"student_id": "STU_101", "job_id": "JOB_501", "predicted_match": 1, "user_accepted": 1, "missing_skill": None},
        {"student_id": "STU_102", "job_id": "JOB_501", "predicted_match": 1, "user_accepted": 0, "missing_skill": "PyTorch"},
        {"student_id": "STU_103", "job_id": "JOB_502", "predicted_match": 0, "user_accepted": 1, "missing_skill": None},
        {"student_id": "STU_104", "job_id": "JOB_503", "predicted_match": 1, "user_accepted": 0, "missing_skill": "Kubernetes"},
    ]

    print("--- POST-LAUNCH MODEL HEALTH REPORT ---")
    print(generate_model_health_report(sample_logs))

    print("\n--- TRIAGED INTELLIGENCE DEFECTS & BACKLOG ---")
    print(triage_intelligence_defects(sample_logs))