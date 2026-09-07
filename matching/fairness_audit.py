import pandas as pd
import numpy as np

def run_fairness_bias_audit(candidate_decisions: list[dict], protected_attribute: str = "group") -> dict:
    """
    Computes Demographic Parity and Disparate Impact Ratio across protected demographic groups.
    """
    df = pd.DataFrame(candidate_decisions)
    
    if protected_attribute not in df.columns or 'is_shortlisted' not in df.columns:
        return {"status": "ERROR", "message": "Missing required fields for demographic audit."}

    # Group selection rates
    group_stats = df.groupby(protected_attribute)['is_shortlisted'].agg(['count', 'mean']).rename(columns={'mean': 'selection_rate'})
    
    selection_rates = group_stats['selection_rate'].to_dict()
    max_rate = max(selection_rates.values()) if selection_rates else 1.0
    min_rate = min(selection_rates.values()) if selection_rates else 0.0

    # Disparate Impact Ratio (80% Rule Check)
    disparate_impact_ratio = (min_rate / max_rate) if max_rate > 0 else 1.0
    passes_80_rule = disparate_impact_ratio >= 0.80

    return {
        "protected_attribute": protected_attribute,
        "group_selection_rates": {k: round(v, 4) for k, v in selection_rates.items()},
        "disparate_impact_ratio": round(disparate_impact_ratio, 4),
        "passes_four_fifths_rule": passes_80_rule,
        "audit_status": "FAIR" if passes_80_rule else "BIAS_DETECTED",
        "explanation": f"Disparate impact ratio is {disparate_impact_ratio:.2%}. " + 
                       ("Selection rates satisfy the 80% fairness rule." if passes_80_rule else "Selection disparity detected across demographic groups.")
    }

def process_dpdp_data_erasure(student_id: str) -> dict:
    """
    Simulates verifiable DPDP 'Right to be Forgotten' data deletion.
    """
    return {
        "student_id": student_id,
        "erasure_status": "COMPLETED",
        "records_purged": ["profile", "skill_scores", "proctor_logs", "application_audit"],
        "explanation": f"All personal data and assessment logs for student {student_id} have been permanently deleted in accordance with DPDP regulations."
    }

if __name__ == "__main__":
    # Test Data for Fairness Audit
    mock_data = [
        {"student_id": "S1", "group": "Tier_1", "is_shortlisted": 1},
        {"student_id": "S2", "group": "Tier_1", "is_shortlisted": 1},
        {"student_id": "S3", "group": "Tier_2", "is_shortlisted": 1},
        {"student_id": "S4", "group": "Tier_2", "is_shortlisted": 0},
    ]
    print("--- FAIRNESS / BIAS AUDIT RESULT ---")
    print(run_fairness_bias_audit(mock_data, protected_attribute="group"))

    print("\n--- DPDP DATA ERASURE TEST ---")
    print(process_dpdp_data_erasure("STU_1029"))