def build_explanation_payload(result):
    """
    Turn one matching result into a structured, API-ready explanation.
    """

    matched_skills = sorted(result.get("matched_skills", []))
    missing_skills = sorted(result.get("missing_skills", []))
    skill_results = result.get("skill_results", [])
    threshold_validation = result.get("threshold_validation", "FAIL")
    match_score = result.get("match_score", 0)

    decision = (
        "SHORTLISTED"
        if threshold_validation == "PASS"
        else "NOT_SHORTLISTED"
    )

    failed_skill_reasons = [
        item["reason"]
        for item in skill_results
        if item.get("result") == "FAIL"
    ]

    if decision == "SHORTLISTED":
        summary = (
            "Shortlisted because all required skill thresholds are met. "
            f"Matched required skills: {', '.join(matched_skills)}. "
            f"Overall match score: {match_score:.2f}%."
        )
    else:
        reasons = failed_skill_reasons

        if not reasons and missing_skills:
            reasons = [
                "Missing required skills: "
                + ", ".join(missing_skills)
                + "."
            ]

        summary = (
            "Not shortlisted because required skill thresholds are not met. "
            + " ".join(reasons)
            + f" Overall match score: {match_score:.2f}%."
        )

    return {
        "student_id": result.get("student_id"),
        "job_id": result.get("job_id"),
        "decision": decision,
        "match_score": match_score,
        "threshold_validation": threshold_validation,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_results": skill_results,
        "score_breakdown": result.get("match_breakdown", {}),
        "summary": summary,
    }


def explain_match(result):
    """
    Backward-compatible helper that returns only the plain-English summary.
    """

    return build_explanation_payload(result)["summary"]