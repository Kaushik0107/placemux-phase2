import pytest
from matching.proctoring_hardening import evaluate_proctoring_hardening

def test_proctoring_hardening_execution():
    mock_data = [
        {"student_id": "S1", "tab_switches": 0, "gaze_off_screen_ratio": 0.05, "audio_anomaly_count": 0, "session_duration": 3000, "is_flagged_cheating": 0},
        {"student_id": "S2", "tab_switches": 6, "gaze_off_screen_ratio": 0.45, "audio_anomaly_count": 3, "session_duration": 3000, "is_flagged_cheating": 1},
    ] * 20  # Duplicate to create test volume

    model = evaluate_proctoring_hardening(mock_data)
    assert model is not None