import hashlib
import time

def assign_user_to_variant(user_id: str, experiment_name: str = "Ranking_V2_Experiment", holdout_pct: float = 0.05) -> dict:
    """
    Deterministically routes users to CONTROL, TREATMENT, or PERMANENT_HOLDOUT based on consistent hashing.
    """
    # 1. Generate deterministic hash integer (0 - 99)
    hash_input = f"{user_id}:{experiment_name}".encode('utf-8')
    hash_val = int(hashlib.md5(hash_input).hexdigest(), 16) % 100

    # 2. Permanent Holdout Group (0 to holdout_pct * 100)
    holdout_threshold = int(holdout_pct * 100)
    if hash_val < holdout_threshold:
        return {
            "user_id": user_id,
            "experiment_name": experiment_name,
            "variant": "PERMANENT_HOLDOUT",
            "model_version": "RuleBasedHeuristic_Baseline",
            "explanation": f"User '{user_id}' assigned to Permanent Holdout group (hash bucket {hash_val})."
        }

    # 3. 50/50 Split between Control and Treatment for remaining traffic
    remaining_bucket = hash_val - holdout_threshold
    if remaining_bucket % 2 == 0:
        variant = "CONTROL"
        model_version = "PlaceMux_Ranking_v1.0"
    else:
        variant = "TREATMENT"
        model_version = "PlaceMux_Ranking_v2.0_ML"

    return {
        "user_id": user_id,
        "experiment_name": experiment_name,
        "variant": variant,
        "model_version": model_version,
        "hash_bucket": hash_val,
        "explanation": f"User '{user_id}' consistently routed to '{variant}' using model '{model_version}'."
    }

def evaluate_experiment_guardrails(treatment_metrics: dict, guardrail_relevance_floor: float = 0.65, max_error_rate: float = 0.02) -> dict:
    """
    Evaluates guardrail metrics (relevance score floor, error rate) for treatment variants and triggers auto-halt.
    """
    avg_relevance = treatment_metrics.get("mean_relevance_score", 0.70)
    error_rate = treatment_metrics.get("error_rate", 0.0)

    alerts = []
    if avg_relevance < guardrail_relevance_floor:
        alerts.append(f"RELEVANCE_GUARDRAIL_BREACH: Relevance dropped to {avg_relevance:.2f} (Floor: {guardrail_relevance_floor:.2f})")

    if error_rate > max_error_rate:
        alerts.append(f"ERROR_RATE_GUARDRAIL_BREACH: Error rate spiked to {error_rate:.2%} (Limit: {max_error_rate:.2%})")

    auto_halt = len(alerts) > 0

    return {
        "variant_evaluated": treatment_metrics.get("variant", "TREATMENT"),
        "guardrail_status": "HALTED" if auto_halt else "HEALTHY",
        "auto_halt_triggered": auto_halt,
        "alerts": alerts,
        "explanation": f"Treatment variant halted due to guardrail breach: {'; '.join(alerts)}" if auto_halt else "Variant operating safely within guardrail metrics."
    }

if __name__ == "__main__":
    print("--- 1. DETERMINISTIC VARIANT ROUTING TEST ---")
    for uid in ["USER_101", "USER_102", "USER_103", "USER_104"]:
        print(assign_user_to_variant(uid))

    print("\n--- 2. GUARDRAIL METRICS AUTO-HALT TEST ---")
    degraded_metrics = {"variant": "TREATMENT", "mean_relevance_score": 0.52, "error_rate": 0.005}
    print(evaluate_experiment_guardrails(degraded_metrics))