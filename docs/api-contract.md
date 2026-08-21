# PlaceMux Matching and Ranking API Contract

## Purpose

The API provides two explainable discovery flows:

1. Students receive ranked jobs.
2. Companies receive ranked candidates.

Every returned result includes a match score, a threshold-based decision, skill evidence, a score breakdown, and a plain-English explanation. Each returned explanation is persisted in `data/explanation_audit.jsonl`.

## 1. Student Job Ranking

### Endpoint

```text
POST /api/v1/matching/jobs
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `student_id` | string | Yes | Student identifier |
| `top_k` | integer | No | Maximum number of jobs to return; defaults to 10 |
| `dataset` | string | No | `sample` or `evaluation`; defaults to `sample` |

### Example request

```text
POST /api/v1/matching/jobs?student_id=EVAL_STU_004&top_k=1&dataset=evaluation
```

## 2. Company Candidate Ranking

### Endpoint

```text
POST /api/v1/ranking/candidates
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `job_id` | string | Yes | Job identifier |
| `top_k` | integer | No | Maximum number of candidates to return; defaults to 10 |

### Example request

```text
POST /api/v1/ranking/candidates?job_id=EVAL_JOB_004&top_k=2
```

## 3. Explainable Result Fields

Each ranked job or candidate includes:

| Field | Description |
|---|---|
| `match_score` | Weighted score from 0 to 100 |
| `threshold_validation` | `PASS` when every required skill threshold is met; otherwise `FAIL` |
| `matched_skills` | Required skills present in the student profile |
| `missing_skills` | Required skills absent from the student profile |
| `skill_results` | Per-skill verified score, required threshold, PASS/FAIL result, and reason |
| `match_breakdown` | Individual component scores used in the weighted match score |
| `explanation.decision` | `SHORTLISTED` or `NOT_SHORTLISTED` |
| `explanation.summary` | Plain-English reason for the decision |

## 4. Error Responses

| Situation | HTTP status | Response detail |
|---|---:|---|
| Unknown student | 404 | `Student profile not found` |
| Unknown job | 404 | `Job not found` |
| Invalid student-ranking dataset | 422 | `dataset must be either 'sample' or 'evaluation'` |
| Explanation audit cannot be saved | 500 | `Unable to store explanation audit record` |

## 5. Live Demonstration Examples

- Student discovery: `EVAL_STU_004` ranks `EVAL_JOB_004` first with a 97.00% score and `SHORTLISTED` decision.
- Company discovery: `EVAL_JOB_004` ranks `EVAL_STU_004` first with a 97.00% score and `SHORTLISTED` decision.
- Negative threshold case: `EVAL_STU_003` is `NOT_SHORTLISTED` for `EVAL_JOB_001` because Python is below threshold and MongoDB is missing.