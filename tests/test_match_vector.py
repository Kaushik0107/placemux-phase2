from matching.feature_matching import (
    load_students,
    load_jobs,
    generate_match_vector,
)


def test_generate_match_vector():
    students = load_students()
    jobs = load_jobs()

    student = students[0]
    job = jobs[0]

    result = generate_match_vector(student, job)

    assert result["student_id"] == "STU_1001"
    assert result["job_id"] == "JOB_2045"

    assert len(result["match_vector"]) == 8

    assert result["match_vector"][0] == 100.0
    assert result["match_vector"][1] == 100.0

    assert result["match_score"] == 95.0



def test_generate_matching_decision():
    from matching.feature_matching import (
        load_students,
        load_jobs,
        generate_matching_decision,
    )

    students = load_students()
    jobs = load_jobs()

    student = students[0]
    job = jobs[0]

    result = generate_matching_decision(student, job)

    assert result["student_id"] == "STU_1001"
    assert result["job_id"] == "JOB_2045"

    assert len(result["match_vector"]) == 8
    assert result["match_score"] == 95.0

    assert result["threshold_validation"] == "PASS"

    assert set(result["matched_skills"]) == {
        "Python",
        "MongoDB",
    }

    assert result["missing_skills"] == []

    assert all(
        item["result"] == "PASS"
        for item in result["skill_results"]
    )    