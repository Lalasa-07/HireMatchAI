def calculate_match_score(jd_skills, resume_skills):
    jd_skills_set = set(skill.lower() for skill in jd_skills)
    resume_skills_set = set(skill.lower() for skill in resume_skills)

    matched_skills = jd_skills_set.intersection(resume_skills_set)
    missing_skills = jd_skills_set - resume_skills_set

    if len(jd_skills_set) == 0:
        score = 0
    else:
        score = (len(matched_skills) / len(jd_skills_set)) * 100

    return {
        "score": round(score, 2),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }