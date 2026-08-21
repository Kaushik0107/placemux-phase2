import json
from pathlib import Path

from matching.scoring import calculate_match
from matching.threshold_validation import validate_skill_thresholds
from search.explainability import build_explanation_payload


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_students(dataset="sample"):
    return load_json(DATA_DIR / f"{dataset}_students.json")


def load_jobs(dataset="sample"):
    return load_json(DATA_DIR / f"{dataset}_jobs.json")


def match_student_to_jobs(student_id, top_k=10, dataset="sample"):
    students = load_students(dataset)
    jobs = load_jobs(dataset)

    student = next(
        (item for item in students if item["student_id"] == student_id),
        None,
    )

    if student is None:
        raise ValueError("Student not found")

    matches = []

    for job in jobs:
        decision = generate_matching_decision(student, job)

        matches.append(
            {
                "job_title": job["job_title"],
                "company": job["company"],
                **decision,
            }
        )

    matches.sort(
        key=lambda item: item["match_score"],
        reverse=True,
    )

    return matches[:top_k]


def generate_match_vector(student, job):
    """
    Generate the eight numerical signals used to score one student-job pair.
    """

    total_score, breakdown = calculate_match(student, job)

    match_vector = [
        breakdown["skill_match"],
        breakdown["proficiency_match"],
        breakdown["experience_match"],
        breakdown["role_match"],
        breakdown["location_match"],
        breakdown["education_match"],
        breakdown["availability_match"],
        breakdown["salary_match"],
    ]

    return {
        "student_id": student["student_id"],
        "job_id": job["job_id"],
        "match_vector": match_vector,
        "match_score": total_score,
        "match_breakdown": breakdown,
    }


def generate_matching_decision(student, job):
    """
    Generate one complete, explainable student-job matching decision.
    """

    match_vector_result = generate_match_vector(student, job)
    threshold_result = validate_skill_thresholds(student, job)

    matched_skills = sorted(
        set(student.get("skills", []))
        .intersection(set(job.get("required_skills", [])))
    )

    missing_skills = sorted(
        set(job.get("required_skills", []))
        - set(student.get("skills", []))
    )

    decision = {
        "student_id": student["student_id"],
        "job_id": job["job_id"],
        "match_vector": match_vector_result["match_vector"],
        "match_score": match_vector_result["match_score"],
        "match_breakdown": match_vector_result["match_breakdown"],
        "threshold_validation": threshold_result["threshold_validation"],
        "skill_results": threshold_result["skill_results"],
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }

    decision["explanation"] = build_explanation_payload(decision)

    return decision