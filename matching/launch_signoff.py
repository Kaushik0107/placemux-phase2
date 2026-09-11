import time
from matching.fairness_audit import run_fairness_bias_audit

def execute_fairness_close_and_signoff(audit_dataset: list[dict], model_name: str = "PlaceMux_Matching_V1") -> dict:
    """
    Evaluates final fairness metrics and provides formal ML model sign-off for launch.
    """
    # 1. Execute Fairness Audit
    audit_results = run_fairness_bias_audit(audit_dataset, protected_attribute="group")
    
    passes_fairness = audit_results.get("passes_four_fifths_rule", False)
    disparate_impact = audit_results.get("disparate_impact_ratio", 0.0)

    # 2. Final Sign-off Logic
    is_signed_off = passes_fairness
    status = "SIGNED_OFF" if is_signed_off else "REJECTED_BIAS_THRESHOLD"

    return {
        "model_name": model_name,
        "timestamp": time.time(),
        "audit_summary": {
            "disparate_impact_ratio": disparate_impact,
            "passes_80_percent_rule": passes_fairness,
            "group_selection_rates": audit_results.get("group_selection_rates", {})
        },
        "signoff_status": status,
        "launch_ready": is_signed_off,
        "explanation": f"Model '{model_name}' successfully passed final fairness audit with {disparate_impact:.2%} disparate impact. ML model signed off for launch."
                       if is_signed_off else f"Model '{model_name}' failed fairness audit ({disparate_impact:.2%} impact ratio). Sign-off rejected."
    }

if __name__ == "__main__":
    # Test Data for Final Launch Rehearsal
    test_data = [
        {"student_id": "STU_1", "group": "Tier_1", "is_shortlisted": 1},
        {"student_id": "STU_2", "group": "Tier_1", "is_shortlisted": 1},
        {"student_id": "STU_3", "group": "Tier_2", "is_shortlisted": 1},
        {"student_id": "STU_4", "group": "Tier_2", "is_shortlisted": 1},
    ]
    print("--- LAUNCH REHEARSAL FAIRNESS CLOSE & SIGN-OFF ---")
    print(execute_fairness_close_and_signoff(test_data))