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


def generate_match_vector(student, job):
    """
    Generate a numerical match vector for a student-job pair.

    Vector dimensions:
    1. Skill Match
    2. Proficiency Match
    3. Experience Match
    4. Role Match
    5. Location/Work Mode Match
    6. Education Match
    7. Availability Match
    8. Salary Match
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
        breakdown["salary_match"]
    ]

    return {
        "student_id": student["student_id"],
        "job_id": job["job_id"],
        "match_vector": match_vector,
        "match_score": total_score
    }


def generate_matching_decision(student, job):
    """
    Generate the complete student-job matching decision.

    Combines:
    - match vector
    - weighted match score
    - threshold validation
    - matched skills
    - missing skills
    """

    from matching.threshold_validation import validate_skill_thresholds

    match_vector_result = generate_match_vector(student, job)

    threshold_result = validate_skill_thresholds(student, job)

    matched_skills = list(
        set(student.get("skills", [])).intersection(
            set(job.get("required_skills", []))
        )
    )

    missing_skills = list(
        set(job.get("required_skills", []))
        - set(student.get("skills", []))
    )

    return {
        "student_id": student["student_id"],
        "job_id": job["job_id"],
        "match_vector": match_vector_result["match_vector"],
        "match_score": match_vector_result["match_score"],
        "threshold_validation": threshold_result["threshold_validation"],
        "skill_results": threshold_result["skill_results"],
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }