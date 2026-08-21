import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from search.candidate_ranking import rank_candidates_for_job
from search.job_ranking import rank_jobs_for_student


DATA_DIR = PROJECT_ROOT / "data"


def load_json(filename):
    with (DATA_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


def calculate_metrics(predictions):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    complete_explanations = 0

    for expected, result in predictions:
        explanation = result["explanation"]

        predicted = (
            1
            if explanation["decision"] == "SHORTLISTED"
            else 0
        )

        if expected == 1 and predicted == 1:
            true_positive += 1
        elif expected == 0 and predicted == 0:
            true_negative += 1
        elif expected == 0 and predicted == 1:
            false_positive += 1
        else:
            false_negative += 1

        required_fields = {
            "decision",
            "match_score",
            "threshold_validation",
            "matched_skills",
            "missing_skills",
            "skill_results",
            "score_breakdown",
            "summary",
        }

        if required_fields.issubset(explanation):
            complete_explanations += 1

    total = len(predictions)

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

    return {
        "total": total,
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": precision,
        "recall": recall,
        "false_positive_rate": false_positive_rate,
        "explanation_coverage": (
            complete_explanations / total
            if total
            else 0
        ),
    }


def print_metrics(title, metrics):
    print(title)
    print("=" * len(title))

    print(f"Total labelled pairs: {metrics['total']}")
    print(f"True positives: {metrics['true_positive']}")
    print(f"True negatives: {metrics['true_negative']}")
    print(f"False positives: {metrics['false_positive']}")
    print(f"False negatives: {metrics['false_negative']}")
    print()
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(
        "False-positive rate: "
        f"{metrics['false_positive_rate']:.4f}"
    )
    print(
        "Explanation payload coverage: "
        f"{metrics['explanation_coverage']:.4f}"
    )
    print()


def main():
    students = load_json("evaluation_students.json")
    jobs = load_json("evaluation_jobs.json")
    labels = load_json("evaluation_labels.json")

    labels_by_pair = {
        (label["student_id"], label["job_id"]): label["expected_match"]
        for label in labels
    }

    job_ranking_predictions = []

    for student in students:
        ranked_jobs = rank_jobs_for_student(
            student["student_id"],
            top_k=len(jobs),
        )

        for result in ranked_jobs:
            expected = labels_by_pair[
                (student["student_id"], result["job_id"])
            ]
            job_ranking_predictions.append((expected, result))

    candidate_ranking_predictions = []

    for job in jobs:
        ranked_candidates = rank_candidates_for_job(
            job["job_id"],
            top_k=len(students),
        )

        for result in ranked_candidates:
            expected = labels_by_pair[
                (result["student_id"], job["job_id"])
            ]
            candidate_ranking_predictions.append((expected, result))

    print_metrics(
        "Job Ranking for Students (Held-Out Data)",
        calculate_metrics(job_ranking_predictions),
    )

    print_metrics(
        "Candidate Ranking for Companies (Held-Out Data)",
        calculate_metrics(candidate_ranking_predictions),
    )


if __name__ == "__main__":
    main()