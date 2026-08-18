# PlaceMux Matching API Contract

## 1. Endpoint

POST /api/v1/matching/jobs

## 2. Purpose

This API returns ranked job matches for a student using the defined student-job feature space.

## 3. Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| student_id | String | Yes | Unique student identifier |
| top_k | Integer | No | Maximum number of jobs to return |

## 4. Example Request

POST /api/v1/matching/jobs?student_id=STU_1001&top_k=10

## 5. Response

The API returns the student ID and a ranked list of matching jobs.

Example response:

{
  "student_id": "STU_1001",
  "matches": [
    {
      "job_id": "JOB_2045",
      "job_title": "Junior Python Developer",
      "company": "ABC Technologies",
      "match_score": 91.4,
      "match_breakdown": {
        "skill_match": 95,
        "proficiency_match": 92,
        "experience_match": 85,
        "role_match": 94,
        "location_match": 100,
        "education_match": 100,
        "availability_match": 100,
        "salary_match": 100
      },
      "matched_skills": [
        "Python",
        "MongoDB"
      ],
      "missing_skills": [
        "Docker"
      ]
    }
  ]
}

## 6. Matching Score

The initial matching score uses the following weights:

- Skill Match: 35%
- Proficiency Match: 20%
- Experience Match: 10%
- Role Match: 10%
- Location/Work Mode Match: 10%
- Education Match: 5%
- Availability Match: 5%
- Salary Match: 5%

Total weight: 100%

## 7. Match Breakdown

The API provides the individual scores used to calculate the overall match score.

This makes the matching result explainable to the Backend and the student.

## 8. Matched Skills

The API identifies skills that are present in both the student profile and job requirements.

## 9. Missing Skills

The API identifies required job skills that are not present in the student profile.

## 10. Error Response

If the student does not exist:

{
  "detail": "Student profile not found"
}

HTTP status code:

404 Not Found

## 11. Backend Integration

The Backend provides the student identifier and matching parameters.

The matching service processes the student and job feature data and returns ranked jobs with:

- Overall match score
- Match breakdown
- Matched skills
- Missing skills