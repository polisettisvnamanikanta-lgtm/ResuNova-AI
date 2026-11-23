
from utils.llm import generate_response


def improve_resume(resume_text, job_description=""):

    if not resume_text or not resume_text.strip():
        return "Please upload and extract a resume first."

    job_context = ""

    if job_description and job_description.strip():
        job_context = f"""
JOB DESCRIPTION:
{job_description}

Tailor the improved resume to this job description.
Prioritize relevant skills, projects, and experience.
"""


    prompt = f"""
You are an expert professional resume writer,
career consultant, and recruitment specialist.

Your task is to professionally improve the candidate's
existing resume.

ORIGINAL RESUME:
{resume_text}

{job_context}

IMPROVEMENT REQUIREMENTS:

1. PROFESSIONAL SUMMARY
Write a strong and professional summary.

2. TECHNICAL SKILLS
Organize the existing skills into suitable categories.

3. EDUCATION
Improve the presentation of educational qualifications.

4. PROJECTS
Rewrite project descriptions using clear,
professional and achievement-focused language.

5. EXPERIENCE
Improve internship, work experience,
leadership and responsibility descriptions.

6. CERTIFICATIONS
Present existing certifications clearly.

7. ACHIEVEMENTS
Improve the presentation of existing achievements.

8. FORMATTING
Organize the resume using clear headings,
consistent formatting and professional language.

IMPORTANT RULES:

- Never invent skills, projects, internships,
  certifications, achievements or qualifications.
- Never create fake numbers or achievements.
- Do not change the candidate's personal details.
- Preserve all important factual information.
- Correct grammar and spelling.
- Use strong professional action verbs.
- Keep the language clear and concise.
- If information is missing, mark it as
  [Information to be added by candidate].
- Do not claim the candidate has experience
  that is not present in the original resume.

OUTPUT:

Generate the complete improved resume.

After the improved resume, provide a separate section
called "Changes Made" explaining the major improvements.
"""

    result = generate_response(prompt)

    return result
