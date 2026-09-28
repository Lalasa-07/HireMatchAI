import os
import re
import fitz
from config import BOT_TOKEN
from analyzer.pdf_parser import extract_text_from_pdf
from analyzer.skill_extractor import extract_skills
from analyzer.jd_analyzer import analyze_job_description
from analyzer.resume_analyzer import analyze_resume
from analyzer.scoring import calculate_match_score
from analyzer.ats_checker import check_ats_compatibility
from analyzer.suggestions import generate_suggestions
from analyzer.course_finder import find_courses_for_skills
from analyzer.gemini_analyzer import analyze_jd_and_resume

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)





# Skills recognized by our analyzer
SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "mongodb",
    "mysql",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "git",
    "github",
    "rest api",
    "machine learning",
    "deep learning",
    "pandas",
    "numpy",
    "tableau",
    "power bi",
    "excel",
    "spark",
    "pyspark",
    "databricks",
    "kafka",
    "django",
    "flask",
    "fastapi"
]


COURSES = {
    "python": "https://www.coursera.org/search?query=python",
    "sql": "https://www.coursera.org/search?query=sql",
    "java": "https://www.coursera.org/search?query=java",
    "aws": "https://www.coursera.org/search?query=aws",
    "docker": "https://www.coursera.org/search?query=docker",
    "rest api": "https://www.coursera.org/search?query=rest%20api",
    "machine learning": "https://www.coursera.org/search?query=machine%20learning",
    "pandas": "https://www.coursera.org/search?query=pandas",
    "numpy": "https://www.coursera.org/search?query=numpy",
    "tableau": "https://www.coursera.org/search?query=tableau",
    "power bi": "https://www.coursera.org/search?query=power%20bi",
    "excel": "https://www.coursera.org/search?query=excel",
    "spark": "https://www.coursera.org/search?query=apache%20spark",
    "pyspark": "https://www.coursera.org/search?query=pyspark",
    "databricks": "https://www.coursera.org/search?query=databricks",
    "kafka": "https://www.coursera.org/search?query=apache%20kafka",
    "react": "https://www.coursera.org/search?query=react",
    "javascript": "https://www.coursera.org/search?query=javascript",
    "git": "https://www.coursera.org/search?query=git"
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    keyboard = [
        [
            InlineKeyboardButton("👔 Recruiter Mode", callback_data="mode_recruiter"),
            InlineKeyboardButton("🎯 Job-Seeker Mode", callback_data="mode_jobseeker")
        ]
    ]

    await update.message.reply_text(
        "🤖 Welcome to HireMatch AI!\n\n"
        "🎯 Intelligent JD & Resume Analyzer\n\n"
        "Choose how you want to use the analyzer:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def mode_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "mode_recruiter":
        context.user_data["mode"] = "recruiter"
        mode_text = (
            "👔 RECRUITER MODE SELECTED\n\n"
            "You can upload one JD and multiple resumes.\n"
            "Candidates will be compared using JD priority-weighted skills and ATS checks.\n\n"
            "📄 Now upload the Job Description PDF."
        )
    else:
        context.user_data["mode"] = "jobseeker"
        mode_text = (
            "🎯 JOB-SEEKER MODE SELECTED\n\n"
            "Upload your Job Description and resume.\n"
            "You will receive your match score, missing skills, "
            "ATS checks, resume improvements and course links.\n\n"
            "📄 Now upload the Job Description PDF."
        )

    await query.edit_message_text(mode_text)





def legacy_analyze_resume(jd_text, resume_text):

    jd_skills = extract_skills(jd_text)

    resume_skills = extract_skills(resume_text)

    matched = [
        skill for skill in jd_skills
        if skill in resume_skills
    ]

    missing = [
        skill for skill in jd_skills
        if skill not in resume_skills
    ]

    if jd_skills:

        score = round(
            len(matched) / len(jd_skills) * 100
        )

    else:

        score = 0

    return jd_skills, matched, missing, score


def generate_suggestions(missing):

    suggestions = []

    for skill in missing:

        suggestions.append(
            f"📌 Learn and practice {skill.title()}."
        )

    if missing:

        suggestions.append(
            "📌 Add projects demonstrating the missing skills."
        )

    else:

        suggestions.append(
            "🎉 Your resume covers all detected JD skills."
        )

    return suggestions


async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):

    document = update.message.document

    if not document.file_name.lower().endswith(".pdf"):

        await update.message.reply_text(
            "❌ Please upload a PDF file."
        )

        return

    await update.message.reply_text(
        "⏳ Reading PDF..."
    )

    os.makedirs("uploads", exist_ok=True)

    file = await document.get_file()

    file_path = os.path.join(
        "uploads",
        document.file_name
    )

    await file.download_to_drive(file_path)

    text = extract_text_from_pdf(file_path)

    # First PDF is the JD
    if "jd_text" not in context.user_data:

        context.user_data["jd_text"] = text

        # Create empty resume list
        context.user_data["resumes"] = []

        await update.message.reply_text(
            "✅ Job Description received!\n\n"
            f"📄 {document.file_name}\n\n"
            "📥 Now upload MULTIPLE resume PDFs.\n\n"
            "You can send Resume 1, Resume 2, "
            "Resume 3, etc.\n\n"
            "When all resumes are uploaded, send:\n\n"
            "👉 /done"
        )

        return

    # Resume received
    if "resumes" not in context.user_data:

        context.user_data["resumes"] = []

    candidate_number = len(
        context.user_data["resumes"]
    ) + 1

    context.user_data["resumes"].append({
        "name": document.file_name,
        "text": text
    })

    total = len(
        context.user_data["resumes"]
    )

    await update.message.reply_text(
        f"✅ Resume {candidate_number} received!\n\n"
        f"📄 {document.file_name}\n\n"
        f"👥 Total resumes received: {total}\n\n"
        "Upload another resume or send /done "
        "to analyze all resumes."
    )


async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    jd_text = context.user_data.get("jd_text")
    resumes = context.user_data.get("resumes", [])

    if not jd_text:
        await update.message.reply_text(
            "❌ Please upload the Job Description PDF first."
        )
        return

    if not resumes:
        await update.message.reply_text(
            "❌ Please upload at least one resume PDF."
        )
        return

    await update.message.reply_text(
        f"🔎 Analyzing {len(resumes)} resume(s)...\n\n"
        "Please wait..."
    )

    # Analyze Job Description and resumes using Gemini AI

    results = []

    for resume in resumes:

        ai_result = analyze_jd_and_resume(
            jd_text,
            resume["text"]
        )

        # Extract JD skill names
        jd_skills = [
            skill["name"]
            for skill in ai_result["jd_skills"]
        ]

        matched_skills = ai_result["matched_skills"]
        missing_skills = ai_result["missing_skills"]

        # Calculate match score.
        # Recruiter Mode: High=3, Medium=2, Low=1.
        # Job-Seeker Mode: keep the original simple skill-match score.
        if context.user_data.get("mode") == "recruiter":
            priority_weights = {"high": 3, "medium": 2, "low": 1}

            priority_by_skill = {
                skill["name"].strip().lower(): skill.get(
                    "priority", "medium"
                ).strip().lower()
                for skill in ai_result["jd_skills"]
            }

            total_weight = sum(
                priority_weights.get(
                    priority_by_skill.get(skill.strip().lower(), "medium"),
                    2
                )
                for skill in jd_skills
            )

            matched_weight = sum(
                priority_weights.get(
                    priority_by_skill.get(skill.strip().lower(), "medium"),
                    2
                )
                for skill in matched_skills
            )

            score = round(
                matched_weight / total_weight * 100
            ) if total_weight else 0

            high_total = sum(
                1 for skill in jd_skills
                if priority_by_skill.get(
                    skill.strip().lower(), "medium"
                ) == "high"
            )

            high_matched = sum(
                1 for skill in matched_skills
                if priority_by_skill.get(
                    skill.strip().lower(), "medium"
                ) == "high"
            )
        else:
            if jd_skills:
                score = round(
                    len(matched_skills) / len(jd_skills) * 100
                )
            else:
                score = 0

            high_total = 0
            high_matched = 0

        # Calculate ATS compatibility
        ats_checks = ai_result["ats"]

        if ats_checks:
            ats_score = round(
                sum(ats_checks.values())
                / len(ats_checks)
                * 100
            )
        else:
            ats_score = 0

        # Keep existing course recommendation system
        courses = find_courses_for_skills(missing_skills)
            

        results.append({
            "name": resume["name"],
            "score": score,
            "matched": matched_skills,
            "missing": missing_skills,
            "ats_score": ats_score,
            "high_matched": high_matched,
            "high_total": high_total,
            "ats_checks": ats_checks,
            "suggestions": ai_result["resume_improvements"],
            "courses": courses,
            "score_reasons": ai_result["score_reasons"],
            "jd_skills": ai_result["jd_skills"]
        })

    # Recruiter ranking: priority-weighted match score first,
    # ATS compatibility second as a tie-breaker.
    results.sort(
        key=lambda x: (x["score"], x["ats_score"]),
        reverse=True
    )

    # Build report
    mode = context.user_data.get("mode", "recruiter")

    if mode == "jobseeker":
        mode_title = "🎯 JOB-SEEKER MODE"
    else:
        mode_title = "👔 RECRUITER MODE"

    report = (
        "🤖 HIREMATCH AI\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"{mode_title}\n"
        "📄 MULTIPLE RESUME ANALYSIS\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    # Job Description skills and priorities
    if results:
        jd_info = results[0].get("jd_skills", [])
    else:
        jd_info = []

    report += "🎯 JD SKILLS & PRIORITY:\n"

    if jd_info:
        for skill in jd_info:
            report += (
                f"• {skill['name']} — "
                f"{skill['requirement']} — "
                f"{skill['priority']} priority\n"
            )
    else:
        report += "No JD skills detected.\n"

    report += "\n"

    # Candidate reports
    if mode == "recruiter":
        # Recruiter Mode: compare candidates only.
        # No courses or resume-improvement coaching.
        for index, result in enumerate(results, start=1):
            report += (
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 PRIORITY {index} — CANDIDATE\n"
                f"📄 {result['name']}\n\n"
                f"🎯 PRIORITY MATCH SCORE: {result['score']}%\n"
                f"📊 ATS COMPATIBILITY: {result['ats_score']}%\n"
                f"⭐ HIGH-PRIORITY SKILLS: "
                f"{result['high_matched']}/{result['high_total']}\n\n"
            )

            report += "✅ MATCHED SKILLS:\n"
            if result["matched"]:
                for skill in result["matched"]:
                    report += f"• {skill}\n"
            else:
                report += "• No matched skills detected.\n"

            report += "\n❌ MISSING SKILLS:\n"
            if result["missing"]:
                for skill in result["missing"]:
                    report += f"• {skill}\n"
            else:
                report += "• No missing JD skills detected.\n"

            report += "\n📋 ATS CHECK:\n"
            for check_name, passed in result["ats_checks"].items():
                label = (
                    check_name.replace("has_", "")
                    .replace("_", " ")
                    .title()
                )
                icon = "✅" if passed else "❌"
                report += f"{icon} {label}\n"

            report += "\n"

    else:
        # Job-Seeker Mode: keep the existing detailed coaching report.
        for index, result in enumerate(results, start=1):
            report += (
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 CANDIDATE {index}\n"
                f"📄 {result['name']}\n\n"
                f"🎯 MATCH SCORE: {result['score']}%\n"
                f"📊 ATS COMPATIBILITY: {result['ats_score']}%\n\n"
            )

            report += "💡 WHY THIS SCORE?\n"
            if result.get("score_reasons"):
                for reason in result["score_reasons"]:
                    report += f"• {reason}\n"
            else:
                report += "• Score is based on matched JD skills.\n"

            report += "\n✅ MATCHED SKILLS:\n"
            if result["matched"]:
                for skill in result["matched"]:
                    report += f"• {skill}\n"
            else:
                report += "• No matched skills detected.\n"

            report += "\n❌ MISSING SKILLS:\n"
            if result["missing"]:
                for skill in result["missing"]:
                    report += f"• {skill}\n"
            else:
                report += "• No missing JD skills detected.\n"

            report += "\n📋 ATS CHECK:\n"
            for check_name, passed in result["ats_checks"].items():
                label = (
                    check_name.replace("has_", "")
                    .replace("_", " ")
                    .title()
                )
                icon = "✅" if passed else "❌"
                report += f"{icon} {label}\n"

            report += "\n🛠️ RESUME IMPROVEMENTS:\n"
            if result["suggestions"]:
                for suggestion in result["suggestions"]:
                    report += f"• {suggestion}\n"
            else:
                report += "• No additional improvements detected.\n"

            report += "\n"

            if result["courses"]:
                report += "🎓 RECOMMENDED COURSES:\n"
                for course in result["courses"]:
                    report += (
                        f"\n📚 {course['skill']}\n"
                        f"• Coursera: {course['Coursera']}\n"
                        f"• Udemy: {course['Udemy']}\n"
                    )
                report += "\n"

    if mode == "recruiter":
        report += "📌 RECRUITER FINAL RESULT:\n"
        report += "• Candidates are ranked by JD-priority-weighted skill match.\n"
        report += "• High-priority JD skills carry more weight than medium/low-priority skills.\n"
        report += "• ATS compatibility is used as the tie-breaker.\n"
        if results:
            report += f"• {len(results)} candidate(s) compared for the same JD.\n"
        report += "\n"
    else:
        report += "📌 JOB-SEEKER ACTION PLAN:\n"
        if results:
            best = results[0]
            report += f"• Focus first on these missing skills: {', '.join(best['missing'][:5]) or 'None detected'}.\n"
            report += "• Review the ATS checks and resume improvements above.\n"
            report += "• Use the recommended course links to close skill gaps.\n\n"
        else:
            report += "• Upload a resume to receive a personalized action plan.\n\n"

    report += (
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 Analysis completed for "
        f"{len(results)} candidate(s).\n\n"
        "ℹ️ Match scores are based on detected "
        "JD/resume skill matches.\n"
        "ATS score is an estimated compatibility "
        "check, not a score from a commercial ATS."
    )

    # Telegram message-length limit
    for i in range(0, len(report), 4000):
        await update.message.reply_text(
            report[i:i + 4000]
        )


def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("done", done_command)
    )

    app.add_handler(
        CallbackQueryHandler(mode_callback, pattern="^mode_")
    )

    app.add_handler(
        MessageHandler(
            filters.Document.PDF,
            handle_pdf
        )
    )

    print("🤖 HireMatch AI Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()