import csv
import json
from datetime import datetime

from VALIDATION.schema import validate_student
from RULES.eligibility_rules import check_eligibility
from RULES.scoring_rules import compute_score

STUDENT_FILE = "data/students.csv"
INTERNSHIP_FILE = "data/internships.json"


def load_students():
    students = []
    with open(STUDENT_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["skills"] = row["skills"].split(";")
            validate_student(row)
            students.append(row)
    return students


def load_internships():
    with open(INTERNSHIP_FILE) as f:
        return json.load(f)


def main():
    students = load_students()
    internships = load_internships()

    decisions = []
    ranked_results = []

    for internship in internships:
        eligible = []

        for student in students:
            status, reasons = check_eligibility(student, internship)

            decision = {
                "timestamp": datetime.utcnow().isoformat(),
                "internship_id": internship["internship_id"],
                "company": internship["company"],
                "student_id": student["student_id"],
                "status": status,
                "reasons": reasons
            }

            if status == "Eligible":
                score = compute_score(student, internship)
                decision["score"] = score
                eligible.append({**student, "score": score})

            decisions.append(decision)

        eligible.sort(key=lambda x: x["score"], reverse=True)

        for rank, candidate in enumerate(eligible, start=1):
            ranked_results.append({
                "internship_id": internship["internship_id"],
                "company": internship["company"],
                "rank": rank,
                "student_id": candidate["student_id"],
                "name": candidate["name"],
                "score": candidate["score"]
            })

    with open("logs/decisions.json", "w") as f:
        json.dump(decisions, f, indent=2)

    with open("reports/ranked_candidates.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=ranked_results[0].keys()
        )
        writer.writeheader()
        writer.writerows(ranked_results)

    print("✅ Multi-internship screening complete")
    print("📊 Ranked candidates generated")


if __name__ == "__main__":
    main()
