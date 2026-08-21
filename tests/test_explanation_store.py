import json

from matching.explanation_store import persist_explanation


def test_persist_explanation_writes_a_jsonl_audit_record(tmp_path):
    audit_file = tmp_path / "explanation_audit.jsonl"

    explanation = {
        "student_id": "STU_1001",
        "job_id": "JOB_2045",
        "decision": "SHORTLISTED",
        "match_score": 95,
        "summary": "All required skill thresholds are met.",
    }

    saved_record = persist_explanation(explanation, audit_file)

    assert audit_file.exists()
    assert saved_record["student_id"] == "STU_1001"
    assert saved_record["job_id"] == "JOB_2045"
    assert "recorded_at" in saved_record

    saved_lines = audit_file.read_text(encoding="utf-8").splitlines()

    assert len(saved_lines) == 1
    assert json.loads(saved_lines[0]) == saved_record