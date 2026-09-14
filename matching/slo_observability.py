import numpy as np
import pandas as pd
import time

# Total monthly error budget allocation (e.g., 0.1% of 100,000 requests = 100 allowed failures)
MONTHLY_ERROR_BUDGET_CAP = 100.0

def evaluate_inference_slos(telemetry_logs: list[dict], p95_target_ms: float = 100.0, min_availability: float = 0.999) -> dict:
    """
    Evaluates inference SLOs (p95 latency, availability, score distribution variance) and triggers alerts.
    """
    if not telemetry_logs:
        return {"status": "NO_TELEMETRY", "explanation": "No telemetry logs recorded for SLO evaluation."}

    df = pd.DataFrame(telemetry_logs)
    total_requests = len(df)
    
    # 1. Latency & Availability Evaluation
    latencies = df['latency_ms'].values
    p95_latency = float(np.percentile(latencies, 95))
    failed_requests = len(df[df['is_error'] == True])
    availability = (total_requests - failed_requests) / total_requests if total_requests > 0 else 1.0

    # 2. Prediction Quality / Score Distribution Check
    scores = df['prediction_score'].values if 'prediction_score' in df.columns else np.array([0.5])
    score_variance = float(np.var(scores))
    mean_score = float(np.mean(scores))

    # 3. Breach & Alert Detection
    alerts = []
    if p95_latency > p95_target_ms:
        alerts.append(f"LATENCY_BREACH: p95 latency is {p95_latency:.2f}ms (SLO target <= {p95_target_ms:.2f}ms)")

    if availability < min_availability:
        alerts.append(f"AVAILABILITY_BREACH: Availability is {availability:.2%} (SLO target >= {min_availability:.2%})")

    # Degenerate/Constant output detection (Variance near zero)
    if score_variance < 0.001 and total_requests > 5:
        alerts.append("DEGENERATE_OUTPUT_ALERT: Model score variance is near zero. Silent garbage predictions detected!")

    # 4. Error Budget Burn Rate Calculation
    budget_consumed = failed_requests
    remaining_budget = max(0.0, MONTHLY_ERROR_BUDGET_CAP - budget_consumed)
    burn_rate_percent = (budget_consumed / MONTHLY_ERROR_BUDGET_CAP) * 100.0

    slo_passed = len(alerts) == 0

    return {
        "total_requests": total_requests,
        "metrics": {
            "p95_latency_ms": round(p95_latency, 2),
            "availability": round(availability, 4),
            "mean_score": round(mean_score, 4),
            "score_variance": round(score_variance, 6)
        },
        "error_budget": {
            "capacity": MONTHLY_ERROR_BUDGET_CAP,
            "consumed": budget_consumed,
            "remaining": remaining_budget,
            "burn_rate_pct": round(burn_rate_percent, 2)
        },
        "slo_status": "PASSED" if slo_passed else "BREACHED",
        "alerts_triggered": alerts,
        "explanation": "All SLOs satisfied." if slo_passed else f"SLO breaches detected: {'; '.join(alerts)}"
    }

if __name__ == "__main__":
    # Test Data: Healthy Traffic
    healthy_logs = [
        {"latency_ms": np.random.normal(30, 5), "is_error": False, "prediction_score": float(np.random.uniform(0.1, 0.9))}
        for _ in range(50)
    ]
    print("--- HEALTHY TELEMETRY SLO EVALUATION ---")
    print(evaluate_inference_slos(healthy_logs))

    # Test Data: Degenerate Score Distribution Breach
    degenerate_logs = [
        {"latency_ms": 40.0, "is_error": False, "prediction_score": 0.50} for _ in range(50)
    ]
    print("\n--- DEGENERATE SCORE DISTRIBUTION ALERT TEST ---")
    print(evaluate_inference_slos(degenerate_logs))