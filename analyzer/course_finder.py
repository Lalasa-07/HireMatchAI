from urllib.parse import quote_plus


def find_courses(skill):
    """
    Dynamically creates course-search links
    for a missing skill.
    """

    skill = skill.strip()

    encoded_skill = quote_plus(skill)

    coursera_link = (
        f"https://www.coursera.org/search?query={encoded_skill}"
    )

    udemy_link = (
        f"https://www.udemy.com/courses/search/?q={encoded_skill}"
    )

    return {
        "skill": skill,
        "Coursera": coursera_link,
        "Udemy": udemy_link
    }


def find_courses_for_skills(missing_skills):
    """
    Generate course links for all missing skills.
    """

    recommendations = []

    for skill in missing_skills:

        course = find_courses(skill)

        recommendations.append(course)

    return recommendations