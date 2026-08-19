def validate_skill_thresholds(student, job):
    """
    Validate whether a student's verified skill scores
    satisfy the required skill thresholds for a job.
    """

    verified_scores = student.get("verified_skill_scores", {})
    required_skills = job.get("required_skills", [])
    required_thresholds = job.get("required_skill_scores", {})

    results = []

    for skill in required_skills:
        student_score = verified_scores.get(skill, 0)
        required_score = required_thresholds.get(skill)

        if required_score is None:
            results.append({
                "skill": skill,
                "student_score": student_score,
                "required_threshold": None,
                "result": "FAIL",
                "reason": (
                    f"No required threshold is defined for {skill}."
                )
            })
            continue

        passed = student_score >= required_score

        if passed:
            reason = (
                f"{skill} score {student_score} meets "
                f"the required threshold of {required_score}."
            )
            result = "PASS"
        else:
            reason = (
                f"{skill} score {student_score} is below "
                f"the required threshold of {required_score}."
            )
            result = "FAIL"

        results.append({
            "skill": skill,
            "student_score": student_score,
            "required_threshold": required_score,
            "result": result,
            "reason": reason
        })

    overall_result = all(
        item["result"] == "PASS"
        for item in results
    )

    return {
        "student_id": student["student_id"],
        "job_id": job["job_id"],
        "threshold_validation": "PASS" if overall_result else "FAIL",
        "skill_results": results
    }