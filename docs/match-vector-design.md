# PlaceMux Match Vector Design

## 1. Objective

The objective of the match vector is to represent the relationship between a student profile and a job requirement using measurable features.

The match vector will use the agreed student-job feature space and verified student skill scores.

The system should produce an explainable matching result that can be used to rank jobs for a student.

---

## 2. Input Data

### Student

The student profile contains:

- student_id
- skills
- verified_skill_scores
- experience_years
- education
- certifications
- preferred_roles
- location
- work_mode
- experience_level
- availability
- salary_expectation
- projects

### Job

The job profile contains:

- job_id
- job_title
- required_skills
- preferred_skills
- required_skill_scores
- experience_required
- education_required
- certifications
- location
- work_mode
- experience_level
- joining_requirement
- salary_range
- domain

---

## 3. Match Vector Dimensions

For each student-job pair, the system will calculate the following matching dimensions:

1. Skill Match
2. Proficiency Match
3. Experience Match
4. Role Match
5. Location/Work Mode Match
6. Education Match
7. Availability Match
8. Salary Match

Project/domain relevance will be retained as an additional feature for future improvement and analysis.

---

## 4. Skill Match

Skill Match measures the overlap between the job's required skills and the student's skills.

Formula:

Skill Match = 
(number of matched required skills / number of required skills) * 100

A required skill is considered matched when the student has that skill.

---

## 5. Proficiency Match

Proficiency Match compares the student's verified skill score with the job's required minimum skill score.

For each required skill:

Student verified score >= Job required score

means the student satisfies the proficiency requirement for that skill.

The proficiency result will be calculated using the student's verified scores and the job's required skill thresholds.

---

## 6. Experience Match

Experience Match compares:

- student experience_years
- job experience_required

If the student's experience meets or exceeds the required experience, the experience requirement is satisfied.

---

## 7. Role Match

Role Match compares the student's preferred roles with the job title/role.

A stronger role match is obtained when the job role is present in the student's preferred roles.

---

## 8. Location and Work Mode Match

Location and work mode are compared between the student and job.

A match is obtained when:

- the locations are compatible, or
- the student's preferred work mode is supported by the job.

---

## 9. Education Match

Education Match compares the student's education with the job's education requirement.

The degree and branch are checked against the job requirement.

---

## 10. Availability Match

Availability Match compares:

- student's availability
- job joining requirement

A match is obtained when the student's availability satisfies the job's joining requirement.

---

## 11. Salary Match

Salary Match compares:

- student's salary expectation
- job salary range

A salary requirement is satisfied when the student's expectation falls within the job's salary range.

---

## 12. Weighted Matching Score

The initial weighted score follows the agreed API contract:

| Dimension | Weight |
|---|---:|
| Skill Match | 35% |
| Proficiency Match | 20% |
| Experience Match | 10% |
| Role Match | 10% |
| Location/Work Mode Match | 10% |
| Education Match | 5% |
| Availability Match | 5% |
| Salary Match | 5% |
| **Total** | **100%** |

Overall Match Score:

Score =
0.35 * Skill Match
+ 0.20 * Proficiency Match
+ 0.10 * Experience Match
+ 0.10 * Role Match
+ 0.10 * Location/Work Mode Match
+ 0.05 * Education Match
+ 0.05 * Availability Match
+ 0.05 * Salary Match

---

## 13. Baseline

The initial baseline will be a simple required-skill overlap method.

For each student-job pair:

Baseline Score =
(number of matched required skills / number of required skills) * 100

The baseline does not use a machine-learning model.

It provides a simple reference point against which the later match-vector implementation can be evaluated.

---

## 14. Explainability

Every matching result must provide a plain-English explanation.

The explanation should identify:

- matched required skills
- missing required skills
- verified student skill scores
- required job skill thresholds
- important matching dimensions
- overall match score

Example:

The student matches the required Python and MongoDB skills. The verified Python score of 85 exceeds the required threshold of 70, and the MongoDB score of 65 exceeds the required threshold of 50. The student is therefore eligible on the required skill thresholds.

---

## 15. Example Using Current Sample Data

Student:

STU_1001

Verified skills:

- Python: 85
- React: 72
- MongoDB: 65

Job:

JOB_2045

Required skills:

- Python: 70 minimum
- MongoDB: 50 minimum

Preferred skill:

- React

The student satisfies both required skill thresholds:

Python:
85 >= 70

MongoDB:
65 >= 50

Therefore:

Matched required skills:
- Python
- MongoDB

Missing required skills:
- None

The student also has the preferred React skill.

This example is for functional verification only. It is not considered held-out evaluation data.

---

## 16. Evaluation Metrics

The matching implementation will be evaluated using:

- Precision
- Recall
- False-positive rate

Accuracy may also be reported where appropriate, but it will not be used as the only evaluation metric.

Evaluation must use held-out real-shaped sample data rather than only the data used for tuning.

---

## 17. Experiment Tracking

Each experiment will record:

- experiment name
- date
- dataset/version
- baseline or implementation version
- parameters
- precision
- recall
- false-positive rate
- observations

A simple experiment log will be used initially.

---

## 18. Current Data Limitation

The current sample dataset contains one student and one job.

This is sufficient for initial functional verification but is not sufficient for meaningful held-out evaluation.

Additional agreed real-shaped sample student/job records will therefore be required before final evaluation.

The system will not claim production-level accuracy from the current single-example dataset.