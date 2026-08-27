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

## Task 7 — Paid Application Flow

The project now includes a test-mode pay-per-application workflow.

The flow demonstrates:

1. Student selects a job.
2. The student's profile and job are validated.
3. The existing matching decision is generated.
4. A test payment is created through a simulated payment gateway.
5. The payment transaction is written to an audit file.
6. An application is created only when payment succeeds.
7. A failed payment does not create an application.
8. Application details are written to a separate audit file.

### Application Fee

- Application fee: `₹100`
- Currency: `INR`
- Gateway: `TEST_GATEWAY`
- Payment modes supported:
  - `success`
  - `failure`

This is a test/simulation implementation and does not process real payments.

---


### Payment Gateway

The simulated gateway is implemented in:

## payments/gateway.py
It generates:
- Test transaction ID
- Payment amount
- Payment status
- Gateway name
- UTC timestamp
- Payment reason

Successful test payments return:
status = SUCCESS

Failed test payments return:
status = FAILED

## Application Service
The pay-per-application business logic is implemented in:
payments/service.py

The service:
- Validates the student.
- Validates the job.
- Generates the existing matching decision.
- Processes the test payment.
- Stores payment audit information.
- Creates an application only after successful payment.
- Stores application audit information.
- Returns the application/payment status.

## Payment Audit
Payment transactions are recorded in:
data/payment_audit.jsonl
Each payment audit record contains:
- Transaction ID
- Student ID
- Job ID
- Amount
- Currency
- Payment status
- Gateway
- Timestamp
- Reason

## Application Audit
Successful applications are recorded in:
data/application_audit.jsonl
Each application audit record contains:
- Application ID
- Student ID
- Job ID
- Payment transaction ID
- Amount
- Currency
- Application status
- Submission timestamp

Successful Payment Behaviour
For a successful payment:
Payment status: SUCCESS
Application status: SUBMITTED
Application ID: APP_...
The application is created and linked to the successful payment transaction.

Failed Payment Behaviour
For a failed payment:
Payment status: FAILED
Application status: NOT_CREATED
No application audit record is created.
This ensures that a failed payment cannot result in a submitted application.

# Task 8 — Receipts, Refunds & Reconciliation

Task 8 adds a controlled pay-per-application flow to PlaceMux while preserving the existing matching, threshold validation, ranking, and explainability logic.

The monetization flow uses the existing match decision to evaluate whether a student's application spend is likely to be high quality.

## Task 8 Flow

Student + Job
      ↓
Existing Matching System
      ↓
Match Score + Shortlist Decision
      ↓
Spend-Quality Guardrail
      ↓
ALLOW / WARN
      ↓
Test Payment Gateway
      ↓
Payment Audit
      ↓
Application
      ↓
Receipt
      ↓
Refund (when requested)
      ↓
Payment/Application Reconciliation

## Task 9 — Failure Handling & Resilience

Verified that the paywall does not degrade PlaceMux matching relevance and
that payment failures are handled safely and observably.

- Held-out pairs: 16
- Shortlisted: 4
- Not shortlisted: 12
- Precision: 1.0000
- Recall: 1.0000
- False-positive rate: 0.0000
- Explanation coverage: 1.0000
- Payment failure verified: no application created
- Payment reconciliation verified
- Automated tests: 30 passed

**Result:** No relevance regression detected after the payment/paywall changes.

## Task 10 — Monetization Integration & Revenue Dashboard

Implemented monetization quality sign-off and revenue verification.

- Matching quality evaluated on held-out evaluation data.
- Precision, recall and false-positive rate verified numerically.
- Explanation coverage verified.
- Paid application flow verified in test mode.
- Payment and application records persisted through audit data.
- Revenue evidence derived from successful payment records.
- Payment failure handling verified.
- Final automated test suite passes.

## API Endpoints

Student Job Ranking
POST /api/v1/matching/jobs

Example:
/api/v1/matching/jobs?student_id=EVAL_STU_004&top_k=1&dataset=evaluation

Company Candidate Ranking
POST /api/v1/ranking/candidates

Example:
/api/v1/ranking/candidates?job_id=EVAL_JOB_004&top_k=2

Paid Application
POST /api/v1/applications/apply

Parameters:
student_id
job_id
payment_outcome
Supported payment outcomes:
success
failure

Example successful payment:
/api/v1/applications/apply?student_id=EVAL_STU_004&job_id=EVAL_JOB_004&payment_outcome=success

Example failed payment:
/api/v1/applications/apply?student_id=EVAL_STU_004&job_id=EVAL_JOB_004&payment_outcome=failure

Invalid payment outcomes are rejected with HTTP 422.
Unknown students and jobs are rejected with HTTP 404.

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