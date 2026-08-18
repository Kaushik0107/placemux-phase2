from matching.feature_matching import match_student_to_jobs


def test_student_matching():
    matches = match_student_to_jobs("STU_1001")

    assert len(matches) > 0
    assert matches[0]["job_id"] == "JOB_2045"
    assert "match_score" in matches[0]