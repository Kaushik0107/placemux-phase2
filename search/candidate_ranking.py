import json
from pathlib import Path

from matching.scoring import calculate_match


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

STUDENTS_FILE = DATA_DIR / "evaluation_students.json"
JOBS_FILE = DATA_DIR / "evaluation_jobs.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_students():
    return load_json(STUDENTS_FILE)


def load_jobs():
    return load_json(JOBS_FILE)


def get_job(job_id):
    jobs = load_jobs()

    for job in jobs:
        if job["job_id"] == job_id:
            return job

    return None


def rank_candidates_for_job(job_id, top_k=10):
    job = get_job(job_id)

    if job is None:
        raise ValueError("Job not found")

    students = load_students()

    ranked_candidates = []

    for student in students:
        match_score, breakdown = calculate_match(student, job)

        matched_skills = sorted(
            set(student.get("skills", []))
            .intersection(set(job.get("required_skills", [])))
        )

        missing_skills = sorted(
            set(job.get("required_skills", []))
            - set(student.get("skills", []))
        )

        ranked_candidates.append(
            {
                "student_id": student["student_id"],
                "match_score": match_score,
                "match_breakdown": breakdown,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            }
        )

    ranked_candidates.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return ranked_candidates[:top_k]