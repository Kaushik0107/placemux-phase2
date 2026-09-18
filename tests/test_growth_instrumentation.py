import pytest
from matching.growth_instrumentation import log_ranked_impression, log_user_outcome, reconstruct_session_trace

def test_growth_event_flow():
    # 1. Log Impression
    imp_res = log_ranked_impression(["STU_1", "STU_2"], "v1.0", "U1")
    assert imp_res["status"] == "LOGGED"
    imp_id = imp_res["impression_id"]

    # 2. Log Outcome
    out_res = log_user_outcome(imp_id, "STU_2", "apply")
    assert out_res["status"] == "RECORDED"
    assert out_res["position"] == 2

    # 3. Reconstruct Trace
    trace = reconstruct_session_trace(imp_id)
    assert trace["found"] is True
    assert len(trace["outcomes"]) == 1
    assert trace["outcomes"][0]["event_type"] == "apply"