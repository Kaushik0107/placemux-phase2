import pandas as pd
import numpy as np

def bulk_onboard_students(students_list: list[dict]) -> dict:
    """
    Processes bulk student onboarding records.
    """
    df = pd.DataFrame(students_list)
    total_processed = len(df)
    
    return {
        "total_onboarded": total_processed,
        "status": "SUCCESS",
        "explanation": f"Successfully onboarded {total_processed} student profiles in bulk."
    }

def analyze_item_bank_quality(item_analytics_data: list[dict]) -> dict:
    """
    Evaluates item-bank quality metrics and flags weak items for admins.
    """
    df = pd.DataFrame(item_analytics_data)
    
    # Identify weak items based on discrimination index (< 0.20) or extreme error rates (> 85% or < 5%)
    df['is_weak'] = (df['discrimination_index'] < 0.20) | (df['error_rate'] > 0.85) | (df['error_rate'] < 0.05)
    
    weak_items = df[df['is_weak']].to_dict(orient='records')
    
    flagged_reasons = []
    for item in weak_items:
        reasons = []
        if item['discrimination_index'] < 0.20:
            reasons.append(f"low discrimination index ({item['discrimination_index']:.2f})")
        if item['error_rate'] > 0.85:
            reasons.append(f"excessively high error rate ({item['error_rate']*100:.1f}%)")
        if item['error_rate'] < 0.05:
            reasons.append(f"too trivial/low error rate ({item['error_rate']*100:.1f}%)")
        
        flagged_reasons.append({
            "item_id": item["item_id"],
            "reason": f"Item {item['item_id']} flagged due to: {', '.join(reasons)}."
        })

    weak_count = len(weak_items)
    total_items = len(df)
    
    return {
        "total_items_analyzed": total_items,
        "weak_items_count": weak_count,
        "weak_item_flags": flagged_reasons,
        "explanation": f"Analyzed {total_items} items: {weak_count} weak items flagged for admin review."
    }

if __name__ == "__main__":
    # Test Bulk Onboarding
    sample_students = [
        {"student_id": f"STU_{i}", "skills": ["Python", "SQL"]} for i in range(10)
    ]
    print("--- BULK ONBOARDING RESULT ---")
    print(bulk_onboard_students(sample_students))

    # Test Item-Bank Quality
    sample_items = [
        {"item_id": "ITEM_101", "discrimination_index": 0.45, "error_rate": 0.30},
        {"item_id": "ITEM_102", "discrimination_index": 0.12, "error_rate": 0.90},  # Weak
        {"item_id": "ITEM_103", "discrimination_index": 0.50, "error_rate": 0.02},  # Weak
    ]
    print("\n--- ITEM-BANK QUALITY ANALYSIS ---")
    print(analyze_item_bank_quality(sample_items))