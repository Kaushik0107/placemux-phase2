import hashlib
import json
import re

# Upstream Dependency: Skills Ontology Taxonomy
SKILLS_ONTOLOGY = {
    "python": ["python", "py", "fastapi", "pandas", "numpy", "scikit-learn"],
    "machine_learning": ["ml", "machine learning", "scikit-learn", "random forest", "classification"],
    "sql": ["sql", "postgres", "postgresql", "mysql"],
    "api_design": ["api", "fastapi", "rest", "restful", "json"]
}

def parse_resume_or_jd(text: str) -> dict:
    """
    Parsing v0: Extracts structured skills and experience years from raw text.
    """
    clean_text = text.lower()
    extracted_skills = set()

    # Skill extraction against Skills Ontology
    for canonical_skill, aliases in SKILLS_ONTOLOGY.items():
        for alias in aliases:
            if re.search(r'\b' + re.escape(alias) + r'\b', clean_text):
                extracted_skills.add(canonical_skill)
                break

    # Extract years of experience (Regex baseline)
    exp_match = re.search(r'(\d+)\+?\s*years?\b', clean_text)
    years_exp = int(exp_match.group(1)) if exp_match else 0

    return {
        "extracted_skills": list(extracted_skills),
        "years_experience": years_exp,
        "skill_count": len(extracted_skills)
    }

def generate_tamper_evident_offer(student_id: str, job_id: str, offer_details: dict) -> dict:
    """
    Generates a cryptographically hashed offer document that is tamper-evident.
    """
    payload = {
        "student_id": student_id,
        "job_id": job_id,
        "offer_details": offer_details
    }
    
    # Canonical JSON string representation for stable hashing
    canonical_json = json.dumps(payload, sort_keys=True)
    offer_hash = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    return {
        "offer_payload": payload,
        "document_hash": offer_hash,
        "status": "ISSUED"
    }

def verify_offer_tamper_evidence(signed_payload: dict, expected_hash: str) -> bool:
    """
    Verifies whether an offer document was tampered with post-signing.
    """
    canonical_json = json.dumps(signed_payload, sort_keys=True)
    current_hash = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    return current_hash == expected_hash

if __name__ == "__main__":
    # Test Parsing v0
    sample_text = "Experienced AI Engineer with 3+ years in Python, FastAPI, and Machine Learning."
    parsed = parse_resume_or_jd(sample_text)
    print("--- PARSING V0 OUTPUT ---")
    print(parsed)

    # Test Tamper-Evidence
    offer = generate_tamper_evident_offer("STU_1029", "JOB_501", {"salary": 120000, "role": "AI Engineer"})
    print("\n--- TAMPER-EVIDENT OFFER ---")
    print(f"Document Hash: {offer['document_hash']}")

    is_valid = verify_offer_tamper_evidence(offer['offer_payload'], offer['document_hash'])
    print(f"Authenticity Verified: {is_valid}")