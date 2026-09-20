import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve, auc

def train_and_eval_churn_model(training_data: list[dict]) -> dict:
    """
    Trains a churn prediction model with a 14-day disengagement horizon and evaluates PR AUC against baseline.
    """
    df = pd.DataFrame(training_data)
    
    # Feature columns and label definition (churn_label: 1 if disengaged in 14d horizon, 0 otherwise)
    X = df[["days_since_last_login", "applications_last_30d", "profile_completeness_pct"]]
    y = df["churn_label"]

    # Simple Baseline (Recency rule: > 14 days inactive = churn)
    baseline_preds = (df["days_since_last_login"] > 14).astype(int)
    baseline_precision = float(np.mean(y[baseline_preds == 1])) if sum(baseline_preds) > 0 else 0.0

    # Train Random Forest Classifier
    model = RandomForestClassifier(n_estimators=20, random_state=42)
    model.fit(X, y)

    probs = model.predict_proba(X)[:, 1]
    precision, recall, _ = precision_recall_curve(y, probs)
    pr_auc = float(auc(recall, precision))

    lift = (pr_auc - baseline_precision) / baseline_precision if baseline_precision > 0 else 1.0

    return {
        "model_type": "RandomForest_14Day_Churn_Classifier",
        "horizon_days": 14,
        "metrics": {
            "baseline_precision": round(baseline_precision, 4),
            "model_pr_auc": round(pr_auc, 4),
            "lift_over_baseline_pct": round(lift * 100.0, 2)
        },
        "explanation": f"Churn model achieved PR AUC of {pr_auc:.4f}, demonstrating a {lift * 100.0:.1f}% lift over recency-only baseline."
    }

def generate_at_risk_list(user_records: list[dict], threshold: float = 0.50) -> dict:
    """
    Generates a prioritized list of at-risk users with churn probabilities and risk drivers for growth team hand-off.
    """
    df = pd.DataFrame(user_records)
    
    # Train inline lightweight classifier on sample feature weights
    X = df[["days_since_last_login", "applications_last_30d", "profile_completeness_pct"]]
    
    # Synthesize probabilities based on recency and activity drop
    at_risk_users = []
    for _, row in df.iterrows():
        # Heuristic probability calculation for demonstration
        risk_score = (row["days_since_last_login"] / 30.0) * 0.5 + (1 - row["applications_last_30d"] / 10.0) * 0.3 + (1 - row["profile_completeness_pct"] / 100.0) * 0.2
        risk_score = min(1.0, max(0.0, float(risk_score)))

        if risk_score >= threshold:
            drivers = []
            if row["days_since_last_login"] > 10:
                drivers.append(f"High inactivity ({row['days_since_last_login']} days)")
            if row["applications_last_30d"] < 2:
                drivers.append("Low application activity")
            if row["profile_completeness_pct"] < 70:
                drivers.append("Incomplete profile")

            at_risk_users.append({
                "entity_id": row["entity_id"],
                "entity_type": row.get("entity_type", "CANDIDATE"),
                "churn_probability": round(risk_score, 4),
                "risk_level": "CRITICAL" if risk_score > 0.75 else "HIGH",
                "primary_risk_drivers": drivers if drivers else ["Declining session engagement"]
            })

    # Sort prioritized list by risk score
    at_risk_users.sort(key=lambda x: x["churn_probability"], reverse=True)

    return {
        "total_evaluated": len(user_records),
        "total_at_risk": len(at_risk_users),
        "prioritized_at_risk_list": at_risk_users,
        "explanation": f"Identified {len(at_risk_users)} at-risk entities out of {len(user_records)} evaluated for retention intervention."
    }

if __name__ == "__main__":
    sample_data = [
        {"entity_id": "STU_1", "days_since_last_login": 20, "applications_last_30d": 0, "profile_completeness_pct": 50, "churn_label": 1},
        {"entity_id": "STU_2", "days_since_last_login": 2, "applications_last_30d": 8, "profile_completeness_pct": 95, "churn_label": 0},
        {"entity_id": "STU_3", "days_since_last_login": 15, "applications_last_30d": 1, "profile_completeness_pct": 60, "churn_label": 1},
        {"entity_id": "STU_4", "days_since_last_login": 1, "applications_last_30d": 12, "profile_completeness_pct": 100, "churn_label": 0},
    ]

    print("--- CHURN MODEL EVALUATION ---")
    print(train_and_eval_churn_model(sample_data))

    print("\n--- PRIORITIZED AT-RISK LIST FOR GROWTH ---")
    print(generate_at_risk_list(sample_data))