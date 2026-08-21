from search.explainability import build_explanation_payload


def test_positive_match_explanation_is_complete():
    result = {
        "student_id": "EVAL_STU_004",
        "job_id": "EVAL_JOB_004",
        "match_score": 97.5,
        "match_breakdown": {
            "skill_match": 100,
            "proficiency_match": 100,
            "experience_match": 100,
            "role_match": 100,
            "location_match": 70,
            "education_match": 100,
            "availability_match": 100,
            "salary_match": 100,
        },
        "matched_skills": ["Python", "Django", "PostgreSQL"],
        "missing_skills": [],
        "threshold_validation": "PASS",
        "skill_results": [
            {
                "skill": "Python",
                "student_score": 88,
                "required_threshold": 70,
                "result": "PASS",
                "reason": "Python score 88 meets the required threshold of 70.",
            }
        ],
    }

    payload = build_explanation_payload(result)

    assert payload["decision"] == "SHORTLISTED"
    assert payload["threshold_validation"] == "PASS"
    assert payload["matched_skills"] == [
        "Django",
        "PostgreSQL",
        "Python",
    ]
    assert payload["missing_skills"] == []
    assert "summary" in payload
    assert "score_breakdown" in payload
    assert "skill_results" in payload


def test_negative_match_explanation_shows_why():
    result = {
        "student_id": "EVAL_STU_003",
        "job_id": "EVAL_JOB_001",
        "match_score": 60.0,
        "match_breakdown": {},
        "matched_skills": ["Python"],
        "missing_skills": ["MongoDB"],
        "threshold_validation": "FAIL",
        "skill_results": [
            {
                "skill": "Python",
                "student_score": 55,
                "required_threshold": 70,
                "result": "FAIL",
                "reason": "Python score 55 is below the required threshold of 70.",
            },
            {
                "skill": "MongoDB",
                "student_score": 0,
                "required_threshold": 60,
                "result": "FAIL",
                "reason": "MongoDB score 0 is below the required threshold of 60.",
            },
        ],
    }

    payload = build_explanation_payload(result)

    assert payload["decision"] == "NOT_SHORTLISTED"
    assert payload["threshold_validation"] == "FAIL"
    assert payload["missing_skills"] == ["MongoDB"]
    assert "MongoDB" in payload["summary"]
    assert "Python" in payload["summary"]