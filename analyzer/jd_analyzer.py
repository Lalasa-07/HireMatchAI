from .skill_extractor import extract_skills


def analyze_job_description(jd_text):
    skills = extract_skills(jd_text)

    return {
        "skills": skills,
        "total_skills": len(skills)
    }