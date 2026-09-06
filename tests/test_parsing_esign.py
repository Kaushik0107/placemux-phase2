import pytest
from matching.parsing_esign import parse_resume_or_jd, generate_tamper_evident_offer, verify_offer_tamper_evidence

def test_parse_resume_or_jd():
    text = "Senior Developer with 5 years experience in Python, SQL, and API Design."
    result = parse_resume_or_jd(text)
    assert "python" in result['extracted_skills']
    assert "sql" in result['extracted_skills']
    assert result['years_experience'] == 5

def test_tamper_evident_offer_verification():
    offer = generate_tamper_evident_offer("STU_1", "JOB_1", {"salary": 90000, "role": "ML Engineer"})
    
    # 1. Verification of untouched document
    assert verify_offer_tamper_evidence(offer['offer_payload'], offer['document_hash']) is True

    # 2. Verification of tampered document (e.g. salary changed)
    tampered_payload = dict(offer['offer_payload'])
    tampered_payload['offer_details']['salary'] = 150000
    assert verify_offer_tamper_evidence(tampered_payload, offer['document_hash']) is False