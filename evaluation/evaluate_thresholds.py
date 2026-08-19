import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from matching.threshold_validation import validate_skill_thresholds

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    students = load_json("data/evaluation_students.json")
    jobs = load_json("data/evaluation_jobs.json")
    labels = load_json("data/evaluation_labels.json")

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

    results = []

    for label in labels:
        student_id = label["student_id"]
        job_id = label["job_id"]
        expected = label["expected_match"]

        student = students_by_id[student_id]
        job = jobs_by_id[job_id]

        validation = validate_skill_thresholds(student, job)

        predicted = (
            1
            if validation["threshold_validation"] == "PASS"
            else 0
        )

        if expected == 1 and predicted == 1:
            true_positive += 1
        elif expected == 0 and predicted == 0:
            true_negative += 1
        elif expected == 0 and predicted == 1:
            false_positive += 1
        elif expected == 1 and predicted == 0:
            false_negative += 1

        results.append({
            "student_id": student_id,
            "job_id": job_id,
            "expected": expected,
            "predicted": predicted
        })

    total = len(results)

    accuracy = (
        (true_positive + true_negative) / total
        if total
        else 0
    )

    precision = (
        true_positive / (true_positive + false_positive)
        if (true_positive + false_positive)
        else 0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if (true_positive + false_negative)
        else 0
    )

    false_positive_rate = (
        false_positive / (false_positive + true_negative)
        if (false_positive + true_negative)
        else 0
    )

    print("Threshold Validation Evaluation")
    print("=" * 40)

    print(f"Total pairs: {total}")
    print(f"True positives: {true_positive}")
    print(f"True negatives: {true_negative}")
    print(f"False positives: {false_positive}")
    print(f"False negatives: {false_negative}")

    print()
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"False-positive rate: {false_positive_rate:.4f}")

    print()
    print("Per-pair results")
    print("=" * 40)

    for result in results:
        print(
            f"{result['student_id']} + "
            f"{result['job_id']} | "
            f"Expected={result['expected']} | "
            f"Predicted={result['predicted']}"
        )


if __name__ == "__main__":
    main()