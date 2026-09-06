import pytest
from matching.trust_signoff import run_ai_trust_signoff

def test_run_ai_trust_signoff_success():
    resume = "Python Developer with SQL and Machine Learning experience."
    session = {"gaze_off_screen_ratio": 0.10, "tab_switches": 0}
    
    res = run_ai_trust_signoff("STU_1", "JOB_1", resume, session)
    
    assert res["overall_trust_signoff"] == "PASSED"
    assert res["pipeline_verification"]["tamper_evident_verified"] is True
    assert res["pipeline_verification"]["ontology_skills_mapped"] == 3

def test_run_ai_trust_signoff_proctor_flagged():
    resume = "Python Developer"
    session = {"gaze_off_screen_ratio": 0.50, "tab_switches": 8}
    
    res = run_ai_trust_signoff("STU_2", "JOB_1", resume, session)
    
    assert res["overall_trust_signoff"] == "FAILED_VERIFICATION"
    assert res["pipeline_verification"]["proctoring_status"] == "FLAGGED"