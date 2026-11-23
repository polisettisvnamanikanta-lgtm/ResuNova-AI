
import re


# --------------------------------------------------
# RESUME SCORING WEIGHTS
# --------------------------------------------------

RESUME_WEIGHTS = {
    "completeness": 25,
    "skills": 20,
    "projects": 20,
    "education": 15,
    "experience": 10,
    "readability": 10
}


# --------------------------------------------------
# ATS SCORING WEIGHTS
# --------------------------------------------------

ATS_WEIGHTS = {
    "required_skills": 30,
    "experience": 25,
    "education": 15,
    "projects": 15,
    "keywords": 10,
    "certifications": 5
}


# --------------------------------------------------
# GRADE CALCULATION
# --------------------------------------------------

def get_grade(score):

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Average"

    else:
        return "Needs Improvement"


# --------------------------------------------------
# EXTRACT CATEGORY SCORES FROM AI RESPONSE
# --------------------------------------------------

def extract_criteria(text, weights):

    criteria = {}

    for category in weights:

        pattern = (
            rf"^\s*(?:[-*]\s*)?(?:\*\*)?"
            rf"{re.escape(category)}"
            rf"(?:\*\*)?\s*:\s*(\d{{1,3}})\b"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.MULTILINE
        )

        if not match:

            raise ValueError(
                f"Could not find a valid score for {category}."
            )

        score = int(match.group(1))

        if not 0 <= score <= 100:

            raise ValueError(
                f"Invalid score for {category}. "
                "Score must be between 0 and 100."
            )

        criteria[category] = score

    return criteria


# --------------------------------------------------
# WEIGHTED SCORE CALCULATION
# --------------------------------------------------

def calculate_weighted_score(criteria, weights):

    if set(criteria) != set(weights):

        raise ValueError(
            "The scoring categories do not match the configured weights."
        )

    if sum(weights.values()) != 100:

        raise ValueError(
            "Scoring weights must add up to 100."
        )

    total = 0

    for category, weight in weights.items():

        performance = criteria[category]

        if not isinstance(performance, (int, float)):

            raise ValueError(
                f"Invalid score for {category}."
            )

        if not 0 <= performance <= 100:

            raise ValueError(
                f"Score for {category} must be between 0 and 100."
            )

        total += performance * weight / 100

    return round(total)


# --------------------------------------------------
# RESUME SCORE
# --------------------------------------------------

def calculate_resume_score(criteria):

    score = calculate_weighted_score(
        criteria,
        RESUME_WEIGHTS
    )

    return {
        "score": score,
        "grade": get_grade(score)
    }


# --------------------------------------------------
# ATS SCORE
# --------------------------------------------------

def calculate_ats_score(criteria):

    score = calculate_weighted_score(
        criteria,
        ATS_WEIGHTS
    )

    return {
        "score": score,
        "grade": get_grade(score)
    }
