import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


client = genai.Client(api_key=API_KEY)


def analyze_jd_and_resume(jd_text, resume_text):

    prompt = f"""
You are an expert recruitment and resume analysis AI.

Analyze the following Job Description and Resume.

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}

Perform the following analysis:

1. Extract important technical and professional skills from the JD.
2. Classify each JD skill as Required or Preferred.
3. Assign each skill a priority: High, Medium, or Low.
4. Extract skills found in the resume.
5. Identify matched skills between the JD and resume.
6. Identify missing skills from the JD.
7. Explain why the resume matches or does not match the JD.
8. Suggest specific improvements to the resume.
9. Check basic ATS compatibility:
   - Email
   - Phone
   - Education
   - Experience
   - Skills section
   - Projects section
10. Do not invent information that is not present in the resume.

Return ONLY valid JSON.
"""


    response_schema = {
        "type": "object",
        "properties": {
            "jd_skills": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "requirement": {"type": "string"},
                        "priority": {"type": "string"}
                    },
                    "required": ["name", "requirement", "priority"]
                }
            },
            "resume_skills": {
                "type": "array",
                "items": {"type": "string"}
            },
            "matched_skills": {
                "type": "array",
                "items": {"type": "string"}
            },
            "missing_skills": {
                "type": "array",
                "items": {"type": "string"}
            },
            "score_reasons": {
                "type": "array",
                "items": {"type": "string"}
            },
            "resume_improvements": {
                "type": "array",
                "items": {"type": "string"}
            },
            "ats": {
                "type": "object",
                "properties": {
                    "email": {"type": "boolean"},
                    "phone": {"type": "boolean"},
                    "education": {"type": "boolean"},
                    "experience": {"type": "boolean"},
                    "skills_section": {"type": "boolean"},
                    "projects": {"type": "boolean"}
                },
                "required": [
                    "email",
                    "phone",
                    "education",
                    "experience",
                    "skills_section",
                    "projects"
                ]
            }
        },
        "required": [
            "jd_skills",
            "resume_skills",
            "matched_skills",
            "missing_skills",
            "score_reasons",
            "resume_improvements",
            "ats"
        ]
    }
    models_to_try = [
        "gemini-3.5-flash-lite",
        "gemini-3.7-flash",
        "gemini-3.8-flash"
        
        
    ]
    response = None

    for model_name in models_to_try:

     

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=response_schema
                    )
                )

                break

            except errors.ServerError as e:

                if attempt < 2:
                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporary error with {model_name}. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    print(
                        f"{model_name} unavailable after retries."
                    )

        if response is not None:
            break

    if response is None:
        raise RuntimeError(
            "Gemini service is temporarily unavailable. "
            "Please try the analysis again."
        )

    return json.loads(response.text)