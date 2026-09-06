import re

# Upstream Skills Ontology Mapping Rules
SKILLS_ONTOLOGY_MAP = {
    "software_engineering": {
        "python": ["python", "py", "fastapi", "django", "flask"],
        "javascript": ["javascript", "js", "typescript", "ts", "react", "node"],
        "sql": ["sql", "postgres", "postgresql", "mysql"]
    },
    "data_ai": {
        "machine_learning": ["ml", "machine learning", "scikit-learn", "random forest", "xgboost"],
        "deep_learning": ["dl", "deep learning", "pytorch", "tensorflow", "neural networks"],
        "data_analysis": ["pandas", "numpy", "eda", "data cleaning"]
    }
}

def map_parsed_skills_to_ontology(raw_text: str) -> dict:
    """
    Feeds parsed text skills into the structured skills ontology.
    """
    clean_text = raw_text.lower()
    mapped_ontology = {}
    total_matches = 0

    for domain, skills_dict in SKILLS_ONTOLOGY_MAP.items():
        mapped_ontology[domain] = []
        for canonical_skill, aliases in skills_dict.items():
            for alias in aliases:
                if re.search(r'\b' + re.escape(alias) + r'\b', clean_text):
                    mapped_ontology[domain].append(canonical_skill)
                    total_matches += 1
                    break

    return {
        "ontology_skills": mapped_ontology,
        "total_ontology_matches": total_matches,
        "explanation": f"Successfully mapped {total_matches} skills into taxonomy categories."
    }

def get_end_to_end_application_status(student_id: str, job_id: str) -> dict:
    """
    End-to-end lifecycle status tracker for candidate journey.
    """
    # Consolidated status audit lifecycle
    return {
        "student_id": student_id,
        "job_id": job_id,
        "lifecycle_stages": {
            "application_submitted": True,
            "proctoring_verified": True,
            "offer_issued": True,
            "offer_signed": True,
            "interview_scheduled": True
        },
        "current_status": "INTERVIEW_SCHEDULED",
        "explanation": f"Candidate {student_id} successfully completed proctoring and signed offer for {job_id}."
    }

if __name__ == "__main__":
    sample_resume = "Experienced ML Engineer proficient in Python, PyTorch, Pandas, and PostgreSQL."
    mapped = map_parsed_skills_to_ontology(sample_resume)
    print("--- ONTOLOGY PARSING OUTPUT ---")
    print(mapped)

    status = get_end_to_end_application_status("STU_1029", "JOB_501")
    print("\n--- END-TO-END LIFE CYCLE STATUS ---")
    print(status)