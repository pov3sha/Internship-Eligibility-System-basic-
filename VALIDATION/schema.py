def validate_student(student):
    required_fields = [
        "student_id", "name", "gpa",
        "skills", "availability_weeks", "start_date"
    ]

    for field in required_fields:
        if field not in student or student[field] in ["", None]:
            raise ValueError(f"Missing or empty field: {field}")

    if not (0 <= float(student["gpa"]) <= 10):
        raise ValueError("Invalid GPA value")

    if int(student["availability_weeks"]) <= 0:
        raise ValueError("Invalid availability weeks")

    return True
