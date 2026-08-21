import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_AUDIT_FILE = PROJECT_ROOT / "data" / "explanation_audit.jsonl"


def persist_explanation(explanation, audit_file=None):
    """
    Save one explanation payload as a JSON Lines audit record.
    """

    target_file = (
        Path(audit_file)
        if audit_file is not None
        else DEFAULT_AUDIT_FILE
    )

    target_file.parent.mkdir(parents=True, exist_ok=True)

    saved_record = {
        **explanation,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }

    with target_file.open("a", encoding="utf-8") as file:
        json.dump(saved_record, file)
        file.write("\n")

    return saved_record