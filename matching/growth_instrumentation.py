import time
import uuid

# In-memory event stores for impressions and outcomes
IMPRESSION_STORE = {}
OUTCOME_STORE = []

def log_ranked_impression(candidate_ids: list[str], model_version: str = "PlaceMux_Ranking_v2.1", user_id: str = "USER_101") -> dict:
    """
    Logs ranked candidate list impressions with position indices and model metadata.
    """
    impression_id = f"IMP_{uuid.uuid4().hex[:8]}"
    timestamp = time.time()

    ranked_items = [
        {"position": idx + 1, "candidate_id": cand_id}
        for idx, cand_id in enumerate(candidate_ids)
    ]

    record = {
        "impression_id": impression_id,
        "user_id": user_id,
        "model_version": model_version,
        "timestamp": timestamp,
        "ranked_candidates": ranked_items
    }

    IMPRESSION_STORE[impression_id] = record

    return {
        "impression_id": impression_id,
        "status": "LOGGED",
        "total_items_logged": len(candidate_ids),
        "explanation": f"Logged impression '{impression_id}' with {len(candidate_ids)} candidates mapped to positions (1-{len(candidate_ids)})."
    }

def log_user_outcome(impression_id: str, candidate_id: str, event_type: str) -> dict:
    """
    Logs downstream conversion outcomes (click, apply, shortlist) joinable to impression_id.
    """
    valid_events = ["click", "apply", "shortlist", "dismiss"]
    if event_type not in valid_events:
        return {"status": "ERROR", "message": f"Invalid event_type. Must be one of {valid_events}."}

    if impression_id not in IMPRESSION_STORE:
        return {"status": "ERROR", "message": f"Impression '{impression_id}' not found."}

    # Find position from original impression
    impression = IMPRESSION_STORE[impression_id]
    position = next((item["position"] for item in impression["ranked_candidates"] if item["candidate_id"] == candidate_id), None)

    outcome_record = {
        "event_id": f"EVT_{uuid.uuid4().hex[:8]}",
        "impression_id": impression_id,
        "candidate_id": candidate_id,
        "position": position,
        "event_type": event_type,
        "timestamp": time.time()
    }

    OUTCOME_STORE.append(outcome_record)

    return {
        "event_id": outcome_record["event_id"],
        "status": "RECORDED",
        "impression_id": impression_id,
        "position": position,
        "event_type": event_type,
        "explanation": f"Recorded '{event_type}' event for candidate '{candidate_id}' at position {position}."
    }

def reconstruct_session_trace(impression_id: str) -> dict:
    """
    Reconstructs exact list position, model version, and outcomes for a given impression ID.
    """
    if impression_id not in IMPRESSION_STORE:
        return {"found": False, "message": "Impression ID not found."}

    impression = IMPRESSION_STORE[impression_id]
    outcomes = [o for o in OUTCOME_STORE if o["impression_id"] == impression_id]

    return {
        "found": True,
        "impression": impression,
        "outcomes": outcomes,
        "explanation": f"Reconstructed impression showing {len(impression['ranked_candidates'])} items and {len(outcomes)} linked user outcomes."
    }

if __name__ == "__main__":
    cands = ["STU_101", "STU_102", "STU_103"]
    imp_res = log_ranked_impression(cands)
    print("--- 1. LOGGED IMPRESSION ---")
    print(imp_res)

    imp_id = imp_res["impression_id"]
    out_res = log_user_outcome(imp_id, "STU_102", "apply")
    print("\n--- 2. LOGGED OUTCOME ---")
    print(out_res)

    print("\n--- 3. RECONSTRUCTED SESSION TRACE ---")
    print(reconstruct_session_trace(imp_id))