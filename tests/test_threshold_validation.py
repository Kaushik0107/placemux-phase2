from matching.threshold_validation import validate_skill_thresholds


def test_threshold_validation_passes():
    student = {
        "student_id": "STU_TEST_PASS",
        "verified_skill_scores": {
            "Python": 85,
            "MongoDB": 65
        }
    }

    job = {
        "job_id": "JOB_TEST_PASS",
        "required_skills": [
            "Python",
            "MongoDB"
        ],
        "required_skill_scores": {
            "Python": 70,
            "MongoDB": 50
        }
    }

    result = validate_skill_thresholds(student, job)

    assert result["threshold_validation"] == "PASS"
    assert result["skill_results"][0]["result"] == "PASS"
    assert result["skill_results"][1]["result"] == "PASS"


def test_threshold_validation_fails_below_threshold():
    student = {
        "student_id": "STU_TEST_FAIL",
        "verified_skill_scores": {
            "Python": 60
        }
    }

    job = {
        "job_id": "JOB_TEST_FAIL",
        "required_skills": [
            "Python"
        ],
        "required_skill_scores": {
            "Python": 70
        }
    }

    result = validate_skill_thresholds(student, job)

    assert result["threshold_validation"] == "FAIL"
    assert result["skill_results"][0]["result"] == "FAIL"


def test_threshold_validation_fails_missing_skill():
    student = {
        "student_id": "STU_TEST_MISSING",
        "verified_skill_scores": {}
    }

    job = {
        "job_id": "JOB_TEST_MISSING",
        "required_skills": [
            "Python"
        ],
        "required_skill_scores": {
            "Python": 70
        }
    }

    result = validate_skill_thresholds(student, job)

    assert result["threshold_validation"] == "FAIL"
    assert result["skill_results"][0]["student_score"] == 0
    assert result["skill_results"][0]["result"] == "FAIL"