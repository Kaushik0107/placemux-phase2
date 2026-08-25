import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from matching.feature_matching import (
    load_jobs,
    load_students,
    generate_matching_decision,
)

from payments.gateway import create_test_payment
from payments.guardrail import evaluate_spend_quality


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

PAYMENT_AUDIT_FILE = DATA_DIR / "payment_audit.jsonl"
APPLICATION_AUDIT_FILE = DATA_DIR / "application_audit.jsonl"
RECEIPT_AUDIT_FILE = DATA_DIR / "receipt_audit.jsonl"
REFUND_AUDIT_FILE = DATA_DIR / "refund_audit.jsonl"

APPLICATION_FEE = 100


def _append_jsonl(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


def _find_student(student_id):
    students = load_students("evaluation")

    return next(
        (
            student
            for student in students
            if student["student_id"] == student_id
        ),
        None,
    )


def _find_job(job_id):
    jobs = load_jobs("evaluation")

    return next(
        (
            job
            for job in jobs
            if job["job_id"] == job_id
        ),
        None,
    )


def process_paid_application(
    student_id,
    job_id,
    payment_outcome,
):
    """
    Process the complete pay-per-application flow.

    Application is created only after successful payment.
    A failed payment never creates an application.
    """

    student = _find_student(student_id)

    if student is None:
        raise ValueError("Student profile not found")

    job = _find_job(job_id)

    if job is None:
        raise ValueError("Job not found")

    decision = generate_matching_decision(student, job)

    guardrail = evaluate_spend_quality(decision)
    
    payment = create_test_payment(payment_outcome)

    payment_record = {
    "transaction_id": payment.transaction_id,
    "student_id": student_id,
    "job_id": job_id,
    "amount": payment.amount,
    "currency": "INR",
    "status": payment.status,
    "gateway": payment.gateway,
    "timestamp": payment.timestamp,
    "reason": payment.reason,
    "guardrail_decision": guardrail["guardrail_decision"],
    "risk_level": guardrail["risk_level"],
    "low_fit_warning": guardrail["low_fit_warning"],
    "guardrail_reason": guardrail["reason"],
}

    _append_jsonl(
        PAYMENT_AUDIT_FILE,
        payment_record,
    )

    if payment.status != "SUCCESS":
     return {
        "student_id": student_id,
        "job_id": job_id,
        "application_status": "NOT_CREATED",
        "payment": payment_record,
        "match_score": decision["match_score"],
        "matching_decision": decision["explanation"]["decision"],
        "spend_quality_guardrail": guardrail,
        "message": (
            "Payment failed. No application was created."
        ),
    }

    application_id = f"APP_{uuid4().hex[:12].upper()}"

    application_record = {
        "application_id": application_id,
        "student_id": student_id,
        "job_id": job_id,
        "payment_transaction_id": payment.transaction_id,
        "amount": APPLICATION_FEE,
        "currency": "INR",
        "status": "SUBMITTED",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }

    _append_jsonl(
        APPLICATION_AUDIT_FILE,
        application_record,
    )
    receipt_record = {
    "receipt_id": f"RCPT_{uuid4().hex[:12].upper()}",
    "application_id": application_id,
    "transaction_id": payment.transaction_id,
    "student_id": student_id,
    "job_id": job_id,
    "amount": payment.amount,
    "currency": "INR",
    "payment_status": payment.status,
    "application_status": "SUBMITTED",
    "issued_at": datetime.now(timezone.utc).isoformat(),
}
    _append_jsonl(
    RECEIPT_AUDIT_FILE,
    receipt_record,
)

    return {
    "student_id": student_id,
    "job_id": job_id,
    "application_id": application_id,
    "application_status": "SUBMITTED",
    "receipt": receipt_record,
    "payment": payment_record,
    "match_score": decision["match_score"],
    "matching_decision": decision["explanation"]["decision"],
    "spend_quality_guardrail": guardrail,
    "message": (
        "Payment successful. Application submitted successfully."
    ),
}

def process_refund(
    transaction_id,
    reason="Application refund requested",
):
    """
    Process a test-mode refund for a successful payment.

    A refund is allowed only when the original payment
    transaction exists and has SUCCESS status.
    """

    if not PAYMENT_AUDIT_FILE.exists():
        raise ValueError("Payment transaction not found")

    payment_record = None

    with PAYMENT_AUDIT_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            record = json.loads(line)

            if record.get("transaction_id") == transaction_id:
                payment_record = record
                break

    if payment_record is None:
        raise ValueError("Payment transaction not found")

    if payment_record.get("status") != "SUCCESS":
        raise ValueError(
            "Only successful payments can be refunded"
        )

    refund_record = {
        "refund_id": f"REF_{uuid4().hex[:12].upper()}",
        "transaction_id": transaction_id,
        "student_id": payment_record["student_id"],
        "job_id": payment_record["job_id"],
        "amount": payment_record["amount"],
        "currency": payment_record["currency"],
        "status": "REFUNDED",
        "reason": reason,
        "refunded_at": datetime.now(timezone.utc).isoformat(),
    }

    _append_jsonl(
        REFUND_AUDIT_FILE,
        refund_record,
    )

    return refund_record

def reconcile_payment(transaction_id):
    """
    Reconcile payment, application, receipt, and refund records
    for a single transaction.
    """

    payment_records = []

    if PAYMENT_AUDIT_FILE.exists():
        with PAYMENT_AUDIT_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    payment_records.append(json.loads(line))

    payment = next(
        (
            record
            for record in payment_records
            if record["transaction_id"] == transaction_id
        ),
        None,
    )

    if payment is None:
        raise ValueError("Payment transaction not found")

    application_records = []

    if APPLICATION_AUDIT_FILE.exists():
        with APPLICATION_AUDIT_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            for line in file:
                if line.strip():
                    application_records.append(json.loads(line))

    application = next(
        (
            record
            for record in application_records
            if record["payment_transaction_id"] == transaction_id
        ),
        None,
    )

    receipt_records = []

    if RECEIPT_AUDIT_FILE.exists():
        with RECEIPT_AUDIT_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            for line in file:
                if line.strip():
                    receipt_records.append(json.loads(line))

    receipt = next(
        (
            record
            for record in receipt_records
            if record["transaction_id"] == transaction_id
        ),
        None,
    )

    refund_records = []

    if REFUND_AUDIT_FILE.exists():
        with REFUND_AUDIT_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            for line in file:
                if line.strip():
                    refund_records.append(json.loads(line))

    refund = next(
        (
            record
            for record in refund_records
            if record["transaction_id"] == transaction_id
        ),
        None,
    )

    issues = []

    if payment["status"] == "SUCCESS":
        if application is None:
            issues.append(
                "Successful payment has no application record"
            )

        if receipt is None:
            issues.append(
                "Successful payment has no receipt record"
            )

        if application is not None:
            if application["payment_transaction_id"] != transaction_id:
                issues.append(
                    "Application transaction does not match payment"
                )

        if receipt is not None:
            if receipt["transaction_id"] != transaction_id:
                issues.append(
                    "Receipt transaction does not match payment"
                )

    if payment["status"] == "FAILED":
        if application is not None:
            issues.append(
                "Failed payment has an application record"
            )

        if receipt is not None:
            issues.append(
                "Failed payment has a receipt record"
            )

    if refund is not None:
        if payment["status"] != "SUCCESS":
            issues.append(
                "Refund exists for a non-successful payment"
            )

        if refund["transaction_id"] != transaction_id:
            issues.append(
                "Refund transaction does not match payment"
            )

        if refund["amount"] != payment["amount"]:
            issues.append(
                "Refund amount does not match payment amount"
            )

    reconciliation_status = (
        "RECONCILED"
        if not issues
        else "MISMATCH"
    )

    return {
        "transaction_id": transaction_id,
        "reconciliation_status": reconciliation_status,
        "payment_status": payment["status"],
        "application_found": application is not None,
        "receipt_found": receipt is not None,
        "refund_found": refund is not None,
        "issues": issues,
        "reconciled_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }