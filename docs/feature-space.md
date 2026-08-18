# Student ↔ Job Feature Space

## 1. Objective

The purpose of the feature space is to represent student profiles and job requirements in a common structure so that verified student scores can be used to generate relevant job matches.

## 2. Student Features

| Feature | Description | Data Type |
|---|---|---|
| student_id | Unique student identifier | String |
| skills | Skills possessed by student | Array |
| verified_skill_scores | Verified proficiency score for each skill | Object |
| experience_years | Total relevant experience | Float |
| education | Degree and branch | Object |
| certifications | Relevant certifications | Array |
| preferred_roles | Roles preferred by student | Array |
| location | Student location | String |
| work_mode | Preferred work arrangement | Array |
| experience_level | Fresher/Junior/Mid/Senior | String |
| availability | Joining availability | String |
| salary_expectation | Expected salary | Number |
| projects | Relevant projects | Array |

## 3. Job Features

| Feature | Description | Data Type |
|---|---|---|
| job_id | Unique job identifier | String |
| job_title | Job title | String |
| required_skills | Mandatory skills | Array |
| preferred_skills | Preferred skills | Array |
| required_skill_scores | Minimum expected proficiency | Object |
| experience_required | Required experience | Float |
| education_required | Required education | Object |
| certifications | Preferred certifications | Array |
| location | Job location | String |
| work_mode | Remote/Hybrid/On-site | Array |
| experience_level | Required experience level | String |
| joining_requirement | Joining requirement | String |
| salary_range | Job salary range | Object |
| domain | Job/business domain | String |

## 4. Matching Dimensions

The matching system compares:

1. Skill overlap
2. Verified skill proficiency
3. Experience
4. Job role
5. Location
6. Work mode
7. Education
8. Availability
9. Salary compatibility
10. Project/domain relevance

## 5. Verified Scores

Verified skill scores are important because the system should consider not only whether a student has a skill but also the student's verified proficiency in that skill.

Example:

Student:

- Python: 85
- React: 72
- MongoDB: 65

Job:

- Python: 70 minimum
- React: 60 minimum
- MongoDB: 50 minimum

The student's verified proficiency exceeds the minimum requirements for all three skills.

## 6. Matching Score

Initial weighted scoring:

- Skill Match: 35%
- Proficiency Match: 20%
- Experience Match: 10%
- Role Match: 10%
- Location/Work Mode Match: 10%
- Education Match: 5%
- Availability Match: 5%
- Salary Match: 5%

Total:

100%

## 7. Output

The matching system returns:

- Overall match score
- Match breakdown
- Matched skills
- Missing skills
- Ranked jobs