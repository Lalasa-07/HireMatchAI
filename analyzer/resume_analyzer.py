from .skill_extractor import extract_skills


def analyze_resume(resume_text):
    skills = extract_skills(resume_text)

    return {
        "skills": skills,
        "total_skills": len(skills)
    }