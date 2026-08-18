import json
from matching.scoring import calculate_match


def load_students():
    with open("data/sample_students.json", "r") as file:
        return json.load(file)


def load_jobs():
    with open("data/sample_jobs.json", "r") as file:
        return json.load(file)


def match_student_to_jobs(student_id, top_k=10):
    students = load_students()
    jobs = load_jobs()

    student = next(
        (s for s in students if s["student_id"] == student_id),
        None
    )

    if not student:
        raise ValueError("Student not found")

    matches = []

    for job in jobs:
        total_score, breakdown = calculate_match(student, job)

        matched_skills = list(
            set(student["skills"]).intersection(
                set(job["required_skills"])
            )
        )

        missing_skills = list(
            set(job["required_skills"])
            - set(student["skills"])
        )

        matches.append({
            "job_id": job["job_id"],
            "job_title": job["job_title"],
            "company": job["company"],
            "match_score": total_score,
            "match_breakdown": breakdown,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    matches.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return matches[:top_k]