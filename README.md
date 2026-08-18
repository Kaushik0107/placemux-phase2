# PlaceMux Phase 2 - Task 1

## AI/ML Engineer

### Task

Company Onboarding & Marketplace Data Model

## Objective

Design the matching foundation that converts verified student scores and profile information into relevant job matches.

## Completed Work

### 1. Student ↔ Job Feature Space

The student and job feature spaces include:

- Skills
- Verified skill scores
- Experience
- Education
- Certifications
- Preferred roles
- Location
- Work mode
- Experience level
- Availability
- Salary
- Projects
- Job domain

### 2. Matching Logic

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

### 3. API Contract

Endpoint:

POST /api/v1/matching/jobs

The API returns:

- Overall match score
- Match breakdown
- Matched skills
- Missing skills
- Ranked jobs

### 4. Technology

- Python
- FastAPI
- Uvicorn
- JSON
- Pytest

## How to Run

### Step 1: Activate virtual environment

Windows PowerShell:

venv\Scripts\activate

### Step 2: Install dependencies

pip install -r requirements.txt

### Step 3: Start the API

python -m uvicorn api.main:app --reload

### Step 4: Open Swagger

http://127.0.0.1:8000/docs

## Task Completion

- Student-job feature space documented
- Matching methodology defined
- Backend API contract defined
- Matching service implemented
- API endpoint implemented
- API tested using Swagger