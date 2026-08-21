from fastapi import FastAPI, HTTPException

from matching.explanation_store import persist_explanation
from matching.feature_matching import match_student_to_jobs
from search.candidate_ranking import rank_candidates_for_job

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