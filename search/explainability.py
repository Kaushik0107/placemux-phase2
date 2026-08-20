def explain_match(result):
    """
    Generate a plain-English explanation for a matching result.
    """

    matched = result.get("matched_skills", [])
    missing = result.get("missing_skills", [])
    breakdown = result.get("match_breakdown", {})
    score = result.get("match_score", 0)

    explanation = []

    if matched:
        explanation.append(
            "Matched required skills: " + ", ".join(sorted(matched)) + "."
        )
    else:
        explanation.append("No required skills were matched.")

    if missing:
        explanation.append(
            "Missing required skills: " + ", ".join(sorted(missing)) + "."
        )
    else:
        explanation.append("No required skills are missing.")

    explanation.append(
        f"Overall match score: {score:.2f}%."
    )

    explanation.append(
        "Match breakdown: "
        f"skill={breakdown.get('skill_match', 0):.2f}%, "
        f"proficiency={breakdown.get('proficiency_match', 0):.2f}%, "
        f"experience={breakdown.get('experience_match', 0):.2f}%, "
        f"role={breakdown.get('role_match', 0):.2f}%, "
        f"location/work mode={breakdown.get('location_match', 0):.2f}%, "
        f"education={breakdown.get('education_match', 0):.2f}%, "
        f"availability={breakdown.get('availability_match', 0):.2f}%, "
        f"salary={breakdown.get('salary_match', 0):.2f}%."
    )

    return " ".join(explanation)
