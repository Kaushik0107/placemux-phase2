import json

from payments.service import (
    APPLICATION_AUDIT_FILE,
    PAYMENT_AUDIT_FILE,
    process_paid_application,
    reconcile_payment,
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

from payments.guardrail import evaluate_spend_quality


def test_spend_quality_allows_shortlisted_match():
    decision = {
        "match_score": 97.0,
        "explanation": {
            "decision": "SHORTLISTED",
        },
    }

    result = evaluate_spend_quality(decision)

    assert result["guardrail_decision"] == "ALLOW"
    assert result["risk_level"] == "LOW"
    assert result["low_fit_warning"] is False
    assert result["match_score"] == 97.0
    assert result["matching_decision"] == "SHORTLISTED"


def test_spend_quality_warns_for_low_fit_match():
    decision = {
        "match_score": 30.0,
        "explanation": {
            "decision": "NOT_SHORTLISTED",
        },
    }

    result = evaluate_spend_quality(decision)

    assert result["guardrail_decision"] == "WARN"
    assert result["risk_level"] == "HIGH"
    assert result["low_fit_warning"] is True
    assert result["match_score"] == 30.0
    assert result["matching_decision"] == "NOT_SHORTLISTED"

def test_successful_payment_reconciliation():
    result = process_paid_application(
        student_id="EVAL_STU_004",
        job_id="EVAL_JOB_004",
        payment_outcome="success",
    )

    transaction_id = result["payment"]["transaction_id"]

    reconciliation = reconcile_payment(transaction_id)

    assert reconciliation["reconciliation_status"] == "RECONCILED"
    assert reconciliation["payment_status"] == "SUCCESS"
    assert reconciliation["application_found"] is True
    assert reconciliation["receipt_found"] is True
    assert reconciliation["refund_found"] in {True, False}
    assert reconciliation["issues"] == []


def test_failed_payment_reconciliation():
    result = process_paid_application(
        student_id="EVAL_STU_004",
        job_id="EVAL_JOB_004",
        payment_outcome="failure",
    )

    transaction_id = result["payment"]["transaction_id"]

    reconciliation = reconcile_payment(transaction_id)

    assert reconciliation["reconciliation_status"] == "RECONCILED"
    assert reconciliation["payment_status"] == "FAILED"
    assert reconciliation["application_found"] is False
    assert reconciliation["receipt_found"] is False
    assert reconciliation["refund_found"] is False
    assert reconciliation["issues"] == []


def test_unknown_transaction_reconciliation_is_rejected():
    try:
        reconcile_payment("UNKNOWN_TXN")
    except ValueError as exc:
        assert str(exc) == "Payment transaction not found"
    else:
        raise AssertionError(
            "Expected unknown transaction to raise ValueError"
        )


def test_successful_payment_has_spend_quality_guardrail():
    result = process_paid_application(
        student_id="EVAL_STU_004",
        job_id="EVAL_JOB_004",
        payment_outcome="success",
    )

    guardrail = result["spend_quality_guardrail"]

    assert guardrail["guardrail_decision"] == "ALLOW"
    assert guardrail["risk_level"] == "LOW"
    assert guardrail["low_fit_warning"] is False


def test_low_fit_payment_has_warning():
    result = process_paid_application(
        student_id="EVAL_STU_001",
        job_id="EVAL_JOB_002",
        payment_outcome="success",
    )

    guardrail = result["spend_quality_guardrail"]

    assert guardrail["guardrail_decision"] == "WARN"
    assert guardrail["risk_level"] == "HIGH"
    assert guardrail["low_fit_warning"] is True