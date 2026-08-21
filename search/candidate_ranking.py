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


def get_job(job_id):
    for job in load_jobs():
        if job["job_id"] == job_id:
            return job

    return None


def rank_candidates_for_job(job_id, top_k=10):
    job = get_job(job_id)

    if job is None:
        raise ValueError("Job not found")

    ranked_candidates = []

    for student in load_students():
        decision = generate_matching_decision(student, job)

        ranked_candidates.append(
            {
                "job_title": job["job_title"],
                "company": job.get("company", ""),
                **decision,
            }
        )

    ranked_candidates.sort(
        key=lambda item: item["match_score"],
        reverse=True,
    )

    return ranked_candidates[:top_k]