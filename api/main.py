from fastapi import FastAPI, HTTPException

from matching.explanation_store import persist_explanation
from matching.feature_matching import match_student_to_jobs
from search.candidate_ranking import rank_candidates_for_job
from payments.service import process_paid_application

app = FastAPI(
    title="PlaceMux Matching API",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "PlaceMux Matching API is running",
    }


@app.post("/api/v1/matching/jobs")
def get_job_matches(
    student_id: str,
    top_k: int = 10,
    dataset: str = "sample",
):
    if dataset not in {"sample", "evaluation"}:
        raise HTTPException(
            status_code=422,
            detail="dataset must be either 'sample' or 'evaluation'",
        )

    try:
        matches = match_student_to_jobs(
            student_id,
            top_k,
            dataset,
        )

        for match in matches:
            persist_explanation(match["explanation"])

        return {
            "student_id": student_id,
            "dataset": dataset,
            "matches": matches,
        }

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found",
        )

    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Unable to store explanation audit record",
        )

@app.post("/api/v1/ranking/candidates")
def get_ranked_candidates(
    job_id: str,
    top_k: int = 10,
):
    try:
        candidates = rank_candidates_for_job(
            job_id,
            top_k,
        )

        for candidate in candidates:
            persist_explanation(candidate["explanation"])

        return {
            "job_id": job_id,
            "dataset": "evaluation",
            "candidates": candidates,
        }

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Unable to store explanation audit record",
        )

@app.post("/api/v1/applications/apply")
def submit_paid_application(
    student_id: str,
    job_id: str,
    payment_outcome: str = "success",
):
    if payment_outcome not in {"success", "failure"}:
        raise HTTPException(
            status_code=422,
            detail=(
                "payment_outcome must be either "
                "'success' or 'failure'"
            ),
        )

    try:
        return process_paid_application(
            student_id=student_id,
            job_id=job_id,
            payment_outcome=payment_outcome,
        )

    except ValueError as exc:
        message = str(exc)

        if message == "Student profile not found":
            raise HTTPException(
                status_code=404,
                detail=message,
            )

        if message == "Job not found":
            raise HTTPException(
                status_code=404,
                detail=message,
            )

        raise HTTPException(
            status_code=400,
            detail=message,
        )

    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Unable to store payment/application audit record",
        )

from pydantic import BaseModel

class ProctoringCheckRequest(BaseModel):
    student_id: str
    gaze_off_screen_ratio: float
    audio_anomaly_count: int
    tab_switches: int
    session_duration: float

@app.post("/proctoring/verify")
def verify_proctoring_status(req: ProctoringCheckRequest):
    reasons = []
    if req.tab_switches > 3:
        reasons.append(f"high tab switching ({req.tab_switches} times)")
    if req.gaze_off_screen_ratio > 0.30:
        reasons.append(f"frequent off-screen gaze ({req.gaze_off_screen_ratio*100:.1f}% duration)")
    if req.audio_anomaly_count > 2:
        reasons.append(f"multiple audio anomalies ({req.audio_anomaly_count} detected)")

    is_flagged = len(reasons) >= 2 or (req.tab_switches > 5)

    explanation = (
        f"Student {req.student_id} flagged due to: {', '.join(reasons)}."
        if is_flagged
        else f"Student {req.student_id} cleared. Integrity metrics remain within acceptable thresholds."
    )

    return {
        "student_id": req.student_id,
        "is_flagged": is_flagged,
        "status": "FLAGGED" if is_flagged else "CLEARED",
        "explanation": explanation
    }    

from pydantic import BaseModel
from matching.parsing_esign import parse_resume_or_jd, generate_tamper_evident_offer, verify_offer_tamper_evidence

class ParseRequest(BaseModel):
    raw_text: str

class OfferIssueRequest(BaseModel):
    student_id: str
    job_id: str
    salary: int
    role: str

class OfferVerifyRequest(BaseModel):
    offer_payload: dict
    document_hash: str

@app.post("/parsing/v0")
def parse_document(req: ParseRequest):
    result = parse_resume_or_jd(req.raw_text)
    return {
        "status": "SUCCESS",
        "parsed_data": result,
        "explanation": f"Successfully extracted {result['skill_count']} skills matched against ontology."
    }

@app.post("/offers/issue")
def issue_offer(req: OfferIssueRequest):
    offer = generate_tamper_evident_offer(
        student_id=req.student_id,
        job_id=req.job_id,
        offer_details={"salary": req.salary, "role": req.role}
    )
    return offer

@app.post("/offers/verify")
def verify_offer(req: OfferVerifyRequest):
    is_authentic = verify_offer_tamper_evidence(req.offer_payload, req.document_hash)
    return {
        "is_authentic": is_authentic,
        "status": "VERIFIED_AUTHENTIC" if is_authentic else "TAMPER_DETECTED",
        "explanation": "SHA-256 digital signature matches payload." if is_authentic else "Payload hash mismatch! Document has been modified."
    }

from pydantic import BaseModel
from matching.verification_scheduling import schedule_interview

class InterviewScheduleRequest(BaseModel):
    student_id: str
    job_id: str
    slot: str

@app.post("/interviews/schedule")
def schedule_interview_endpoint(req: InterviewScheduleRequest):
    result = schedule_interview(req.student_id, req.job_id, req.slot)
    return {
        "status": "SUCCESS",
        "data": result,
        "explanation": f"Interview confirmed for {req.student_id} on slot {req.slot}."
    }

from pydantic import BaseModel
from matching.ontology_tracking import map_parsed_skills_to_ontology, get_end_to_end_application_status

class OntologyParseRequest(BaseModel):
    raw_text: str

@app.post("/parsing/ontology")
def parse_into_ontology(req: OntologyParseRequest):
    result = map_parsed_skills_to_ontology(req.raw_text)
    return {
        "status": "SUCCESS",
        "data": result
    }

@app.get("/applications/status")
def track_application_status(student_id: str, job_id: str):
    status = get_end_to_end_application_status(student_id, job_id)
    return {
        "status": "SUCCESS",
        "data": status
    }

from pydantic import BaseModel
from matching.trust_signoff import run_ai_trust_signoff

class TrustSignoffRequest(BaseModel):
    student_id: str
    job_id: str
    raw_resume_text: str
    gaze_off_screen_ratio: float
    tab_switches: int

@app.post("/trust/signoff")
def execute_trust_signoff(req: TrustSignoffRequest):
    session_data = {
        "gaze_off_screen_ratio": req.gaze_off_screen_ratio,
        "tab_switches": req.tab_switches
    }
    result = run_ai_trust_signoff(
        student_id=req.student_id,
        job_id=req.job_id,
        raw_resume_text=req.raw_resume_text,
        session_data=session_data
    )
    return {
        "status": "SUCCESS",
        "data": result
    }

from typing import List
from pydantic import BaseModel
from matching.item_bank_onboarding import bulk_onboard_students, analyze_item_bank_quality

class StudentProfile(BaseModel):
    student_id: str
    skills: List[str]

class ItemAnalytic(BaseModel):
    item_id: str
    discrimination_index: float
    error_rate: float

@app.post("/onboarding/bulk")
def bulk_onboard_endpoint(students: List[StudentProfile]):
    students_data = [s.dict() for s in students]
    result = bulk_onboard_students(students_data)
    return {
        "status": "SUCCESS",
        "data": result
    }

@app.post("/items/quality-check")
def item_quality_check_endpoint(items: List[ItemAnalytic]):
    items_data = [item.dict() for item in items]
    result = analyze_item_bank_quality(items_data)
    return {
        "status": "SUCCESS",
        "data": result
    }

from typing import List
from pydantic import BaseModel
from matching.rec_validation import validate_recommendation_quality, get_college_placement_portal_view

class RecEvalItem(BaseModel):
    student_id: str
    recommended_job_ids: List[str]
    relevant_job_ids: List[str]

@app.post("/portals/validate-recommendations")
def validate_recs_endpoint(items: List[RecEvalItem]):
    data = [item.dict() for item in items]
    result = validate_recommendation_quality(data)
    return {
        "status": "SUCCESS",
        "data": result
    }

@app.get("/portals/college-view")
def college_portal_view_endpoint(target_college_id: str, requesting_college_id: str):
    # Simulated database records
    mock_candidates = [
        {"student_id": "STU_101", "college_id": "COLLEGE_A", "score": 88, "status": "SHORTLISTED"},
        {"student_id": "STU_102", "college_id": "COLLEGE_A", "score": 91, "status": "PLACED"},
        {"student_id": "STU_201", "college_id": "COLLEGE_B", "score": 85, "status": "SHORTLISTED"}
    ]
    result = get_college_placement_portal_view(target_college_id, requesting_college_id, mock_candidates)
    if not result["access_granted"]:
        raise HTTPException(status_code=403, detail=result["message"])
    return {
        "status": "SUCCESS",
        "data": result
    }

from typing import List
from pydantic import BaseModel
from matching.fairness_audit import run_fairness_bias_audit, process_dpdp_data_erasure

class CandidateAuditItem(BaseModel):
    student_id: str
    group: str
    is_shortlisted: int

class DPDPForgetRequest(BaseModel):
    student_id: str

@app.post("/security/fairness-audit")
def fairness_audit_endpoint(candidates: List[CandidateAuditItem], protected_attribute: str = "group"):
    data = [c.dict() for c in candidates]
    result = run_fairness_bias_audit(data, protected_attribute)
    return {
        "status": "SUCCESS",
        "data": result
    }

@app.post("/security/dpdp-forget")
def dpdp_forget_endpoint(req: DPDPForgetRequest):
    result = process_dpdp_data_erasure(req.student_id)
    return {
        "status": "SUCCESS",
        "data": result
    }

from typing import List
from pydantic import BaseModel
from matching.drift_retraining import detect_feature_drift, execute_model_retraining

class DriftCheckRequest(BaseModel):
    reference_distribution: List[float]
    current_distribution: List[float]

class RetrainSample(BaseModel):
    feature_val: float
    label: int

@app.post("/mlops/drift-check")
def drift_check_endpoint(req: DriftCheckRequest):
    result = detect_feature_drift(req.reference_distribution, req.current_distribution)
    return {
        "status": "SUCCESS",
        "data": result
    }

@app.post("/mlops/trigger-retrain")
def trigger_retrain_endpoint(samples: List[RetrainSample]):
    data = [s.dict() for s in samples]
    result = execute_model_retraining(data)
    return {
        "status": "SUCCESS",
        "data": result
    }

from pydantic import BaseModel
from matching.registry_feature_store import store_entity_features, get_entity_features, register_model_version

class FeatureStoreRequest(BaseModel):
    entity_id: str
    features: dict

class ModelRegisterRequest(BaseModel):
    model_name: str
    version: str
    metrics: dict
    stage: str = "STAGING"

@app.post("/mlops/features/store")
def store_features_endpoint(req: FeatureStoreRequest):
    result = store_entity_features(req.entity_id, req.features)
    return {"status": "SUCCESS", "data": result}

@app.get("/mlops/features/{entity_id}")
def fetch_features_endpoint(entity_id: str):
    result = get_entity_features(entity_id)
    if not result["found"]:
        raise HTTPException(status_code=404, detail=f"Entity '{entity_id}' not found in Feature Store.")
    return {"status": "SUCCESS", "data": result}

@app.post("/mlops/registry/register")
def register_model_endpoint(req: ModelRegisterRequest):
    result = register_model_version(req.model_name, req.version, req.metrics, req.stage)
    return {"status": "SUCCESS", "data": result}

from typing import List
from pydantic import BaseModel
from matching.launch_signoff import execute_fairness_close_and_signoff

class LaunchAuditItem(BaseModel):
    student_id: str
    group: str
    is_shortlisted: int

class LaunchSignoffRequest(BaseModel):
    model_name: str
    candidates: List[LaunchAuditItem]

@app.post("/launch/rehearsal-signoff")
def launch_rehearsal_endpoint(req: LaunchSignoffRequest):
    candidates_data = [c.dict() for c in req.candidates]
    result = execute_fairness_close_and_signoff(candidates_data, req.model_name)
    return {
        "status": "SUCCESS",
        "data": result
    }

from pydantic import BaseModel
from matching.live_monitoring import record_inference_telemetry, evaluate_production_health

class TelemetryLogRequest(BaseModel):
    endpoint: str
    latency_ms: float
    is_error: bool = False

@app.post("/production/monitoring/log")
def log_telemetry_endpoint(req: TelemetryLogRequest):
    record_inference_telemetry(req.endpoint, req.latency_ms, req.is_error)
    return {"status": "SUCCESS", "message": "Telemetry logged."}

@app.get("/production/monitoring/health")
def production_health_endpoint():
    result = evaluate_production_health()
    return {"status": "SUCCESS", "data": result}


from matching.post_launch_health import generate_model_health_report, triage_intelligence_defects
from typing import List, Optional  # <--- Import Optional
from pydantic import BaseModel

class LogItem(BaseModel):
    student_id: str
    job_id: str
    predicted_match: int
    user_accepted: int
    missing_skill: Optional[str] = None  # <--- Change str = None to Optional[str] = None


@app.post("/health/model-report")
def model_health_report_endpoint(logs: List[LogItem], offline_baseline: float = 0.94):
    logs_data = [l.dict() for l in logs]
    result = generate_model_health_report(logs_data, offline_baseline)
    return {"status": "SUCCESS", "data": result}

@app.post("/health/triage-defects")
def triage_defects_endpoint(logs: List[LogItem]):
    logs_data = [l.dict() for l in logs]
    result = triage_intelligence_defects(logs_data)
    return {"status": "SUCCESS", "data": result}

from typing import List, Optional
from pydantic import BaseModel
from matching.slo_observability import evaluate_inference_slos, MONTHLY_ERROR_BUDGET_CAP

class TelemetryEvalItem(BaseModel):
    latency_ms: float
    is_error: bool = False
    prediction_score: Optional[float] = 0.5

@app.post("/observability/eval-slo")
def eval_slo_endpoint(logs: List[TelemetryEvalItem], p95_target_ms: float = 100.0, min_availability: float = 0.999):
    logs_data = [l.dict() for l in logs]
    result = evaluate_inference_slos(logs_data, p95_target_ms, min_availability)
    return {"status": "SUCCESS", "data": result}

@app.get("/observability/error-budget")
def error_budget_endpoint():
    return {
        "status": "SUCCESS",
        "data": {
            "monthly_budget_capacity": MONTHLY_ERROR_BUDGET_CAP,
            "policy": "SLO breaches freeze non-critical production deployments until budget resets.",
            "owner": "DevOps / MLOps Platform Team"
        }
    }

from pydantic import BaseModel
from matching.latency_profiler import profile_unoptimized_inference_path, profile_optimized_inference_path

class ProfileRequest(BaseModel):
    num_candidates: int = 100

@app.post("/performance/profile-inference")
def profile_inference_endpoint(req: ProfileRequest):
    result = profile_unoptimized_inference_path(req.num_candidates)
    return {"status": "SUCCESS", "data": result}

@app.post("/performance/optimize-inference")
def optimize_inference_endpoint(req: ProfileRequest):
    result = profile_optimized_inference_path(req.num_candidates)
    return {"status": "SUCCESS", "data": result}

from pydantic import BaseModel
from matching.scale_load_test import execute_concurrency_load_test, get_horizontal_scaling_plan

class LoadTestRequest(BaseModel):
    target_qps: int = 600
    breaking_point_qps: int = 500

@app.post("/scale/run-load-test")
def run_load_test_endpoint(req: LoadTestRequest):
    result = execute_concurrency_load_test(req.target_qps, req.breaking_point_qps)
    return {"status": "SUCCESS", "data": result}

@app.get("/scale/plan")
def get_scaling_plan_endpoint():
    result = get_horizontal_scaling_plan()
    return {"status": "SUCCESS", "data": result}

from pydantic import BaseModel
from matching.reliability_signoff import execute_load_test_simulation, generate_reliability_signoff

class LoadTestRequest(BaseModel):
    target_rps: int = 500
    duration_sec: float = 1.0
    force_failure: bool = False

class SignoffRequest(BaseModel):
    model_version: str = "PlaceMux_Phase3_SprintA_v1.0"
    target_rps: int = 500

@app.post("/reliability/load-test")
def load_test_endpoint(req: LoadTestRequest):
    result = execute_load_test_simulation(req.target_rps, req.duration_sec, req.force_failure)
    return {"status": "SUCCESS", "data": result}

@app.post("/reliability/signoff")
def reliability_signoff_endpoint(req: SignoffRequest):
    test_result = execute_load_test_simulation(req.target_rps, 1.0, False)
    result = generate_reliability_signoff(test_result, req.model_version)
    return {"status": "SUCCESS", "data": result}

from typing import List
from pydantic import BaseModel
from matching.growth_instrumentation import log_ranked_impression, log_user_outcome, reconstruct_session_trace

class ImpressionRequest(BaseModel):
    candidate_ids: List[str]
    model_version: str = "PlaceMux_Ranking_v2.1"
    user_id: str = "USER_101"

class OutcomeRequest(BaseModel):
    impression_id: str
    candidate_id: str
    event_type: str  # click, apply, shortlist, dismiss

@app.post("/growth/log-impression")
def log_impression_endpoint(req: ImpressionRequest):
    result = log_ranked_impression(req.candidate_ids, req.model_version, req.user_id)
    return {"status": "SUCCESS", "data": result}

@app.post("/growth/log-outcome")
def log_outcome_endpoint(req: OutcomeRequest):
    result = log_user_outcome(req.impression_id, req.candidate_id, req.event_type)
    if result.get("status") == "ERROR":
        raise HTTPException(status_code=400, detail=result["message"])
    return {"status": "SUCCESS", "data": result}

@app.get("/growth/reconstruct/{impression_id}")
def reconstruct_trace_endpoint(impression_id: str):
    result = reconstruct_session_trace(impression_id)
    if not result["found"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return {"status": "SUCCESS", "data": result}