# PlaceMux Phase 2 — Matching, Search and Discovery

## Overview

PlaceMux matches students with jobs using verified skill scores, experience, role preference, location/work mode, education, availability, and salary expectations.

This project supports:

- Student-to-job matching
- Required-skill threshold validation
- Explainable job ranking for students
- Explainable candidate ranking for companies
- Proctoring hardening and false-positive reduction
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

### Task 7 — Paid Application Flow

The project includes a test-mode pay-per-application workflow.

The flow demonstrates:

1. Student selects a job.
2. The student's profile and job are validated.
3. The existing matching decision is generated.
4. A test payment is created through a simulated payment gateway.
5. The payment transaction is written to an audit file.
6. An application is created only when payment succeeds.
7. A failed payment does not create an application.
8. Application details are written to a separate audit file.

#### Application Fee

- Application fee: `₹100`
- Currency: `INR`
- Gateway: `TEST_GATEWAY`
- Payment modes supported:
  - `success`
  - `failure`

#### Payment Gateway

The simulated gateway is implemented in `payments/gateway.py`. It generates transaction IDs, status, gateway details, UTC timestamps, and payment reasons.

#### Application Service
The pay-per-application business logic is implemented in `payments/service.py`. It handles validation, matching execution, payment storage, and application creation.

#### Audits
- Payment transactions: `data/payment_audit.jsonl`
- Successful applications: `data/application_audit.jsonl`

---

### Task 8 — Receipts, Refunds & Reconciliation

Task 8 adds a controlled pay-per-application flow to PlaceMux while preserving the existing matching, threshold validation, ranking, and explainability logic.

---

### Task 9 — Failure Handling & Resilience

Verified that the paywall does not degrade PlaceMux matching relevance and that payment failures are handled safely and observably.

- Held-out pairs: 16
- Precision: 1.0000 | Recall: 1.0000 | FPR: 0.0000
- Payment failure verified: no application created
- Automated tests: 30 passed

---

### Task 10 — Monetization Integration & Revenue Dashboard

Implemented monetization quality sign-off and revenue verification.

- Paid application flow verified in test mode.
- Payment and application records persisted through audit data.
- Revenue evidence derived from successful payment records.

---

### Task 11 — Proctoring Hardening (Start)

Task 11 begins the intelligence layer hardening for candidate proctoring and assessment integrity verification.

The objective is to replace rigid rule-based flag thresholds with a trained model that significantly reduces False Positive Rates (FPR) on integrity data without creating black-box decisions.

#### Technical Implementation

- **Hardened Classifier (`matching/proctoring_hardening.py`):** Trains an ensemble model on behavioral features (`gaze_off_screen_ratio`, `audio_anomaly_count`, `tab_switches`, `session_duration`).
- **Plain-English Explainability Engine:** Analyzes feature contributions to generate plain-English explanations for every flag decision (`FLAGGED` / `CLEARED`).
- **API Endpoint (`api/main.py`):** Exposes `POST /proctoring/verify` for live candidate integrity check and explainability payload retrieval.
- **Automated Tests (`tests/test_proctoring_hardening.py`):** End-to-end verification and evaluation assertions.

#### Proctoring Hardening Baseline vs. Hardened Model

| Evaluation Metric | Rule Baseline | Hardened Model |
|---|---:|---:|
| **False Positive Rate (FPR)** | 88.00% | **0.00%** |
| **Precision** | 0.17 | **1.00** |
| **Recall** | 1.00 | **1.00** |
| **F1-Score** | 0.29 | **1.00** |
| **Explanation Coverage** | 100.0% | **100.0%** |

---

## API Endpoints

### Student Job Ranking
`POST /api/v1/matching/jobs`

Example:
`/api/v1/matching/jobs?student_id=EVAL_STU_004&top_k=1&dataset=evaluation`

### Company Candidate Ranking
`POST /api/v1/ranking/candidates`

Example:
`/api/v1/ranking/candidates?job_id=EVAL_JOB_004&top_k=2`

### Paid Application
`POST /api/v1/applications/apply`

Parameters:
- `student_id`
- `job_id`
- `payment_outcome` (`success` or `failure`)

Example:
`/api/v1/applications/apply?student_id=EVAL_STU_004&job_id=EVAL_JOB_004&payment_outcome=success`

### Proctoring Verification (Task 11)
`POST /proctoring/verify`

Request Body:
```json
{
  "student_id": "STU_1029",
  "gaze_off_screen_ratio": 0.42,
  "audio_anomaly_count": 1,
  "tab_switches": 5,
  "session_duration": 3600
}

## Setup
1. Activate the virtual environment
.\venv\Scripts\Activate.ps1
2. Install dependencies
python -m pip install -r requirements.txt
3. Run automated tests
pytest -q
4. Start the API
uvicorn api.main:app --reload
5. Open Swagger API documentation
http://127.0.0.1:8000/docs