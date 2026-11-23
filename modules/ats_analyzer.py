
from utils.llm import generate_response


def analyze_resume_against_job(resume_text, job_description):

    prompt = f"""
You are an expert Applicant Tracking System (ATS),
technical recruiter, and professional career advisor.

Your task is to compare the candidate's resume
with the provided job description.

CANDIDATE RESUME:
{resume_text}


JOB DESCRIPTION:
{job_description}


ANALYSIS REQUIREMENTS:

1. OVERALL JOB MATCH
Explain how suitable the candidate is for this position.

2. MATCHING TECHNICAL SKILLS
Identify the technical skills that match the job requirements.

3. MISSING TECHNICAL SKILLS
Identify important skills required by the job
that are missing from the resume.

4. EXPERIENCE MATCH
Evaluate the candidate's relevant experience.

5. EDUCATION MATCH
Compare the candidate's qualifications
with the job requirements.

6. PROJECT RELEVANCE
Evaluate how relevant the candidate's projects
are to this particular job.

7. KEYWORD ANALYSIS
Identify important job-related keywords
that are present and missing.

8. CERTIFICATION MATCH
Evaluate relevant certifications.

9. STRENGTHS
Explain the candidate's strongest matching points.

10. IMPROVEMENT SUGGESTIONS
Give practical suggestions to improve the resume
for this particular job.

11. RESUME TAILORING
Suggest better resume descriptions and improvements.
Never invent qualifications, skills, or experience.


SCORING REQUIREMENTS:

Evaluate the resume using six categories.

Give each category a score between 0 and 100.

Use these exact categories and considerations:

required_skills:
How well the candidate's demonstrated skills
match the required skills in the job description.

experience:
How relevant the candidate's experience is
to the position.

education:
How well the candidate's qualifications
match the educational requirements.

projects:
How relevant the candidate's practical projects
are to the job.

keywords:
How many important job-related keywords
are appropriately represented in the resume.

certifications:
How relevant the candidate's certifications
are to the job requirements.


IMPORTANT SCORING RULES:

- Give realistic scores based only on the supplied information.
- Do not assume missing skills or qualifications.
- Do not invent certifications or experience.
- Do not calculate the final weighted ATS score.
- Python will calculate the final weighted score.
- Give all six category scores.
- Do not omit any category.
- Output the scores in the exact format below.
- Do not put explanations on the scoring data lines.

SCORING DATA:
required_skills: 0
experience: 0
education: 0
projects: 0
keywords: 0
certifications: 0

Replace every zero with your actual score between 0 and 100.
"""

    result = generate_response(prompt)

    return result
