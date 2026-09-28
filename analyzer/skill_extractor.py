import re


SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "MongoDB",
    "MySQL",
    "PostgreSQL",
    "AWS",
    "Azure",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "REST API",
    "Machine Learning",
    "Deep Learning",
    "Pandas",
    "NumPy",
    "Tableau",
    "Power BI",
    "Excel",
    "Spark",
    "PySpark",
    "Databricks",
    "Kafka",
    "Django",
    "Flask",
    "FastAPI",
    "Spring Boot",
    "Linux",
    "Jenkins",
    "Terraform",
    "Oracle",
    "Redis",
    "Postman",
    "TensorFlow",
    "PyTorch",
]


def extract_skills(text):
    """
    Extract technical skills from text.

    Returns:
        list: Skills detected in the given text.
    """

    found_skills = []

    if not text:
        return found_skills

    text_lower = text.lower()

    for skill in SKILLS:

        # Special handling for single-letter C
        if skill == "C":
            c_patterns = [
                r"\bc programming\b",
                r"\bc language\b",
                r"\bc developer\b",
                r"\bc programming language\b",
                r"\bprogramming in c\b",
            ]

            if any(re.search(pattern, text_lower) for pattern in c_patterns):
                found_skills.append(skill)

            continue

        # Normal skills
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills