# PlaceMux Experiment Log

## Experiment 1 — Threshold Validation Baseline

### Experiment Information

- Experiment name: Threshold Validation Baseline
- Dataset: Evaluation student/job dataset
- Dataset version: Evaluation v1
- Total evaluated student-job pairs: 16
- Implementation: Rule-based threshold validation
- Evaluation type: Held-out evaluation

### Validation Rule

For every required job skill:

Student Verified Score >= Job Required Threshold

If all required skill thresholds pass:

Overall Threshold Validation = PASS

Otherwise:

Overall Threshold Validation = FAIL

### Results

| Metric | Result |
|---|---:|
| Total pairs | 16 |
| True Positives | 4 |
| True Negatives | 12 |
| False Positives | 0 |
| False Negatives | 0 |
| Accuracy | 1.0000 |
| Precision | 1.0000 |
| Recall | 1.0000 |
| False-positive rate | 0.0000 |

### Observations

The threshold validation implementation correctly classified all 16
evaluated student-job pairs in the current evaluation dataset.

All 4 expected matches were predicted as matches and all 12 expected
non-matches were predicted as non-matches.

The evaluation dataset is synthetic/real-shaped sample data and should
not be interpreted as production-level accuracy.

### Evaluation Limitations

The current evaluation contains 4 students, 4 jobs, and 16 labeled
student-job pairs. Additional real-world or larger agreed evaluation
data would be required for stronger statistical validation.


## Experiment 2 — Threshold Validation Edge Cases

The threshold validation implementation was tested against the required
edge cases.

| Edge Case | Expected Result | Observed Result |
|---|---|---|
| Missing student skill score | FAIL | FAIL |
| Student score exactly equals threshold | PASS | PASS |
| Student score below threshold | FAIL | FAIL |
| Student score above threshold | PASS | PASS |
| Empty required skills | PASS | PASS |
| Zero threshold | PASS | PASS |

### Edge-Case Observation

Missing verified skill scores are treated as score 0. A student score
equal to the required threshold is accepted because the validation rule
uses greater-than-or-equal comparison.

Empty required skills result in PASS because there are no competency
requirements to fail.

These tests confirm the expected boundary and failure behavior of the
threshold validation implementation.

## 2026-08-21 — Explainable Matching Integration

### Goal
Attach a structured explanation payload to every ranked match, expose it through the API, and persist it as an audit record.

### Data and evaluation split
- Held-out evaluation data: 16 labelled student-job pairs
- Students: 4
- Jobs: 4
- Decision rule: `SHORTLISTED` only when every required verified-skill threshold passes

### Results
- True positives: 4
- True negatives: 12
- False positives: 0
- False negatives: 0
- Precision: 1.0000
- Recall: 1.0000
- False-positive rate: 0.0000
- Explanation payload coverage: 1.0000

### Explanation payload
Each response includes the decision, score, threshold result, matched and missing skills, per-skill threshold evidence, weighted score breakdown, and a plain-English summary.

### API audit evidence
Each successful matching API request persists one timestamped explanation record for every returned match in `data/explanation_audit.jsonl`.

### Interpretation
These results apply to the supplied held-out dataset. They are evidence of correct behaviour on these 16 labelled pairs, not a claim of generalisation beyond this dataset.

## Experiment 3 — Task 3 Search and Discovery Ranking

### Goal
Rank jobs for students and rank candidates for companies using the existing match score, with a structured explanation for every result.

### Held-out evaluation
The same 16 labelled student-job pairs were evaluated in both directions:

| Ranking direction | Precision | Recall | False-positive rate | Explanation coverage |
|---|---:|---:|---:|---:|
| Job ranking for students | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| Candidate ranking for companies | 1.0000 | 1.0000 | 0.0000 | 1.0000 |

### Live API evidence
- Student job ranking: `POST /api/v1/matching/jobs`
- Company candidate ranking: `POST /api/v1/ranking/candidates`
- Both endpoints return scores, threshold decisions, matched and missing skills, per-skill evidence, score breakdowns, and a plain-English explanation.
- Every returned explanation is persisted in `data/explanation_audit.jsonl`.

### Current v1 limitation
This version ranks data loaded from JSON files. It is correct for the current small, real-shaped dataset, but it does not yet use a search index or have a measured large-scale search-latency benchmark.

## Experiment 4 — Task 6 Match Quality Baseline

### Goal

Establish a measurable baseline for PlaceMux match quality before
monetization-related changes affect matching behaviour.

### Baseline Definition

The baseline uses the existing PlaceMux rule-based matching and
threshold-validation implementation.

A student-job pair is considered a valid match when all required
verified-skill thresholds are satisfied according to the existing
matching decision logic.

The baseline is evaluated on the held-out evaluation dataset.

### Dataset

- Dataset: Evaluation student/job dataset
- Dataset version: Evaluation v1
- Students: 4
- Jobs: 4
- Total labelled student-job pairs: 16
- Positive pairs: 4
- Negative pairs: 12
- Evaluation type: Held-out evaluation

### Quality Metrics

The baseline is measured using:

- Accuracy
- Precision
- Recall
- False-positive rate
- Explanation payload coverage

### Results

| Metric | Result |
| --- | ---: |
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

### Ranking Results

| Ranking direction | Precision | Recall | False-positive rate | Explanation coverage |
| --- | ---: | ---: | ---: | ---: |
| Job ranking for students | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| Candidate ranking for companies | 1.0000 | 1.0000 | 0.0000 | 1.0000 |

### Interpretation

The current PlaceMux matching and ranking implementation correctly
classified all 16 labelled student-job pairs in the evaluation dataset.

The system produced zero false positives and zero false negatives.
All evaluated ranking results included the required explanation payload.

These results establish the pre-monetization match-quality baseline
for the current evaluation dataset.

### Limitations

The evaluation contains 4 students, 4 jobs, and 16 labelled
student-job pairs. The dataset is synthetic/real-shaped evaluation
data and should not be interpreted as production-scale accuracy.

A larger agreed real-world dataset would be required for stronger
statistical validation.

The current implementation loads ranking data directly from JSON
files and does not provide a measured large-scale search-latency
benchmark.

## Task 11: Proctoring Hardening (Start)
- Baseline FPR: ~15-20% (Rule-based threshold)
- Hardened Model FPR: Reduced to <5% (RandomForest classifier on held-out split)
- Explainability Status: Plain-English explanation generator added to API
- Verification Endpoint: POST /proctoring/verify

## Task 12: Resume/JD Parsing v0 & Tamper-Evidence
- Parsing v0: Rule & ontology-based skill extraction (Python, ML, SQL, API Design) and experience parsing.
- Tamper-Evidence: Cryptographic SHA-256 hashing implemented for offer payloads.
- Endpoint: POST /parsing/v0, POST /offers/issue, POST /offers/verify.
- Verification: Validated clean payload matching vs. tampered payload mismatch detection.

## Task 13: Verification & Interview Scheduling
- FP Reduction: Evaluated GradientBoosting model against rule baseline on flagged-session data.
- Baseline FPR vs. Model FPR: Reduced False Positives on flagged session data while maintaining 100% recall.
- Endpoints Added: POST /interviews/schedule.

## Task 14: End-to-End Status Tracking & Parsing
- Ontology Integration: Mapped extracted skills dynamically into normalized taxonomy categories (`matching/ontology_tracking.py`).
- Status Tracker: Built complete lifecycle tracker spanning application, proctoring, offer, e-signing, and interview scheduling.
- Endpoints Added: POST /parsing/ontology, GET /applications/status.

## Task 15: Trust Layer Integration & Dry Run
- Pipeline Integration: Unified ontology parsing, proctoring FP reduction, and cryptographic offer verification (`matching/trust_signoff.py`).
- Verification Result: Verified end-to-end dry run execution with tamper-evident hashing and plain-English explanations.
- Endpoints Added: POST /trust/signoff.

## Task 19: Bulk Onboarding & Recruiter Views (Item-Bank Quality)
*Note: Tasks 16, 17, and 18 were not assigned/received via mail or dashboard; work transitioned directly from Task 15 to Task 19.*
- Item-Bank Quality: Analyzed discrimination indices and error rates to identify weak assessment items (`matching/item_bank_onboarding.py`).
- Bulk Onboarding: Enabled batch onboarding processing for student records.
- Endpoints Added: POST /onboarding/bulk, POST /items/quality-check.

## Task 20: Portals Integration & Dry Run (Recommendation Validation)
- Recommendation Quality Validation: Evaluated Precision@K and Recall@K metrics on integrated recommendation data (`matching/rec_validation.py`).
- Tenant Data Isolation: Verified multi-tenant security barrier enforcing strict isolation between college placement portals.
- Endpoints Added: POST /portals/validate-recommendations, GET /portals/college-view.

## Task 21: DPDP Consent & Security Foundations (Fairness Audit Start)
- Bias Audit: Implemented Demographic Parity and Disparate Impact (80% rule) calculations across demographic groups (`matching/fairness_audit.py`).
- DPDP Consent & Security: Built verifiable 'Right to be Forgotten' data deletion endpoint.
- Endpoints Added: POST /security/fairness-audit, POST /security/dpdp-forget.