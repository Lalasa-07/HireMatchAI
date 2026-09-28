COURSE_LINKS = {
    "Python": {
        "Coursera": "https://www.coursera.org/search?query=python",
        "Udemy": "https://www.udemy.com/courses/search/?q=python"
    },
    "SQL": {
        "Coursera": "https://www.coursera.org/search?query=sql",
        "Udemy": "https://www.udemy.com/courses/search/?q=sql"
    },
    "AWS": {
        "Coursera": "https://www.coursera.org/search?query=aws",
        "Udemy": "https://www.udemy.com/courses/search/?q=aws"
    },
    "Docker": {
        "Coursera": "https://www.coursera.org/search?query=docker",
        "Udemy": "https://www.udemy.com/courses/search/?q=docker"
    },
    "Kubernetes": {
        "Coursera": "https://www.coursera.org/search?query=kubernetes",
        "Udemy": "https://www.udemy.com/courses/search/?q=kubernetes"
    },
    "JavaScript": {
        "Coursera": "https://www.coursera.org/search?query=javascript",
        "Udemy": "https://www.udemy.com/courses/search/?q=javascript"
    },
    "React": {
        "Coursera": "https://www.coursera.org/search?query=react",
        "Udemy": "https://www.udemy.com/courses/search/?q=react"
    },
    "Machine Learning": {
        "Coursera": "https://www.coursera.org/search?query=machine%20learning",
        "Udemy": "https://www.udemy.com/courses/search/?q=machine%20learning"
    },
    "Tableau": {
        "Coursera": "https://www.coursera.org/search?query=tableau",
        "Udemy": "https://www.udemy.com/courses/search/?q=tableau"
    },
    "Power BI": {
        "Coursera": "https://www.coursera.org/search?query=power%20bi",
        "Udemy": "https://www.udemy.com/courses/search/?q=power%20bi"
    },
    "Excel": {
        "Coursera": "https://www.coursera.org/search?query=excel",
        "Udemy": "https://www.udemy.com/courses/search/?q=excel"
    },
    "PySpark": {
        "Coursera": "https://www.coursera.org/search?query=pyspark",
        "Udemy": "https://www.udemy.com/courses/search/?q=pyspark"
    },
    "Databricks": {
        "Coursera": "https://www.coursera.org/search?query=databricks",
        "Udemy": "https://www.udemy.com/courses/search/?q=databricks"
    },
    "Kafka": {
        "Coursera": "https://www.coursera.org/search?query=apache%20kafka",
        "Udemy": "https://www.udemy.com/courses/search/?q=apache%20kafka"
    },

    "Git": {
        "Coursera": "https://www.coursera.org/search?query=git",
        "Udemy": "https://www.udemy.com/courses/search/?q=git"
    },

    "Java": {
        "Coursera": "https://www.coursera.org/search?query=java",
        "Udemy": "https://www.udemy.com/courses/search/?q=java"
    },

    "Pandas": {
        "Coursera": "https://www.coursera.org/search?query=pandas",
        "Udemy": "https://www.udemy.com/courses/search/?q=pandas"
    },

    "NumPy": {
        "Coursera": "https://www.coursera.org/search?query=numpy",
        "Udemy": "https://www.udemy.com/courses/search/?q=numpy"
    },

    "Artificial Intelligence": {
        "Coursera": "https://www.coursera.org/search?query=artificial%20intelligence",
        "Udemy": "https://www.udemy.com/courses/search/?q=artificial%20intelligence"
    },

    "Deep Learning": {
        "Coursera": "https://www.coursera.org/search?query=deep%20learning",
        "Udemy": "https://www.udemy.com/courses/search/?q=deep%20learning"
    },

    "Django": {
        "Coursera": "https://www.coursera.org/search?query=django",
        "Udemy": "https://www.udemy.com/courses/search/?q=django"
    },

    "Flask": {
        "Coursera": "https://www.coursera.org/search?query=flask",
        "Udemy": "https://www.udemy.com/courses/search/?q=flask"
    }
}



def recommend_courses(missing_skills):
    recommendations = {}

    skill_lookup = {
        skill.lower(): skill
        for skill in COURSE_LINKS
    }

    for skill in missing_skills:
        skill_clean = skill.strip().lower()

        original_skill = skill_lookup.get(skill_clean)

        if original_skill:
            recommendations[original_skill] = COURSE_LINKS[original_skill]

    return recommendations