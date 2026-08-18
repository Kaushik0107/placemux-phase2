def skill_match(student, job):
    required = set(job["required_skills"])
    student_skills = set(student["skills"])

    if not required:
        return 100

    matched = required.intersection(student_skills)

    return (len(matched) / len(required)) * 100


def proficiency_match(student, job):
    requirements = job.get("required_skill_scores", {})
    scores = student.get("verified_skill_scores", {})

    if not requirements:
        return 100

    results = []

    for skill, required_score in requirements.items():
        student_score = scores.get(skill, 0)

        score = min((student_score / required_score) * 100, 100)
        results.append(score)

    return sum(results) / len(results)


def experience_match(student, job):
    required = job.get("experience_required", 0)
    actual = student.get("experience_years", 0)

    if required == 0:
        return 100

    return min((actual / required) * 100, 100)


def role_match(student, job):
    preferred_roles = [
        role.lower()
        for role in student.get("preferred_roles", [])
    ]

    job_title = job["job_title"].lower()

    for role in preferred_roles:
        if role in job_title or job_title in role:
            return 100

    return 50


def location_work_mode_match(student, job):
    location_match = (
        student.get("location", "").lower()
        == job.get("location", "").lower()
    )

    student_modes = set(student.get("work_mode", []))
    job_modes = set(job.get("work_mode", []))

    work_mode_match = bool(student_modes.intersection(job_modes))

    if location_match and work_mode_match:
        return 100

    if location_match or work_mode_match:
        return 70

    return 0


def education_match(student, job):
    student_education = student.get("education", {})
    job_education = job.get("education_required", {})

    if (
        student_education.get("degree") == job_education.get("degree")
        and student_education.get("branch") == job_education.get("branch")
    ):
        return 100

    return 50


def availability_match(student, job):
    if (
        student.get("availability", "").lower()
        == job.get("joining_requirement", "").lower()
    ):
        return 100

    return 50


def salary_match(student, job):
    expected = student.get("salary_expectation", 0)
    salary_range = job.get("salary_range", {})

    minimum = salary_range.get("min", 0)
    maximum = salary_range.get("max", 0)

    if minimum <= expected <= maximum:
        return 100

    return 50


def calculate_match(student, job):
    scores = {
        "skill_match": skill_match(student, job),
        "proficiency_match": proficiency_match(student, job),
        "experience_match": experience_match(student, job),
        "role_match": role_match(student, job),
        "location_match": location_work_mode_match(student, job),
        "education_match": education_match(student, job),
        "availability_match": availability_match(student, job),
        "salary_match": salary_match(student, job)
    }

    weights = {
        "skill_match": 0.35,
        "proficiency_match": 0.20,
        "experience_match": 0.10,
        "role_match": 0.10,
        "location_match": 0.10,
        "education_match": 0.05,
        "availability_match": 0.05,
        "salary_match": 0.05
    }

    total = sum(
        scores[key] * weights[key]
        for key in scores
    )

    return round(total, 2), scores