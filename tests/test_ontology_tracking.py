import pytest
from matching.ontology_tracking import map_parsed_skills_to_ontology, get_end_to_end_application_status

def test_map_parsed_skills_to_ontology():
    text = "Proficient in Python, Machine Learning, and SQL databases."
    res = map_parsed_skills_to_ontology(text)
    assert res["total_ontology_matches"] == 3
    assert "python" in res["ontology_skills"]["software_engineering"]
    assert "machine_learning" in res["ontology_skills"]["data_ai"]

def test_get_end_to_end_application_status():
    status = get_end_to_end_application_status("STU_100", "JOB_200")
    assert status["current_status"] == "INTERVIEW_SCHEDULED"
    assert status["lifecycle_stages"]["offer_signed"] is True