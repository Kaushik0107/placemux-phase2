import json

from payments.service import (
    APPLICATION_AUDIT_FILE,
    PAYMENT_AUDIT_FILE,
    process_paid_application,
)


def test_successful_payment_creates_application(
    monkeypatch,
    tmp_path,
):
    payment_file = tmp_path / "payment_audit.jsonl"
    application_file = tmp_path / "application_audit.jsonl"

    monkeypatch.setattr(
        "payments.service.PAYMENT_AUDIT_FILE",
        payment_file,
    )

    monkeypatch.setattr(
        "payments.service.APPLICATION_AUDIT_FILE",
        application_file,
    )

    result = process_paid_application(
        student_id="EVAL_STU_004",
        job_id="EVAL_JOB_004",
        payment_outcome="success",
    )

    assert result["application_status"] == "SUBMITTED"
    assert result["payment"]["status"] == "SUCCESS"
    assert result["payment"]["amount"] == 100
    assert result["payment"]["currency"] == "INR"
    assert result["application_id"].startswith("APP_")

    assert payment_file.exists()
    assert application_file.exists()

    payment_record = json.loads(
        payment_file.read_text(encoding="utf-8").strip()
    )

    application_record = json.loads(
        application_file.read_text(encoding="utf-8").strip()
    )

    assert payment_record["status"] == "SUCCESS"
    assert payment_record["amount"] == 100

    assert application_record["status"] == "SUBMITTED"
    assert (
        application_record["payment_transaction_id"]
        == payment_record["transaction_id"]
    )


def test_failed_payment_does_not_create_application(
    monkeypatch,
    tmp_path,
):
    payment_file = tmp_path / "payment_audit.jsonl"
    application_file = tmp_path / "application_audit.jsonl"

    monkeypatch.setattr(
        "payments.service.PAYMENT_AUDIT_FILE",
        payment_file,
    )

    monkeypatch.setattr(
        "payments.service.APPLICATION_AUDIT_FILE",
        application_file,
    )

    result = process_paid_application(
        student_id="EVAL_STU_004",
        job_id="EVAL_JOB_004",
        payment_outcome="failure",
    )

    assert result["application_status"] == "NOT_CREATED"
    assert result["payment"]["status"] == "FAILED"
    assert result["payment"]["amount"] == 100

    assert payment_file.exists()

    payment_record = json.loads(
        payment_file.read_text(encoding="utf-8").strip()
    )

    assert payment_record["status"] == "FAILED"

    assert not application_file.exists()


def test_unknown_student_is_rejected():
    try:
        process_paid_application(
            student_id="UNKNOWN_STUDENT",
            job_id="EVAL_JOB_004",
            payment_outcome="success",
        )
    except ValueError as exc:
        assert str(exc) == "Student profile not found"
    else:
        raise AssertionError(
            "Expected unknown student to raise ValueError"
        )


def test_unknown_job_is_rejected():
    try:
        process_paid_application(
            student_id="EVAL_STU_004",
            job_id="UNKNOWN_JOB",
            payment_outcome="success",
        )
    except ValueError as exc:
        assert str(exc) == "Job not found"
    else:
        raise AssertionError(
            "Expected unknown job to raise ValueError"
        )