# PlaceMux Phase 2 — Matching, Search and Discovery

## Overview

PlaceMux matches students with jobs using verified skill scores, experience, role preference, location/work mode, education, availability, and salary expectations.

This project supports:

- Student-to-job matching
- Required-skill threshold validation
- Explainable job ranking for students
- Explainable candidate ranking for companies
- Held-out evaluation metrics
- API response audit records

## Features

### Task 1 — Student ↔ Job Matching

- Weighted match score from 0 to 100
- Eight score components:
  - Skill match: 35%
  - Proficiency match: 20%
  - Experience match: 10%
  - Role match: 10%
  - Location/work mode match: 10%
  - Education match: 5%
  - Availability match: 5%
  - Salary match: 5%

### Task 2 — Skill Threshold Validation

- Validates every required skill against the student's verified score.
- Returns `PASS` only when all required skill thresholds are satisfied.
- Missing skill scores are treated as 0.
- Includes edge-case tests and held-out evaluation.

### Task 3 — Search and Discovery

- Ranks jobs for students.
- Ranks candidates for companies.
- Returns results in descending score order.
- Includes a complete structured explanation payload for every result.
- Supports live API demonstration for both ranking directions.

### Task 4 — Explainable Matching

Each result includes:

- Match score
- `SHORTLISTED` or `NOT_SHORTLISTED` decision
- Threshold validation result
- Matched and missing skills
- Per-skill verified score, threshold, result, and reason
- Weighted score breakdown
- Plain-English summary
- Timestamped audit record in `data/explanation_audit.jsonl`

### Task 5 — Matching Validation

Task 5 validates the matching and ranking system using held-out labelled data and live API testing.

Validation covers:

- Student-to-job ranking
- Company candidate ranking
- Required-skill threshold validation
- Explainable ranking results
- Shortlist and non-shortlist decisions
- API failure handling
- Edge-case handling
- Explanation payload coverage

### Task 6 — Match Quality Baseline

Task 6 establishes a measurable baseline for PlaceMux match quality before further system or monetization-related changes.

The baseline uses the existing rule-based matching and threshold-validation implementation.

A student-job pair is considered a valid match when all required verified-skill thresholds are satisfied according to the existing matching decision logic.

The baseline is evaluated using the held-out evaluation dataset.

#### Baseline Dataset

- Dataset: Evaluation student/job dataset
- Dataset version: Evaluation v1
- Students: 4
- Jobs: 4
- Total labelled student-job pairs: 16
- Positive pairs: 4
- Negative pairs: 12
- Evaluation type: Held-out evaluation

#### Match Quality Results

| Metric | Result |
|---|---:|
| Total labelled pairs | 16 |
| True positives | 4 |
| True negatives | 12 |
| False positives | 0 |
| False negatives | 0 |
| Accuracy | 1.0000 |
| Precision | 1.0000 |
| Recall | 1.0000 |
| False-positive rate | 0.0000 |
| Explanation payload coverage | 1.0000 |

#### Ranking Results

| Ranking direction | Precision | Recall | False-positive rate | Explanation coverage |
|---|---:|---:|---:|---:|
| Job ranking for students | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| Candidate ranking for companies | 1.0000 | 1.0000 | 0.0000 | 1.0000 |

These results establish the current pre-change match-quality baseline for the supplied evaluation dataset.

The results should not be interpreted as production-scale accuracy because the evaluation dataset contains only 4 students, 4 jobs, and 16 labelled student-job pairs.

---

## Setup

### 1. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Run automated tests

```powershell
pytest
```

### 4. Start the API

```powershell
uvicorn api.main:app --reload
```

### 5. Open Swagger API documentation

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Student job ranking

```text
POST /api/v1/matching/jobs
```

Example:

```text
/api/v1/matching/jobs?student_id=EVAL_STU_004&top_k=1&dataset=evaluation
```

### Company candidate ranking

```text
POST /api/v1/ranking/candidates
```

Example:

```text
/api/v1/ranking/candidates?job_id=EVAL_JOB_004&top_k=2
```

## Evaluation

Run threshold validation evaluation:

```powershell
python .\evaluation\evaluate_thresholds.py
```

Run explainability evaluation:

```powershell
python .\evaluation\evaluate_explainability.py
```

Run Task 3 job and candidate ranking evaluation:

```powershell
python .\evaluation\evaluate_ranking.py
```

Held-out evaluation dataset:

- 4 students
- 4 jobs
- 16 labelled student-job pairs

Current held-out results for both job ranking and candidate ranking:

| Metric | Result |
|---|---:|
| Precision | 1.0000 |
| Recall | 1.0000 |
| False-positive rate | 0.0000 |
| Explanation payload coverage | 1.0000 |

These results apply to the supplied held-out, real-shaped dataset. They are not a production-scale performance claim.

## Project Structure

```text
api/          FastAPI endpoints
data/         Sample data, held-out evaluation data, and audit records
docs/         API contract, experiment log, and demo notes
evaluation/   Evaluation scripts
matching/     Matching, threshold validation, and persistence logic
search/       Job ranking, candidate ranking, and explanations
tests/        Automated tests
```

## Current v1 Limitation

Ranking currently loads JSON data directly. It is appropriate for the small evaluation dataset, but a production deployment should use a search index/vector store and include a measured large-scale latency benchmark.