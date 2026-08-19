# PlaceMux Threshold Validation Design

## 1. Objective

The objective of threshold validation is to determine whether a student's verified competency score satisfies the minimum competency threshold defined by a job.

For every required job skill, the student's verified skill score will be compared with the job's required skill score.

---

## 2. Validation Rule

For each required skill:

Student Verified Score >= Job Required Threshold

If the condition is true:

PASS

Otherwise:

FAIL

---

## 3. Inputs

### Student

The validation uses:

- student_id
- verified_skill_scores

### Job

The validation uses:

- job_id
- required_skills
- required_skill_scores

---

## 4. Per-Skill Validation

For every required skill, the system will record:

- skill name
- student verified score
- required threshold
- pass/fail result
- plain-English reason

Example:

Python:
Student score = 85
Required threshold = 70
Result = PASS

Reason:
"Python score 85 meets the required threshold of 70."

---

## 5. Missing Skill Handling

If a required skill is not present in the student's verified skill scores, the student's score will be treated as 0 for threshold validation.

The result will therefore be FAIL when the required threshold is greater than zero.

---

## 6. Overall Validation

A student satisfies the job's required competency thresholds only when all required skill thresholds pass.

Example:

Python: 85 >= 70 -> PASS
MongoDB: 65 >= 50 -> PASS

Overall threshold validation:

PASS

---

## 7. Failure Example

If:

Python: 85 >= 70 -> PASS
MongoDB: 40 >= 50 -> FAIL

Overall threshold validation:

FAIL

Reason:

"MongoDB score 40 is below the required threshold of 50."

---

## 8. Explainability

The validation output must provide:

- student ID
- job ID
- overall validation result
- per-skill validation
- student score
- required threshold
- plain-English reason

---

## 9. Edge Cases

The implementation will handle:

1. Missing student skill score
2. Missing required threshold
3. Empty required skills
4. Zero threshold
5. Student score exactly equal to threshold
6. Student score below threshold
7. Student score above threshold

---

## 10. Evaluation

Threshold validation will be evaluated using held-out real-shaped sample data.

The evaluation will measure the correctness of pass/fail threshold decisions.

Where applicable, precision, recall and false-positive rate will be reported.

The current single student/job example is used only for functional verification and is not sufficient for final held-out evaluation.

---

## 11. Explainable Example

Student:

STU_1001

Job:

JOB_2045

Python:
Student verified score = 85
Required threshold = 70
Result = PASS

MongoDB:
Student verified score = 65
Required threshold = 50
Result = PASS

Overall:

Threshold validation PASSED.

Reason:

"The student's verified Python score of 85 meets the required threshold of 70, and the verified MongoDB score of 65 meets the required threshold of 50."