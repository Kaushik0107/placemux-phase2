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

- **Parsing v0 (`matching/parsing_esign.py`):** Extracts structured skills mapped to the skills ontology and calculates experience duration from unstructured text.
- **Tamper-Evident Offers:** Generates SHA-256 hashes for canonical offer JSON payloads. Any post-signing modification to the offer invalidates the document hash.

- **API Endpoints:**
  - `POST /parsing/v0`: Parse raw resume/JD text into structured features.
  - `POST /offers/issue`: Issue an offer document with a cryptographic hash.
  - `POST /offers/verify`: Verify if an offer payload has been tampered with.

### Task 13 — Verification & Interview Scheduling

Task 13 delivers proctoring false-positive reduction and interview slot scheduling for verified candidates.

- **FP Reduction Model (`matching/verification_scheduling.py`):** Trains an ensemble model on flagged-session data to filter out false proctoring flags.
- **Interview Scheduling Engine:** Confirms interview slots for verified candidates.

- **API Endpoint:**
  - `POST /interviews/schedule`: Schedules an interview slot for a student and job pai.

### Task 14 — End-to-End Status Tracking & Parsing

Task 14 connects parsed skill signals into the central skills ontology and provides end-to-end application lifecycle tracking.

- **Ontology Mapper (`matching/ontology_tracking.py`):** Maps unstructured candidate skills into domain-specific canonical categories.
- **Lifecycle Tracker:** Monitors candidate state from application through proctoring, offer issuance, e-signing, and scheduling.

- **API Endpoints:**
  - `POST /parsing/ontology`: Map raw text skills to ontology categories.
  - `GET /applications/status`: Retrieve full candidate lifecycle status.

### Task 15 — Trust Layer Integration & Dry Run

Task 15 delivers the final end-to-end dry run sign-off across the entire PlaceMux intelligence and trust layer.

- **Trust Sign-off Engine (`matching/trust_signoff.py`):** Integrates ontology skill mapping, proctoring verification, offer generation, and cryptographic hash checks into a unified pipeline.
- **API Endpoint:**
  - `POST /trust/signoff`: Executes full end-to-end AI trust dry run.  

### Task 19 — Bulk Onboarding & Recruiter Views

*(Note: Tasks 16, 17, and 18 were not received via email or dashboard; development jumped directly from Task 15 to Task 19.)*

Task 19 delivers bulk student onboarding processing and item-bank quality support for admins and recruiters.

- **Item-Bank Quality Engine (`matching/item_bank_onboarding.py`):** Flags weak assessment items using discrimination index thresholds and extreme error rate analysis.
- **Bulk Onboarding Processor:** Handles bulk profile creation and skill ingestion.

- **API Endpoints:**
  - `POST /onboarding/bulk`: Process bulk student onboarding records.
  - `POST /items/quality-check`: Analyze item-bank analytics and retrieve weak-item flags.

### Task 20 — Portals Integration & Dry Run

Task 20 completes Week 5 Phase 2 by validating recommendation quality metrics and verifying college placement portal data isolation.

- **Recommendation Validation Engine (`matching/rec_validation.py`):** Calculates Precision@K and Recall@K on integrated recommendation runs.
- **Multi-Tenant Security Enforcement:** Guarantees strict college portal data isolation to prevent cross-tenant data leaks.

- **API Endpoints:**
  - `POST /portals/validate-recommendations`: Evaluate recommendation precision/recall on integrated datasets.
  - `GET /portals/college-view`: Secure portal analytics endpoint enforcing college tenant isolation.

### Task 21 — DPDP Consent & Security Foundations

Task 21 initiates the bias/fairness auditing pipeline and implements DPDP compliance mechanisms.

- **Fairness & Bias Audit Engine (`matching/fairness_audit.py`):** Audits candidate selection parity across demographic categories using disparate impact ratio analysis.
- **DPDP Data Deletion Engine:** Facilitates verifiable data erasure in compliance with DPDP regulations.

- **API Endpoints:**
  - `POST /security/fairness-audit`: Evaluate candidate selection fairness across groups.
  - `POST /security/dpdp-forget`: Trigger complete student personal data purging.

### Task 22 — Data-Subject Rights & Resilience

Task 22 stands up feature drift monitoring and automated model retraining pipelines for MLOps resilience.

- **Drift Monitoring Engine (`matching/drift_retraining.py`):** Uses KS statistical testing to compare baseline feature distributions against live inference inputs.
- **Automated Retraining Module:** Triggers automated model refitting when feature distribution drift is detected.

- **API Endpoints:**
  - `POST /mlops/drift-check`: Evaluate statistical feature drift between reference and live distributions.
  - `POST /mlops/trigger-retrain`: Execute automated model retraining on new production data.
  
  ### Task 23 — Hardening, Scale & MLOps

Task 23 establishes the MLOps foundation with a central feature store and model registry.

- **Feature Store & Registry Engine (`matching/registry_feature_store.py`):** Persists feature space vectors and manages model metadata/stages.

- **API Endpoints:**
  - `POST /mlops/features/store`: Ingest entity features into the feature store.
  - `GET /mlops/features/{entity_id}`: Retrieve online features for inference.
  - `POST /mlops/registry/register`: Register model artifacts with evaluation metrics and deployment stages.

### Task 24 — Launch Rehearsal

Task 24 closes the fairness audit and issues final ML model sign-offs for production launch readiness.

- **Launch Rehearsal Engine (`matching/launch_signoff.py`):** Closes fairness auditing and validates disparate impact metrics against the 80% threshold.

- **API Endpoint:**
  - `POST /launch/rehearsal-signoff`: Run launch rehearsal fairness checks and generate model sign-off certificates.

### Task 25 — Go-Live

Task 25 delivers live model monitoring and production cutover verification for the PlaceMux platform.

- **Live Monitoring Engine (`matching/live_monitoring.py`):** Tracks production inference latency distribution and error rates against SLAs.

- **API Endpoints:**
  - `POST /production/monitoring/log`: Ingest live production inference telemetry logs.
  - `GET /production/monitoring/health`: Evaluate production health SLAs and cutover sign-off.

### Phase 3 Task 1 — Post-Launch Health & Incident Triage

Task 1 of Phase 3 establishes the post-launch model health baseline and triages live intelligence defects.

- **Health & Defect Triage Engine (`matching/post_launch_health.py`):** Calculates offline vs online F1 metric gaps and ranks intelligence defects from interaction logs.

- **API Endpoints:**
  - `POST /health/model-report`: Generate live offline vs. online performance gap report.
  - `POST /health/triage-defects`: Triage interaction defects and generate Phase 3 backlog.

### Phase 3 Task 2 — Observability Deep-Dive, SLOs & Error Budgets

Task 2 establishes inference layer SLOs, automated alert triggers, and error budget tracking.

- **SLO Engine & Alerting (`matching/slo_observability.py`):** Monitors p95 latency, availability floors, and prediction score variance.

- **API Endpoints:**
  - `POST /observability/eval-slo`: Evaluate live telemetry against SLO thresholds and return active alerts.
  - `GET /observability/error-budget`: Retrieve error budget policy and capacity status.

### Phase 3 Task 3 — Performance Profiling & Bottleneck Elimination

Task 3 delivers inference latency profiling and optimization to meet latency SLOs without sacrificing matching quality.

- **Performance Profiler Engine (`matching/latency_profiler.py`):** Profiles pipeline stages and executes vectorized batch optimization.

- **API Endpoints:**
  - `POST /performance/profile-inference`: Profile unoptimized inference path latency and compute cost.
  - `POST /performance/optimize-inference`: Execute optimized inference path meeting latency SLOs.

### Phase 3 Task 4 — Horizontal Scale & Load Readiness

Task 4 proves intelligence layer resilience under marketplace-scale concurrency and formulates scaling plans.

- **Load Test & Scaling Engine (`matching/scale_load_test.py`):** Executes high-QPS load simulations, identifies system breaking points, and triggers precompute fallbacks.

- **API Endpoints:**
  - `POST /scale/run-load-test`: Execute concurrency load test and inspect fallback state.
  - `GET /scale/plan`: Retrieve horizontal pod autoscaling specifications for DevOps integration.

### Phase 3 Task 5 — Reliability Sign-off & Scale Integration

Task 5 signs off the intelligence layer as scale-ready with sustained load testing and verified fallbacks.

- **Scale Reliability Engine (`matching/reliability_signoff.py`):** Runs load simulations, evaluates capacity headroom, tests failure injections, and generates scale sign-off certificates.

- **API Endpoints:**
  - `POST /reliability/load-test`: Execute load test simulations with optional failure injection.
  - `POST /reliability/signoff`: Generate formal scale reliability sign-off certificate.

### Phase 3 Task 6 — Growth Instrumentation & North-Star Metrics

Task 6 delivers position-level impression logging and outcome event attribution.

- **Growth Engine (`matching/growth_instrumentation.py`):** Logs candidate rankings with position indices and links conversion events.

- **API Endpoints:**
  - `POST /growth/log-impression`: Record ranked candidate list impression and model version.
  - `POST /growth/log-outcome`: Attribute user actions (click, apply, shortlist) to an impression ID.
  - `GET /growth/reconstruct/{impression_id}`: Reconstruct ranking position and outcome history.

### Phase 3 Task 7 — Activation & Onboarding Funnel Optimization

Task 7 optimizes candidate activation for brand-new users with zero interaction history.

- **Cold-Start Recommendation Engine (`matching/cold_start_recommendation.py`):** Serves personalized first-session job matches using onboarding profile signals with guaranteed non-empty fallbacks.

- **API Endpoints:**
  - `POST /growth/cold-start-recommend`: Get tailored first-session job recommendations for new users.
  - `GET /growth/cold-start-lift`: Retrieve measured conversion lift metrics.

### Phase 3 Task 8 — Retention, Cohorts & Churn Prediction

Task 8 builds churn prediction models to identify disengaging candidates and employers before churn occurs.

- **Churn Prediction Engine (`matching/churn_prediction.py`):** Trains 14-day churn classifiers and calculates Precision-Recall lift metrics.

- **API Endpoints:**
  - `POST /growth/churn-eval`: Evaluate churn classifier performance and PR AUC lift.
  - `POST /growth/at-risk-list`: Retrieve prioritized list of at-risk users with churn risk drivers.

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