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