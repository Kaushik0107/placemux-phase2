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


def get_student(student_id):
    students = load_students()

    for student in students:
        if student["student_id"] == student_id:
            return student

    return None


def rank_jobs_for_student(student_id, top_k=10):
    student = get_student(student_id)

    if student is None:
        raise ValueError("Student profile not found")

    jobs = load_jobs()

    ranked_jobs = []

    for job in jobs:
        match_score, breakdown = calculate_match(student, job)

        matched_skills = sorted(
            set(student.get("skills", []))
            .intersection(set(job.get("required_skills", [])))
        )

        missing_skills = sorted(
            set(job.get("required_skills", []))
            - set(student.get("skills", []))
        )

        ranked_jobs.append(
            {
                "job_id": job["job_id"],
                "job_title": job["job_title"],
                "company": job.get("company", ""),
                "match_score": match_score,
                "match_breakdown": breakdown,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            }
        )

    ranked_jobs.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return ranked_jobs[:top_k]