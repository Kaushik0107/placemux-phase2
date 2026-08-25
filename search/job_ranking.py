import json
from pathlib import Path

from matching.feature_matching import generate_matching_decision


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

STUDENTS_FILE = DATA_DIR / "evaluation_students.json"
JOBS_FILE = DATA_DIR / "evaluation_jobs.json"


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_students():
    return load_json(STUDENTS_FILE)


def load_jobs():
    return load_json(JOBS_FILE)


def get_student(student_id):
    for student in load_students():
        if student["student_id"] == student_id:
            return student

    return None


def rank_jobs_for_student(student_id, top_k=10):
    student = get_student(student_id)

    if student is None:
        raise ValueError("Student profile not found")

    ranked_jobs = []

    for job in load_jobs():
        decision = generate_matching_decision(student, job)

        ranked_jobs.append(
            {
                "job_title": job["job_title"],
                "company": job.get("company", ""),
                **decision,
            }
        )

    ranked_jobs.sort(
    key=lambda item: (
        item["threshold_validation"] == "PASS",
        item["match_score"],
    ),
    reverse=True,
)
    return ranked_jobs[:top_k]
