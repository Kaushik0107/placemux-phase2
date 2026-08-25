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


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

PAYMENT_AUDIT_FILE = DATA_DIR / "payment_audit.jsonl"
APPLICATION_AUDIT_FILE = DATA_DIR / "application_audit.jsonl"

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

    return {
        "student_id": student_id,
        "job_id": job_id,
        "application_id": application_id,
        "application_status": "SUBMITTED",
        "payment": payment_record,
        "match_score": decision["match_score"],
        "matching_decision": decision["explanation"]["decision"],
        "message": (
            "Payment successful. Application submitted successfully."
        ),
    }