# PlaceMux Phase 2

## Task 1 – Student ↔ Job Matching

### Objective
Design and implement the foundation for matching students with relevant job opportunities.

### Completed
- Defined student and job feature spaces
- Implemented weighted matching logic
- Implemented verified skill proficiency matching
- Implemented match vector generation
- Implemented explainable match results
- Implemented FastAPI matching endpoint
- Added unit tests

### Matching Weights
- Skill Match – 35%
- Proficiency Match – 20%
- Experience Match – 10%
- Role Match – 10%
- Location/Work Mode – 10%
- Education – 5%
- Availability – 5%
- Salary – 5%

### API
`POST /api/v1/matching/jobs`

Returns:
- Overall match score
- Match breakdown
- Matched skills
- Missing skills
- Ranked jobs

---

## Task 2 – Job Skill Threshold Validation

### Objective
Validate whether a student's verified skill scores meet the minimum competency thresholds required by a job.

### Completed
- Implemented per-skill threshold validation
- Added PASS/FAIL decisions
- Added explainable validation reasons
- Handled missing skills and edge cases
- Added evaluation dataset with student-job pairs
- Added precision, recall and false-positive-rate evaluation
- Added automated tests

### Evaluation Results
- Total pairs: 16
- True Positives: 4
- True Negatives: 12
- False Positives: 0
- False Negatives: 0
- Precision: 1.0000
- Recall: 1.0000
- False-Positive Rate: 0.0000

> These results are based on the current held-out real-shaped evaluation dataset and are intended for functional evaluation, not production-level accuracy claims.

---

## Technology

- Python
- FastAPI
- Uvicorn
- JSON
- Pytest

## Project Structure

```text
data/          → Sample and evaluation datasets
matching/      → Matching and threshold-validation logic
evaluation/    → Evaluation scripts
tests/         → Automated tests
docs/          → Design and experiment documentation
api/           → FastAPI application

## How to Run

1. Activate virtual environment
venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Run tests
pytest -q

4. Start API
python -m uvicorn api.main --reload

5. Open Swagger
http://127.0.0.1:8000/docs