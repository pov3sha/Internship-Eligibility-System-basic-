def compute_score(student, internship):
    score = 0.0

    # GPA Score (normalized out of 10)
    gpa_score = float(student["gpa"]) / 10
    score += gpa_score * internship["weights"]["gpa"]

    # Skills Score
    student_skills = set(student["skills"])
    required_skills = set(internship["required_skills"])
    skill_match_ratio = len(student_skills & required_skills) / len(required_skills)
    score += skill_match_ratio * internship["weights"]["skills"]

    # Availability Score
    weeks = int(student["availability_weeks"])
    if internship["min_duration_weeks"] <= weeks <= internship["max_duration_weeks"]:
        score += 1.0 * internship["weights"]["availability"]

    return round(score, 3)
