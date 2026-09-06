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