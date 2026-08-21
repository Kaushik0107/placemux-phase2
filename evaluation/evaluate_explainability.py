import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from matching.feature_matching import generate_matching_decision


DATA_DIR = PROJECT_ROOT / "data"

REQUIRED_EXPLANATION_FIELDS = {
    "decision",
    "match_score",
    "threshold_validation",
    "matched_skills",
    "missing_skills",
    "skill_results",
    "score_breakdown",
    "summary",
}


def load_json(filename):
    with (DATA_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    students = load_json("evaluation_students.json")
    jobs = load_json("evaluation_jobs.json")
    labels = load_json("evaluation_labels.json")

    students_by_id = {
        student["student_id"]: student
        for student in students
    }

    jobs_by_id = {
        job["job_id"]: job
        for job in jobs
    }

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    complete_explanations = 0

    for label in labels:
        student = students_by_id[label["student_id"]]
        job = jobs_by_id[label["job_id"]]

        decision = generate_matching_decision(student, job)
        explanation = decision["explanation"]

        predicted = (
            1
            if explanation["decision"] == "SHORTLISTED"
            else 0
        )
        expected = label["expected_match"]

        if expected == 1 and predicted == 1:
            true_positive += 1
        elif expected == 0 and predicted == 0:
            true_negative += 1
        elif expected == 0 and predicted == 1:
            false_positive += 1
        elif expected == 1 and predicted == 0:
            false_negative += 1

        if REQUIRED_EXPLANATION_FIELDS.issubset(explanation):
            complete_explanations += 1

    total = len(labels)

    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive
        else 0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative
        else 0
    )

    false_positive_rate = (
        false_positive / (false_positive + true_negative)
        if false_positive + true_negative
        else 0
    )

    explanation_coverage = (
        complete_explanations / total
        if total
        else 0
    )

    print("Explainable Match Evaluation (Held-Out Data)")
    print("=" * 46)
    print(f"Total labelled pairs: {total}")
    print(f"True positives: {true_positive}")
    print(f"True negatives: {true_negative}")
    print(f"False positives: {false_positive}")
    print(f"False negatives: {false_negative}")
    print()
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"False-positive rate: {false_positive_rate:.4f}")
    print(f"Explanation payload coverage: {explanation_coverage:.4f}")
    print(
        "Definition: coverage is the proportion of held-out "
        "pairs with every required explanation field."
    )


if __name__ == "__main__":
    main()