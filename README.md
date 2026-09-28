# HireMatch AI

HireMatch AI is an AI-powered Telegram chatbot that analyzes job descriptions and resumes to help recruiters and job seekers understand candidate-job compatibility.

## Features

- 📄 Job Description (JD) analysis
- 📑 Multiple resume analysis
- 🎯 Resume-JD match score
- ⭐ JD skill priority detection
- ✅ Matched skills identification
- ❌ Missing skills identification
- 📋 ATS-friendly resume checks
- 💡 Resume improvement suggestions
- 🎓 Course recommendations for missing skills
- 🔗 Coursera and Udemy course search links
- 👔 Recruiter Mode
- 🎯 Job-Seeker Mode
- 🤖 Gemini AI-powered analysis

## Technologies Used

- Python
- Telegram Bot API
- Google Gemini API
- PyMuPDF
- python-dotenv
- Git & GitHub

## Project Architecture

Telegram User  
↓  
Telegram Bot  
↓  
PDF Parser  
↓  
Gemini AI Analysis  
↓  
Skill Matching & ATS Analysis  
↓  
Recruiter / Job-Seeker Results  
↓  
Course Recommendations

## How It Works

### Recruiter Mode

Recruiters can upload one Job Description followed by multiple resumes. HireMatch AI analyzes and compares the candidates based on the skills and priorities identified from the JD.

It provides:

- Priority-based match score
- Candidate ranking based on JD skill priorities
- Matched skills
- Missing skills
- High, Medium, and Low priority skills
- ATS compatibility

### Job-Seeker Mode

Job seekers can upload a Job Description and resume to understand:

- How well the resume matches the JD
- Missing skills
- ATS compatibility
- Resume improvement areas
- Recommended learning resources

## Security

API keys and bot tokens are stored in environment variables and are excluded from GitHub using `.gitignore`.

## Disclaimer

The match score and ATS compatibility are estimates based on detected JD and resume information. They are not scores produced by a commercial ATS system.
