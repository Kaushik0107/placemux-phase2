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

## Task 7/8 — Paid Application Flow

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

## API Endpoints

Student Job Ranking
POST /api/v1/matching/jobs

Example:
/api/v1/matching/jobs?student_id=EVAL_STU_004&top_k=1&dataset=evaluation

Company Candidate Ranking
POST /api/v1/ranking/candidates

Example:
/api/v1/ranking/candidates?job_id=EVAL_JOB_004&top_k=2

## Paid Application
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

## API Demonstration
The API can be started with:
uvicorn api.main:app --reload

Swagger documentation:
http://127.0.0.1:8000/docs

The Swagger interface can be used to demonstrate:
- Student job matching
- Candidate ranking
- Successful paid application
- Failed paid application
- Invalid payment outcome
- Unknown student/job handling
Successful Payment Demonstration
Use the following test data:
Student ID: EVAL_STU_004
Job ID: EVAL_JOB_004
Payment outcome: success
Expected result:
HTTP 200

application_status: SUBMITTED
payment.status: SUCCESS
amount: 100
currency: INR
application_id: APP_...
The successful transaction is written to:
data/payment_audit.jsonl
The application is written to:
data/application_audit.jsonl
Failed Payment Demonstration
Use the following test data:
Student ID: EVAL_STU_004
Job ID: EVAL_JOB_004
Payment outcome: failure
Expected result:
HTTP 200

application_status: NOT_CREATED
payment.status: FAILED
amount: 100
currency: INR
The failed transaction is written to:
data/payment_audit.jsonl
No corresponding application is created in:
data/application_audit.jsonl
Automated Tests
The project includes payment-flow tests in:
tests/test_payment_flow.py
The tests verify:
- Successful payment creates an application.
- Successful payment stores the correct payment amount.
- Successful payment uses INR currency.
- Application is linked to the payment transaction.
- Failed payment does not create an application.
- Failed payment is still recorded in the payment audit.
- Unknown students are rejected.
- Unknown jobs are rejected.
Current test result:
23 passed
Command:
pytest -q

## Evaluation
Run threshold validation evaluation:
python .\evaluation\evaluate_thresholds.py

Run explainability evaluation:
python .\evaluation\evaluate_explainability.py

Run Task 3 job and candidate ranking evaluation:
python .\evaluation\evaluate_ranking.py

Run all automated tests:
pytest -q

Held-out evaluation dataset:
- 4 students
- 4 jobs
- 16 labelled student-job pairs

Current held-out results for both job ranking and candidate ranking:
Metric	Result
Precision	1.0000
Recall	1.0000
False-positive rate	0.0000
Explanation payload coverage	1.0000


These results apply to the supplied held-out, real-shaped dataset. They are not a production-scale performance claim.

## Project Structure
api/
    FastAPI endpoints

data/
    Sample data
    Held-out evaluation data
    Explanation audit records
    Payment audit records
    Application audit records

docs/
    API contract
    Experiment log
    Demo notes

evaluation/
    Evaluation scripts

matching/
    Matching
    Threshold validation
    Explanation
    Persistence logic

payments/
    Test payment gateway
    Paid application service

search/
    Job ranking
    Candidate ranking
    Explanations

tests/
    Automated tests
    Payment-flow tests

## Current Validation Status
The current implementation has been validated with:
pytest -q

23 passed in 0.41s
The payment-flow tests confirm the core business rule:
SUCCESS payment
        ↓
Application created
        ↓
SUBMITTED
and:
FAILED payment
        ↓
Application NOT created
        ↓
NOT_CREATED
The payment and application audit records also confirm the separation between successful and failed transactions.

## Current v1 Limitations
- The payment gateway is a test/simulation gateway and does not process real payments.
- Payment and application records currently use JSONL audit files.
- Ranking currently loads JSON data directly.
- The current implementation is appropriate for the small evaluation dataset.
- A production deployment should use a persistent database for payment/application state.
- A production deployment should integrate a real payment provider.
- A production deployment should use a search index/vector store for large-scale discovery.
- A production deployment should include measured large-scale latency benchmarks.
- Authentication and authorization are not implemented in the current test implementation.
- Payment idempotency and webhook verification would be required for a production payment system.

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

## Current Project Status
Completed functionality currently includes:
- Student ↔ Job matching
- Skill threshold validation
- Job ranking
- Candidate ranking
- Explainable matching
- Held-out evaluation
- Match-quality baseline
- FastAPI endpoints
- Test payment gateway
- Pay-per-application service
- Successful payment flow
- Failed payment flow
- Payment audit records
- Application audit records
- Automated payment-flow tests