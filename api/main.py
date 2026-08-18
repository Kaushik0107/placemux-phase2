from fastapi import FastAPI, HTTPException
from matching.feature_matching import match_student_to_jobs

app = FastAPI(
    title="PlaceMux Matching API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "PlaceMux Matching API is running"
    }


@app.post("/api/v1/matching/jobs")
def get_job_matches(
    student_id: str,
    top_k: int = 10
):
    try:
        matches = match_student_to_jobs(
            student_id,
            top_k
        )

        return {
            "student_id": student_id,
            "matches": matches
        }

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )