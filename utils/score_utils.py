
import streamlit as st
import re


def get_score_grade(score):

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Average"

    else:
        return "Poor"


def extract_score(text, score_type):

    pattern = rf"{score_type}\s*:\s*(\d{{1,3}})"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        score = int(match.group(1))

        if 0 <= score <= 100:
            return score

    return None


def display_score(score, title):

    if score is not None:

        grade = get_score_grade(score)

        st.metric(
            label=title,
            value=f"{score}/100",
            delta=grade
        )

        st.progress(score / 100)

    else:
        st.warning("Score could not be extracted. Please generate the analysis again.")
