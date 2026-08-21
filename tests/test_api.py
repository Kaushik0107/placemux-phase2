from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_matching_api_returns_explanation_payload(monkeypatch):
    monkeypatch.setattr(
        "api.main.persist_explanation",
        lambda explanation: explanation,
        raising=False,
    )

    response = client.post(
        "/api/v1/matching/jobs",
        params={
            "student_id": "STU_1001",
            "top_k": 1,
        },
    )

    assert response.status_code == 200

    response_body = response.json()
    match = response_body["matches"][0]
    explanation = match["explanation"]

    assert match["job_id"] == "JOB_2045"
    assert explanation["decision"] == "SHORTLISTED"
    assert explanation["threshold_validation"] == "PASS"
    assert "summary" in explanation
    assert "score_breakdown" in explanation
    assert "skill_results" in explanation


def test_matching_api_persists_each_explanation(monkeypatch):
    saved_explanations = []

    def fake_persist(explanation):
        saved_explanations.append(explanation)
        return explanation

    monkeypatch.setattr(
        "api.main.persist_explanation",
        fake_persist,
        raising=False,
    )

    response = client.post(
        "/api/v1/matching/jobs",
        params={
            "student_id": "STU_1001",
            "top_k": 1,
        },
    )

    assert response.status_code == 200
    assert len(saved_explanations) == 1
    assert saved_explanations[0]["student_id"] == "STU_1001"
    assert saved_explanations[0]["job_id"] == "JOB_2045"

def test_matching_api_explains_a_negative_held_out_match(monkeypatch):
    monkeypatch.setattr(
        "api.main.persist_explanation",
        lambda explanation: explanation,
        raising=False,
    )

    response = client.post(
        "/api/v1/matching/jobs",
        params={
            "student_id": "EVAL_STU_003",
            "top_k": 4,
            "dataset": "evaluation",
        },
    )

    assert response.status_code == 200

    response_body = response.json()

    match = next(
        item
        for item in response_body["matches"]
        if item["job_id"] == "EVAL_JOB_001"
    )

    explanation = match["explanation"]

    assert explanation["decision"] == "NOT_SHORTLISTED"
    assert explanation["threshold_validation"] == "FAIL"
    assert "MongoDB" in explanation["missing_skills"]
    assert "Python" in explanation["summary"]
    assert "MongoDB" in explanation["summary"]

def test_matching_api_returns_404_for_an_unknown_student():
    response = client.post(
        "/api/v1/matching/jobs",
        params={
            "student_id": "UNKNOWN_STUDENT",
            "dataset": "sample",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student profile not found"


def test_matching_api_rejects_an_invalid_dataset():
    response = client.post(
        "/api/v1/matching/jobs",
        params={
            "student_id": "STU_1001",
            "dataset": "invalid",
        },
    )

    assert response.status_code == 422
    assert (
        response.json()["detail"]
        == "dataset must be either 'sample' or 'evaluation'"
    )

def test_candidate_ranking_api_returns_ranked_candidates(monkeypatch):
    monkeypatch.setattr(
        "api.main.persist_explanation",
        lambda explanation: explanation,
        raising=False,
    )

    response = client.post(
        "/api/v1/ranking/candidates",
        params={
            "job_id": "EVAL_JOB_004",
            "top_k": 2,
        },
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["job_id"] == "EVAL_JOB_004"
    assert len(response_body["candidates"]) == 2

    candidate = response_body["candidates"][0]

    assert candidate["student_id"] == "EVAL_STU_004"
    assert candidate["explanation"]["decision"] == "SHORTLISTED"
    assert candidate["explanation"]["threshold_validation"] == "PASS"