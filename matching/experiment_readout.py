import math
import numpy as np

# In-memory store for pre-registered experiment hypotheses
EXPERIMENT_REGISTRY = {}

def pre_register_hypothesis(
    experiment_id: str,
    hypothesis: str,
    primary_metric: str = "application_ctr",
    target_lift_pct: float = 5.0,
    alpha: float = 0.05
) -> dict:
    """
    Pre-registers an A/B experiment hypothesis and primary evaluation metrics before reading results.
    """
    record = {
        "experiment_id": experiment_id,
        "hypothesis": hypothesis,
        "primary_metric": primary_metric,
        "target_lift_pct": target_lift_pct,
        "alpha": alpha,
        "status": "PRE_REGISTERED"
    }
    EXPERIMENT_REGISTRY[experiment_id] = record
    return {
        "status": "SUCCESS",
        "data": record,
        "explanation": f"Hypothesis pre-registered for experiment '{experiment_id}'. Target metric: {primary_metric} (+{target_lift_pct}%)."
    }

def evaluate_ab_test_readout(
    experiment_id: str,
    control_conversions: int,
    control_impressions: int,
    treatment_conversions: int,
    treatment_impressions: int,
    guardrail_breached: bool = False
) -> dict:
    """
    Performs honest two-sample proportion z-test and generates a SHIP / DO-NOT-SHIP decision.
    """
    # 1. Check Pre-registration
    prereg = EXPERIMENT_REGISTRY.get(experiment_id, {
        "primary_metric": "application_ctr",
        "target_lift_pct": 5.0,
        "alpha": 0.05
    })

    # 2. Conversion Rates
    p_control = control_conversions / control_impressions if control_impressions > 0 else 0.0
    p_treatment = treatment_conversions / treatment_impressions if treatment_impressions > 0 else 0.0

    relative_lift_pct = ((p_treatment - p_control) / p_control) * 100.0 if p_control > 0 else 0.0

    # 3. Two-sample Z-test for statistical significance
    p_pooled = (control_conversions + treatment_conversions) / (control_impressions + treatment_impressions)
    se_pooled = math.sqrt(p_pooled * (1 - p_pooled) * ((1 / control_impressions) + (1 / treatment_impressions)))
    
    z_score = (p_treatment - p_control) / se_pooled if se_pooled > 0 else 0.0
    p_value = float(2 * (1 - 0.5 * (1 + math.erf(abs(z_score) / math.sqrt(2)))))  # Two-tailed p-value

    stat_significant = p_value < prereg["alpha"]

    # 4. Ship / Do-Not-Ship Decision Logic
    is_winning = relative_lift_pct > 0 and stat_significant
    
    if guardrail_breached:
        decision = "DO_NOT_SHIP_GUARDRAIL_BREACH"
        reason = "Treatment achieved lift, but failed critical safety guardrails. Model rollout halted."
    elif is_winning:
        decision = "SHIP_TO_PRODUCTION"
        reason = f"Treatment achieved statistically significant {relative_lift_pct:.2f}% lift in {prereg['primary_metric']} (p = {p_value:.4f} < {prereg['alpha']})."
    else:
        decision = "DO_NOT_SHIP_INSUFFICIENT_LIFT"
        reason = f"Treatment failed to show statistically significant lift over control (Lift: {relative_lift_pct:.2f}%, p = {p_value:.4f})."

    return {
        "experiment_id": experiment_id,
        "metrics": {
            "control_ctr": round(p_control, 4),
            "treatment_ctr": round(p_treatment, 4),
            "relative_lift_pct": round(relative_lift_pct, 2),
            "z_score": round(z_score, 4),
            "p_value": round(p_value, 4),
            "statistically_significant": stat_significant
        },
        "decision": decision,
        "ship_recommended": decision == "SHIP_TO_PRODUCTION",
        "explanation": reason
    }

if __name__ == "__main__":
    exp_id = "EXP_RANKING_V2_001"
    pre_register_hypothesis(
        exp_id,
        hypothesis="Neural ranking model increases first-session job application CTR by > 5%",
        primary_metric="application_ctr"
    )

    print("--- 1. STATISTICALLY SIGNIFICANT WINNING READOUT ---")
    win_res = evaluate_ab_test_readout(exp_id, control_conversions=120, control_impressions=1000, treatment_conversions=180, treatment_impressions=1000)
    print(win_res)

    print("\n--- 2. GUARDRAIL BREACHED ROLLBACK READOUT ---")
    fail_res = evaluate_ab_test_readout(exp_id, control_conversions=120, control_impressions=1000, treatment_conversions=180, treatment_impressions=1000, guardrail_breached=True)
    print(fail_res)