def check_eligibility(student, internship):
    reasons = []

    if float(student["gpa"]) < internship["min_gpa"]:
        reasons.append("GPA below cutoff")

    if not set(internship["required_skills"]).issubset(set(student["skills"])):
        reasons.append("Missing required skills")

    weeks = int(student["availability_weeks"])
    if not (internship["min_duration_weeks"] <= weeks <= internship["max_duration_weeks"]):
        reasons.append("Duration mismatch")

    status = "Eligible" if not reasons else "Rejected"

    return status, reasons
