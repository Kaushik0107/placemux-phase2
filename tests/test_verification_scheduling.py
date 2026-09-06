import pytest
from matching.verification_scheduling import evaluate_fp_reduction, schedule_interview

def test_fp_reduction_eval():
    mock_sessions = [
        {"tab_switches": 0, "gaze_off_screen_ratio": 0.05, "audio_anomaly_count": 0, "session_duration": 3000, "is_truly_flagged": 0},
        {"tab_switches": 5, "gaze_off_screen_ratio": 0.40, "audio_anomaly_count": 3, "session_duration": 3000, "is_truly_flagged": 1},
    ] * 20

    model = evaluate_fp_reduction(mock_sessions)
    assert model is not None

def test_schedule_interview():
    res = schedule_interview("STU_100", "JOB_200", "2026-09-10T10:00:00Z")
    assert res["status"] == "CONFIRMED"
    assert res["student_id"] == "STU_100"