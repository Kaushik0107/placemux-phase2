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

### Task 12 — Resume/JD Parsing v0 & Offer Tamper-Evidence

Task 12 delivers initial parsing capabilities for resumes/JDs and cryptographic tamper-evidence for job offers.

- **Parsing v0 (`matching/parsing_esign.py`):** Extracts structured skills mapped to the skills ontology and calculates experience duration from unstructured text[cite: 3].
- **Tamper-Evident Offers:** Generates SHA-256 hashes for canonical offer JSON payloads[cite: 3]. Any post-signing modification to the offer invalidates the document hash[cite: 3].

- **API Endpoints:**
  - `POST /parsing/v0`: Parse raw resume/JD text into structured features[cite: 3].
  - `POST /offers/issue`: Issue an offer document with a cryptographic hash[cite: 3].
  - `POST /offers/verify`: Verify if an offer payload has been tampered with[cite: 3].

### Task 13 — Verification & Interview Scheduling

Task 13 delivers proctoring false-positive reduction and interview slot scheduling for verified candidates.

- **FP Reduction Model (`matching/verification_scheduling.py`):** Trains an ensemble model on flagged-session data to filter out false proctoring flags.
- **Interview Scheduling Engine:** Confirms interview slots for verified candidates[cite: 4].

- **API Endpoint:**
  - `POST /interviews/schedule`: Schedules an interview slot for a student and job pair[cite: 4].

### Task 14 — End-to-End Status Tracking & Parsing

Task 14 connects parsed skill signals into the central skills ontology and provides end-to-end application lifecycle tracking.

- **Ontology Mapper (`matching/ontology_tracking.py`):** Maps unstructured candidate skills into domain-specific canonical categories.
- **Lifecycle Tracker:** Monitors candidate state from application through proctoring, offer issuance, e-signing, and scheduling[cite: 5].

- **API Endpoints:**
  - `POST /parsing/ontology`: Map raw text skills to ontology categories[cite: 5].
  - `GET /applications/status`: Retrieve full candidate lifecycle status[cite: 5].

### Task 15 — Trust Layer Integration & Dry Run

Task 15 delivers the final end-to-end dry run sign-off across the entire PlaceMux intelligence and trust layer.

- **Trust Sign-off Engine (`matching/trust_signoff.py`):** Integrates ontology skill mapping, proctoring verification, offer generation, and cryptographic hash checks into a unified pipeline.
- **API Endpoint:**
  - `POST /trust/signoff`: Executes full end-to-end AI trust dry run[cite: 6].  

### Task 19 — Bulk Onboarding & Recruiter Views

*(Note: Tasks 16, 17, and 18 were not received via email or dashboard; development jumped directly from Task 15 to Task 19.)*

Task 19 delivers bulk student onboarding processing and item-bank quality support for admins and recruiters.

- **Item-Bank Quality Engine (`matching/item_bank_onboarding.py`):** Flags weak assessment items using discrimination index thresholds and extreme error rate analysis[cite: 7].
- **Bulk Onboarding Processor:** Handles bulk profile creation and skill ingestion[cite: 7].

- **API Endpoints:**
  - `POST /onboarding/bulk`: Process bulk student onboarding records[cite: 7].
  - `POST /items/quality-check`: Analyze item-bank analytics and retrieve weak-item flags[cite: 7].

### Task 20 — Portals Integration & Dry Run

Task 20 completes Week 5 Phase 2 by validating recommendation quality metrics and verifying college placement portal data isolation.

- **Recommendation Validation Engine (`matching/rec_validation.py`):** Calculates Precision@K and Recall@K on integrated recommendation runs.
- **Multi-Tenant Security Enforcement:** Guarantees strict college portal data isolation to prevent cross-tenant data leaks.

- **API Endpoints:**
  - `POST /portals/validate-recommendations`: Evaluate recommendation precision/recall on integrated datasets[cite: 8].
  - `GET /portals/college-view`: Secure portal analytics endpoint enforcing college tenant isolation[cite: 8].

### Task 21 — DPDP Consent & Security Foundations

Task 21 initiates the bias/fairness auditing pipeline and implements DPDP compliance mechanisms.

- **Fairness & Bias Audit Engine (`matching/fairness_audit.py`):** Audits candidate selection parity across demographic categories using disparate impact ratio analysis[cite: 9].
- **DPDP Data Deletion Engine:** Facilitates verifiable data erasure in compliance with DPDP regulations[cite: 9].

- **API Endpoints:**
  - `POST /security/fairness-audit`: Evaluate candidate selection fairness across groups[cite: 9].
  - `POST /security/dpdp-forget`: Trigger complete student personal data purging[cite: 9].

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