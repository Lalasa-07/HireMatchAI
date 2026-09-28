def generate_suggestions(missing_skills, ats_result):
    suggestions = []

    # Suggestions based on missing skills
    if missing_skills:
        suggestions.append(
            "Add relevant missing skills to your resume if you genuinely have "
            "experience with them."
        )

        for skill in missing_skills:
            suggestions.append(
                f"Consider adding {skill} through a project, certification, "
                "or practical experience."
            )

    # Suggestions based on ATS checks
    checks = ats_result.get("checks", {})

    if not checks.get("has_email"):
        suggestions.append("Add a professional email address.")

    if not checks.get("has_phone"):
        suggestions.append("Add a professional phone number.")

    if not checks.get("has_education"):
        suggestions.append("Add a clear Education section.")

    if not checks.get("has_experience"):
        suggestions.append(
            "Add relevant internship, work experience, or practical experience."
        )

    if not checks.get("has_skills_section"):
        suggestions.append("Create a clearly labelled Skills section.")

    if not checks.get("has_projects"):
        suggestions.append(
            "Add relevant projects with technologies and measurable outcomes."
        )

    return suggestions