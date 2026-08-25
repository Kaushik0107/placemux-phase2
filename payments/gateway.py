from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


PAYMENT_AMOUNT = 100


@dataclass
class PaymentResult:
    transaction_id: str
    amount: int
    status: str
    gateway: str
    timestamp: str
    reason: str


def create_test_payment(outcome: str) -> PaymentResult:
    """
    Simulate a payment gateway in test mode.

    outcome:
        success -> payment succeeds
        failure -> payment fails
    """

    if outcome not in {"success", "failure"}:
        raise ValueError(
            "payment_outcome must be either 'success' or 'failure'"
        )

    transaction_id = f"TEST_TXN_{uuid4().hex[:12].upper()}"

    timestamp = datetime.now(timezone.utc).isoformat()

    if outcome == "success":
        return PaymentResult(
            transaction_id=transaction_id,
            amount=PAYMENT_AMOUNT,
            status="SUCCESS",
            gateway="TEST_GATEWAY",
            timestamp=timestamp,
            reason="Test payment completed successfully.",
        )

    return PaymentResult(
        transaction_id=transaction_id,
        amount=PAYMENT_AMOUNT,
        status="FAILED",
        gateway="TEST_GATEWAY",
        timestamp=timestamp,
        reason="Test payment was intentionally failed.",
    )