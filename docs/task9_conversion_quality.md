# Task 9 — Conversion-Quality Check

## Objective

Confirm that the pay-per-application flow has not degraded the relevance
of the existing PlaceMux matching system.

## Baseline

The Task 8 pre-change matching baseline uses the held-out Evaluation v1
dataset.

- Students: 4
- Jobs: 4
- Labelled student-job pairs: 16
- True positives: 4
- True negatives: 12
- False positives: 0
- False negatives: 0

## Baseline Metrics

| Metric | Baseline |
|---|---:|
| Precision | 1.0000 |
| Recall | 1.0000 |
| False-positive rate | 0.0000 |
| Explanation coverage | 1.0000 |

## Task 9 Check

The conversion-quality check will verify that the payment/paywall flow
does not cause relevance regression in the existing matching decisions.

The same held-out evaluation data will be used to compare relevance
before and after the payment-related changes.

## Success Condition

No relevance regression should be detected.

The evaluation must report numerical precision, recall, false-positive
rate, and explanation coverage rather than relying on qualitative claims.

## Post-Change Results

The conversion-quality check was run after the payment/paywall changes
using the same held-out Evaluation v1 dataset.

- Total labelled student-job pairs: 16
- True positives: 4
- True negatives: 12
- False positives: 0
- False negatives: 0

| Metric | Baseline | Post-Change | Regression |
|---|---:|---:|---:|
| Precision | 1.0000 | 1.0000 | None |
| Recall | 1.0000 | 1.0000 | None |
| False-positive rate | 0.0000 | 0.0000 | None |
| Explanation coverage | 1.0000 | 1.0000 | None |

Additional matching results:

- Shortlisted pairs: 4
- Not-shortlisted pairs: 12
- Average match score: 59.0
- Explanation coverage: 1.0000

## Conclusion

No relevance regression was detected after the payment/paywall changes.
The post-change held-out results exactly match the Task 8 baseline.

The payment flow therefore does not change the existing matching
relevance decisions on the supplied Evaluation v1 dataset.

## Task 9 Held-Out Evaluation Results

The conversion-quality check was run against the held-out Evaluation v1
dataset after the payment-related changes.

| Metric | Task 8 Baseline | Task 9 Result | Regression |
|---|---:|---:|---:|
| Precision | 1.0000 | 1.0000 | None |
| Recall | 1.0000 | 1.0000 | None |
| False-positive rate | 0.0000 | 0.0000 | None |
| Explanation coverage | 1.0000 | 1.0000 | None |

### Evaluation Dataset

- Students: 4
- Jobs: 4
- Labelled student-job pairs: 16
- Shortlisted pairs: 4
- Not shortlisted pairs: 12
- Average match score: 59.0
- Explanation coverage: 1.0000

### Conversion-Quality Conclusion

No relevance regression was detected after adding the pay-per-application
flow. The matching decisions, ranking quality, false-positive rate, and
explanation coverage remain unchanged from the Task 8 baseline.

The payment-related changes therefore did not degrade the existing matching
relevance on the supplied held-out Evaluation v1 dataset.

This is a small held-out dataset and should not be interpreted as a
production-scale performance claim.
