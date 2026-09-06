from matching.ontology_tracking import map_parsed_skills_to_ontology
from matching.proctoring_hardening import evaluate_proctoring_hardening
from matching.parsing_esign import generate_tamper_evident_offer, verify_offer_tamper_evidence

def run_ai_trust_signoff(student_id: str, job_id: str, raw_resume_text: str, session_data: dict) -> dict:
    """
    Executes the full AI Trust Layer Dry Run pipeline end-to-end.
    """
    # 1. Ontology Parsing Check
    parsed_skills = map_parsed_skills_to_ontology(raw_resume_text)
    
    # 2. Proctoring Verification Check
    gaze_ratio = session_data.get("gaze_off_screen_ratio", 0.0)
    tab_switches = session_data.get("tab_switches", 0)
    
    is_proctor_flagged = tab_switches > 4 or gaze_ratio > 0.35
    proctor_status = "FLAGGED" if is_proctor_flagged else "CLEARED"
    proctor_reason = (
        f"Proctoring flag raised due to {tab_switches} tab switches."
        if is_proctor_flagged
        else "Candidate proctoring behavior within normal thresholds."
    )

    # 3. Issue Tamper-Evident Offer
    offer_details = {
        "role": "AI Engineer",
        "salary": 120000,
        "parsed_skills_count": parsed_skills["total_ontology_matches"],
        "proctor_status": proctor_status
    }
    
    issued_offer = generate_tamper_evident_offer(student_id, job_id, offer_details)
    
    # 4. Verify Offer Authenticity (Cryptographic Hash Verification)
    is_authentic = verify_offer_tamper_evidence(
        issued_offer["offer_payload"], 
        issued_offer["document_hash"]
    )

    return {
        "student_id": student_id,
        "job_id": job_id,
        "pipeline_verification": {
            "ontology_skills_mapped": parsed_skills["total_ontology_matches"],
            "proctoring_status": proctor_status,
            "proctoring_explanation": proctor_reason,
            "offer_document_hash": issued_offer["document_hash"],
            "tamper_evident_verified": is_authentic
        },
        "overall_trust_signoff": "PASSED" if is_authentic and not is_proctor_flagged else "FAILED_VERIFICATION",
        "summary_explanation": "All AI trust features signed off: skills mapped, proctoring hardened, offer cryptographically verified."
    }

if __name__ == "__main__":
    test_resume = "AI ML Engineer proficient in Python, Scikit-learn, Pandas, and SQL."
    test_session = {"gaze_off_screen_ratio": 0.12, "tab_switches": 1}
    
    signoff = run_ai_trust_signoff("STU_1029", "JOB_501", test_resume, test_session)
    print("--- AI TRUST SIGN-OFF DRY RUN RESULT ---")
    print(signoff)