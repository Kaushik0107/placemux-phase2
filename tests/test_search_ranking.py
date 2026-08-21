import pytest

from search.candidate_ranking import rank_candidates_for_job
from search.job_ranking import rank_jobs_for_student


def test_job_ranking_returns_explainable_results_in_score_order():
    ranked_jobs = rank_jobs_for_student("EVAL_STU_004", top_k=2)

    assert len(ranked_jobs) == 2
    assert ranked_jobs[0]["job_id"] == "EVAL_JOB_004"
    assert ranked_jobs[0]["match_score"] >= ranked_jobs[1]["match_score"]

    explanation = ranked_jobs[0]["explanation"]
    assert explanation["decision"] == "SHORTLISTED"
    assert explanation["threshold_validation"] == "PASS"


def test_candidate_ranking_returns_explainable_results_in_score_order():
    ranked_candidates = rank_candidates_for_job(
        "EVAL_JOB_004",
        top_k=2,
    )

    assert len(ranked_candidates) == 2
    assert ranked_candidates[0]["student_id"] == "EVAL_STU_004"
    assert (
        ranked_candidates[0]["match_score"]
        >= ranked_candidates[1]["match_score"]
    )

    explanation = ranked_candidates[0]["explanation"]
    assert explanation["decision"] == "SHORTLISTED"
    assert explanation["threshold_validation"] == "PASS"


def test_job_ranking_rejects_unknown_student():
    with pytest.raises(ValueError, match="Student profile not found"):
        rank_jobs_for_student("UNKNOWN_STUDENT")


def test_candidate_ranking_rejects_unknown_job():
    with pytest.raises(ValueError, match="Job not found"):
        rank_candidates_for_job("UNKNOWN_JOB")