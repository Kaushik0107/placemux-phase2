import pandas as pd
import numpy as np

def validate_recommendation_quality(recommendations_data: list[dict]) -> dict:
    """
    Validates recommendation quality metrics (Precision@K, Recall@K) on integrated data.
    """
    df = pd.DataFrame(recommendations_data)
    
    total_queries = len(df)
    precision_scores = []
    recall_scores = []

    for _, row in df.iterrows():
        recommended_set = set(row['recommended_job_ids'])
        relevant_set = set(row['relevant_job_ids'])
        
        if not recommended_set:
            continue
            
        hits = len(recommended_set.intersection(relevant_set))
        precision = hits / len(recommended_set)
        recall = hits / len(relevant_set) if relevant_set else 1.0
        
        precision_scores.append(precision)
        recall_scores.append(recall)

    avg_precision = float(np.mean(precision_scores)) if precision_scores else 0.0
    avg_recall = float(np.mean(recall_scores)) if recall_scores else 0.0

    return {
        "total_queries_evaluated": total_queries,
        "mean_precision": round(avg_precision, 4),
        "mean_recall": round(avg_recall, 4),
        "status": "VALIDATED" if avg_precision >= 0.80 else "NEEDS_TUNING",
        "explanation": f"Validated {total_queries} recommendation runs: Mean Precision@K = {avg_precision:.2%}, Mean Recall@K = {avg_recall:.2%}."
    }

def get_college_placement_portal_view(college_id: str, requesting_college_id: str, candidates_data: list[dict]) -> dict:
    """
    Validates multi-tenant isolation: Ensures College A cannot access College B's candidate data.
    """
    if college_id != requesting_college_id:
        return {
            "access_granted": False,
            "error_code": 403,
            "message": f"ACCESS_DENIED: Tenant '{requesting_college_id}' is unauthorized to view candidate data belonging to '{college_id}'."
        }
    
    college_candidates = [c for c in candidates_data if c.get('college_id') == college_id]
    
    return {
        "access_granted": True,
        "college_id": college_id,
        "total_candidates": len(college_candidates),
        "candidates": college_candidates,
        "explanation": f"Successfully loaded portal analytics for {college_id}. Data isolation verified."
    }

if __name__ == "__main__":
    # 1. Test Rec Validation
    mock_recs = [
        {"student_id": "S1", "recommended_job_ids": ["J1", "J2", "J3"], "relevant_job_ids": ["J1", "J2"]},
        {"student_id": "S2", "recommended_job_ids": ["J4", "J5"], "relevant_job_ids": ["J4", "J5"]}
    ]
    print("--- RECOMMENDATION QUALITY VALIDATION ---")
    print(validate_recommendation_quality(mock_recs))

    # 2. Test Tenant Data Isolation
    mock_candidates = [
        {"student_id": "STU_101", "college_id": "COLLEGE_A", "score": 88},
        {"student_id": "STU_102", "college_id": "COLLEGE_B", "score": 92}
    ]
    print("\n--- TENANT ISOLATION CHECK (AUTHORIZED) ---")
    print(get_college_placement_portal_view("COLLEGE_A", "COLLEGE_A", mock_candidates))

    print("\n--- TENANT ISOLATION CHECK (UNAUTHORIZED DATA LEAK PREVENTED) ---")
    print(get_college_placement_portal_view("COLLEGE_A", "COLLEGE_B", mock_candidates))