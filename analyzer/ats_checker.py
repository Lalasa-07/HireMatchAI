import re


def check_ats_compatibility(resume_text):
    checks = {
        "has_email": bool(
            re.search(r"[\w\.-]+@[\w\.-]+\.\w+", resume_text)
        ),
        "has_phone": bool(
            re.search(r"\+?\d[\d\s\-\(\)]{8,}", resume_text)
        ),
        "has_education": bool(
            re.search(r"\b(education|degree|b\.?tech|bachelor|master)\b",
                      resume_text, re.IGNORECASE)
        ),
        "has_experience": bool(
            re.search(r"\b(experience|internship|intern)\b",
                      resume_text, re.IGNORECASE)
        ),
        "has_skills_section": bool(
            re.search(r"\b(skills|technical skills|technologies)\b",
                      resume_text, re.IGNORECASE)
        ),
        "has_projects": bool(
            re.search(r"\b(projects|project experience)\b",
                      resume_text, re.IGNORECASE)
        )
    }

    passed_checks = sum(checks.values())
    total_checks = len(checks)

    ats_score = (passed_checks / total_checks) * 100

    return {
        "ats_score": round(ats_score, 2),
        "checks": checks
    }