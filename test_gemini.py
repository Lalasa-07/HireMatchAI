from analyzer.gemini_analyzer import analyze_jd_and_resume


jd = """
We are looking for a Python Developer.

Required skills:
Python, SQL, Git

Preferred skills:
AWS, Docker

The candidate should have good problem-solving
and communication skills.
"""


resume = """
Lalasa

Skills:
Python
SQL
Git
Java

Education:
B.Tech Computer Science

Projects:
Built a Python-based resume analyzer.
Developed a SQL data analysis project.

Email: lalasa@example.com
Phone: 9876543210
"""


result = analyze_jd_and_resume(jd, resume)


print("\n========== HIREMATCH AI TEST ==========\n")

print("JD SKILLS:")
for skill in result["jd_skills"]:
    print(
        f"- {skill['name']} | "
        f"{skill['requirement']} | "
        f"{skill['priority']}"
    )

print("\nRESUME SKILLS:")
print(", ".join(result["resume_skills"]))

print("\nMATCHED SKILLS:")
print(", ".join(result["matched_skills"]))

print("\nMISSING SKILLS:")
print(", ".join(result["missing_skills"]))

print("\nWHY THIS MATCH:")
for reason in result["score_reasons"]:
    print("-", reason)

print("\nRESUME IMPROVEMENTS:")
for suggestion in result["resume_improvements"]:
    print("-", suggestion)

print("\nATS CHECK:")
for item, value in result["ats"].items():
    print(f"- {item}: {value}")