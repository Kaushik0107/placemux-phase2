from datetime import datetime, timezone


def evaluate_spend_quality(decision):
    """
    Evaluate whether a paid application is a good-quality spend.

    The existing matching system is the source of truth.
    A SHORTLISTED decision is considered safe to proceed.
    A NOT_SHORTLISTED decision produces a low-fit warning.

    Returns a persisted/demo-friendly guardrail payload.
    """

    match_score = float(decision.get("match_score", 0))
    matching_decision = decision.get("explanation", {}).get(
        "decision",
        "NOT_SHORTLISTED",
    )

    if matching_decision == "SHORTLISTED":
        return {
            "guardrail_decision": "ALLOW",
            "risk_level": "LOW",
            "low_fit_warning": False,
            "match_score": match_score,
            "matching_decision": matching_decision,
            "reason": (
                "The existing matching system shortlisted this "
                "student-job pair, so paid application is allowed."
            ),
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }

    return {
        "guardrail_decision": "WARN",
        "risk_level": "HIGH",
        "low_fit_warning": True,
        "match_score": match_score,
        "matching_decision": matching_decision,
        "reason": (
            "The existing matching system did not shortlist this "
            "student-job pair. Paying to apply may be low-quality spend."
        ),
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
    }