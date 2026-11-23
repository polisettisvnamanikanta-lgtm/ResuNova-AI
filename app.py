import os
import sys
import types
import hashlib
import traceback
from datetime import datetime

import streamlit as st

# =========================================================
# PROJECT PATH + LOCAL PACKAGE BINDING
# =========================================================
# Guarantees that "modules" and "utils" always point to the folders next to
# app.py, even after the Google login redirect, OneDrive syncing, Streamlit
# reruns, or another installed package that uses the same name.

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT in sys.path:
    sys.path.remove(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)


def bind_local_package(package_name):
    package_dir = os.path.join(PROJECT_ROOT, package_name)

    if not os.path.isdir(package_dir):
        return

    # Create the missing __init__.py automatically
    init_file = os.path.join(package_dir, "__init__.py")
    if not os.path.isfile(init_file):
        try:
            open(init_file, "a", encoding="utf-8").close()
        except OSError:
            pass

    loaded = sys.modules.get(package_name)
    loaded_paths = [
        os.path.normcase(os.path.abspath(p))
        for p in getattr(loaded, "__path__", [])
    ] if loaded else []

    if os.path.normcase(package_dir) in loaded_paths:
        return

    # Remove any wrong package with the same name, then bind ours
    for name in [
        n for n in sys.modules
        if n == package_name or n.startswith(package_name + ".")
    ]:
        del sys.modules[name]

    package = types.ModuleType(package_name)
    package.__path__ = [package_dir]
    package.__file__ = init_file
    package.__package__ = package_name
    sys.modules[package_name] = package


for _package in ("modules", "utils"):
    bind_local_package(_package)

IMPORT_ERROR = None

try:
    from modules.resume_parser import extract_resume_text
    from modules.ats_analyzer import analyze_resume_against_job
    from modules.resume_improver import improve_resume
    from modules.resume_exporter import create_word_resume, create_pdf_resume

    from utils.llm import generate_response

    from utils.scoring_engine import (
        RESUME_WEIGHTS,
        ATS_WEIGHTS,
        extract_criteria,
        calculate_resume_score,
        calculate_ats_score,
    )
except Exception as _import_error:
    IMPORT_ERROR = _import_error
    IMPORT_TRACE = traceback.format_exc()


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ResuNova AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Show a clear message (instead of a crash) if any project file is missing
if IMPORT_ERROR is not None:
    st.error(f"ResuNova could not load a project file: {IMPORT_ERROR}")

    def _list_dir(path):
        return sorted(os.listdir(path)) if os.path.isdir(path) else "FOLDER NOT FOUND"

    st.markdown("**What Python can see:**")
    st.code(
        f"Project folder : {PROJECT_ROOT}\n"
        f"Files here     : {_list_dir(PROJECT_ROOT)}\n"
        f"modules folder : {_list_dir(os.path.join(PROJECT_ROOT, 'modules'))}\n"
        f"utils folder   : {_list_dir(os.path.join(PROJECT_ROOT, 'utils'))}"
    )
    with st.expander("Technical details"):
        st.code(IMPORT_TRACE)
    st.stop()


# =========================================================
# DESIGN SYSTEM
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --navy: #101B3C;
        --navy-2: #172957;
        --blue: #3478F6;
        --blue-dark: #245DCE;
        --ink: #17213B;
        --muted: #68748D;
        --line: #E5EAF4;
        --surface: #FFFFFF;
        --page: #F4F7FD;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #F4F7FD;
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(244,247,253,0.92);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101B3C 0%, #14264F 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: #F4F7FF;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 10px 12px;
        border-radius: 11px;
        margin: 3px 0;
        transition: background 0.2s ease;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(255,255,255,0.10);
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
        gap: 3px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label p {
        font-weight: 600;
        font-size: 0.94rem;
    }

    .brand-wrap {
        padding: 14px 8px 24px 8px;
        margin-bottom: 18px;
        border-bottom: 1px solid rgba(255,255,255,0.13);
    }

    .brand-mark {
        display: inline-flex;
        width: 46px;
        height: 46px;
        border-radius: 14px;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #5CA5FF, #6C63F5);
        font-size: 25px;
        box-shadow: 0 8px 22px rgba(45,111,238,0.30);
        vertical-align: middle;
        margin-right: 10px;
    }

    .brand-name {
        display: inline-block;
        vertical-align: middle;
        font-family: 'Manrope', sans-serif;
        font-size: 1.36rem;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: #FFFFFF;
    }

    .brand-subtitle {
        color: #AAB9DC;
        font-size: 0.73rem;
        margin: 8px 0 0 2px;
        letter-spacing: 1.1px;
        font-weight: 700;
    }

    .sidebar-note {
        margin-top: 34px;
        padding: 17px;
        border: 1px solid rgba(151,183,255,0.25);
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(66,112,224,0.25), rgba(95,82,218,0.18));
    }

    .sidebar-note-title {
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 6px;
    }

    .sidebar-note-copy {
        color: #C3D0EC;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    .main .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        color: #17213B !important;
        letter-spacing: -0.7px;
    }

    h1 { font-weight: 800 !important; }
    h2, h3 { font-weight: 750 !important; }

    p, li, label {
        color: #34415C;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 32px 36px;
        border-radius: 22px;
        background: linear-gradient(112deg, #101B3C 0%, #173A83 66%, #315FC4 100%);
        color: white;
        margin: 2px 0 22px 0;
        box-shadow: 0 14px 35px rgba(26,56,118,0.14);
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        right: -65px;
        top: -150px;
        background: rgba(135,177,255,0.12);
        border: 1px solid rgba(255,255,255,0.10);
    }

    .hero-kicker {
        color: #AFC9FF;
        text-transform: uppercase;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 1.7px;
        margin-bottom: 10px;
    }

    .hero-title {
        color: white !important;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(1.8rem, 3vw, 2.65rem);
        font-weight: 800;
        letter-spacing: -1.2px;
        line-height: 1.15;
        margin: 0 0 10px 0;
    }

    .hero-copy {
        color: #DCE7FF;
        font-size: 1rem;
        max-width: 720px;
        line-height: 1.6;
        margin: 0;
    }

    .hero-pill {
        display: inline-block;
        margin-top: 20px;
        border: 1px solid rgba(196,216,255,0.35);
        background: rgba(255,255,255,0.09);
        color: #F1F6FF;
        border-radius: 999px;
        padding: 8px 13px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .section-eyebrow {
        color: #3478F6;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .section-heading {
        color: #17213B;
        font-family: 'Manrope', sans-serif;
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.6px;
        margin: 0 0 5px 0;
    }

    .section-copy {
        color: #71809B;
        font-size: 0.91rem;
        margin-bottom: 18px;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E5EAF4;
        border-radius: 17px;
        padding: 17px 19px;
        min-height: 112px;
        box-shadow: 0 5px 18px rgba(30,55,100,0.035);
    }

    .metric-label {
        color: #74819A;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 9px;
    }

    .metric-value {
        color: #17213B;
        font-family: 'Manrope', sans-serif;
        font-size: 1.65rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .metric-hint {
        color: #8A96AA;
        font-size: 0.75rem;
        margin-top: 7px;
    }

    .feature-card {
        background: #FFFFFF;
        border: 1px solid #E5EAF4;
        border-radius: 17px;
        padding: 19px;
        min-height: 150px;
        box-shadow: 0 5px 18px rgba(30,55,100,0.035);
    }

    .feature-icon {
        display: inline-flex;
        width: 39px;
        height: 39px;
        border-radius: 12px;
        align-items: center;
        justify-content: center;
        background: #EAF1FF;
        font-size: 19px;
        margin-bottom: 12px;
    }

    .feature-title {
        color: #1C2945;
        font-weight: 800;
        font-size: 0.98rem;
        margin-bottom: 5px;
    }

    .feature-copy {
        color: #77839A;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    .info-card {
        background: #FFFFFF;
        border: 1px solid #E5EAF4;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 5px 18px rgba(30,55,100,0.035);
        margin-bottom: 14px;
    }

    .upload-hint {
        background: #F7FAFF;
        border: 1.5px dashed #9CB9F4;
        border-radius: 15px;
        padding: 15px;
        color: #62718F;
        text-align: center;
        font-size: 0.88rem;
        margin-bottom: 12px;
    }

    .score-number {
        font-family: 'Manrope', sans-serif;
        font-size: 2.55rem;
        font-weight: 800;
        color: #245DCE;
        line-height: 1.1;
    }

    .score-caption {
        color: #74819A;
        font-size: 0.83rem;
        font-weight: 600;
    }

    .status-chip {
        display: inline-block;
        border-radius: 999px;
        padding: 6px 11px;
        background: #EAF2FF;
        color: #245DCE;
        font-size: 0.76rem;
        font-weight: 800;
    }

    .stButton > button, .stDownloadButton > button {
        border-radius: 11px;
        min-height: 43px;
        font-weight: 700;
        border: 1px solid #DCE5F5;
        transition: all 0.2s ease;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(110deg, #3478F6, #5368E8);
        border: none;
        color: white;
        box-shadow: 0 7px 16px rgba(52,120,246,0.18);
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color: #3478F6;
        transform: translateY(-1px);
    }

    .stTextArea textarea, .stTextInput input {
        border-radius: 11px !important;
        border-color: #DCE4F1 !important;
        background: #FFFFFF !important;
    }

    [data-testid="stFileUploader"] {
        background: #F8FAFF;
        border: 1px dashed #A9BFF0;
        border-radius: 14px;
        padding: 8px;
    }

    [data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid #E5EAF4;
        border-radius: 12px;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E5EAF4;
        border-radius: 14px;
        padding: 14px;
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #3478F6, #6B72EF);
        border-radius: 99px;
    }

    hr {
        border-color: #E5EAF4 !important;
    }

    .footer {
        color: #8A96AA;
        text-align: center;
        font-size: 0.78rem;
        padding: 20px 0 0 0;
    }

    @media (max-width: 800px) {
        .main .block-container { padding: 1rem 1rem 2rem 1rem; }
        .hero { padding: 25px 22px; }
        .hero-title { font-size: 1.8rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# GOOGLE SIGN-IN GATE
# =========================================================

# Streamlit uses the OAuth credentials stored in .streamlit/secrets.toml.
# Users must sign in before accessing the resume-analysis dashboard.
if not st.user.is_logged_in:
    st.markdown(
        """
        <div style="max-width:620px;margin:8vh auto 0 auto;text-align:center;">
            <div style="font-size:3.2rem;margin-bottom:12px;">📄</div>
            <div style="font-size:2.35rem;font-weight:800;color:#17213B;">
                Welcome to ResuNova <span style="color:#3478F6;">AI</span>
            </div>
            <p style="font-size:1.05rem;color:#68748D;margin-top:12px;">
                Your AI-powered resume analyzer and career companion.
            </p>
            <p style="color:#68748D;margin-top:28px;">Sign in to continue to your workspace.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.button(
            "Continue with Google",
            type="primary",
            use_container_width=True,
            on_click=st.login,
        )
    st.stop()


# =========================================================
# SESSION STATE
# =========================================================

default_values = {
    "resume_text": "",
    "analysis_result": "",
    "ats_result": "",
    "analysis_cache": {},
    "improved_resume_result": "",
    "job_description": "",
    "analysis_history": [],
    "current_page": "Dashboard",
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def normalize_text(text):
    return "\n".join(
        line.rstrip()
        for line in text.replace("\r\n", "\n").splitlines()
    ).strip()


def create_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def add_history(item_type, score, details):
    st.session_state.analysis_history.insert(
        0,
        {
            "type": item_type,
            "score": score,
            "details": details,
            "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        },
    )
    st.session_state.analysis_history = st.session_state.analysis_history[:20]


def section_header(eyebrow, title, description=""):
    st.markdown(
        f"""
        <div class="section-eyebrow">{eyebrow}</div>
        <div class="section-heading">{title}</div>
        <div class="section-copy">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def display_score_card(result, title):
    score = max(0, min(100, int(result["score"])))
    st.markdown(
        f"""
        <div class="info-card">
            <div class="metric-label">{title}</div>
            <div class="score-number">{score}<span style="font-size:1.1rem;color:#8A96AA;"> / 100</span></div>
            <div style="margin-top:9px;"><span class="status-chip">{result["grade"]}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(score / 100)


def display_categories(criteria):
    friendly_names = {
        "required_skills": "Required Skills",
        "skills": "Skills",
        "experience": "Experience",
        "education": "Education",
        "projects": "Projects",
        "keywords": "Keywords",
        "certifications": "Certifications",
        "completeness": "Completeness",
        "readability": "Readability",
    }

    for category, score in criteria.items():
        label = friendly_names.get(
            category,
            category.replace("_", " ").title(),
        )
        left, right = st.columns([4, 1])
        with left:
            st.markdown(f"**{label}**")
            st.progress(max(0, min(100, int(score))) / 100)
        with right:
            st.markdown(
                f"<div style='text-align:right;font-weight:800;color:#245DCE;padding-top:3px;'>{score}/100</div>",
                unsafe_allow_html=True,
            )


def render_hero(title, copy, kicker="YOUR AI CAREER COMPANION"):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">{kicker}</div>
            <div class="hero-title">{title}</div>
            <p class="hero-copy">{copy}</p>
            <div class="hero-pill">✦ Analyze · Improve · Get hired</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SHARED AI ANALYSIS CACHE
# =========================================================

@st.cache_data(show_spinner=False)
def cached_resume_analysis(resume_text):
    resume_prompt = f"""
You are an expert resume reviewer, career advisor, and professional recruiter.

Analyze the following candidate resume.

RESUME:
{resume_text}

Provide these sections:
1. Overall Resume Assessment
2. Resume Strengths
3. Resume Weaknesses
4. Technical Skills Assessment
5. Projects Assessment
6. Education Assessment
7. Experience Assessment
8. Missing Skills and Keywords
9. Improvement Suggestions
10. Suggested Resume Improvements

SCORING:
Evaluate all six categories from 0 to 100:
- completeness: important resume sections, contact details, and information
- skills: relevance and presentation of skills
- projects: practical projects and demonstrated abilities
- education: qualifications and presentation
- experience: internships, work, leadership, and relevant activities
- readability: clarity, grammar, organization, and ease of reading

Rules:
- Use consistent, realistic scoring.
- Do not invent skills or experience.
- Score only information actually present.
- Do not calculate a final weighted score; Python calculates it.
- Include every category in exactly this format:

SCORING DATA:
completeness: [score]
skills: [score]
projects: [score]
education: [score]
experience: [score]
readability: [score]
"""

    result = generate_response(resume_prompt)
    if not result or result.startswith("Gemini API Error:"):
        raise RuntimeError(result or "Resume analysis failed.")

    extract_criteria(result, RESUME_WEIGHTS)
    return result


@st.cache_data(show_spinner=False)
def cached_ats_analysis(resume_text, job_description):
    result = analyze_resume_against_job(resume_text, job_description)

    if not result or result.startswith("Gemini API Error:"):
        raise RuntimeError(result or "ATS analysis failed.")

    extract_criteria(result, ATS_WEIGHTS)
    return result


# =========================================================
# SIDEBAR / BRAND NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand-wrap">
            <span class="brand-mark">📄</span>
            <span class="brand-name">ResuNova <span style="color:#75A9FF;">AI</span></span>
            <div class="brand-subtitle">ANALYZE · IMPROVE · GET HIRED</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page_options = [
        "Dashboard",
        "Resume Analyzer",
        "ATS Checker",
        "Resume Improver",
        "Analysis History",
        "About",
    ]

    selected_page = st.radio(
        "NAVIGATION",
        page_options,
        index=page_options.index(st.session_state.current_page)
        if st.session_state.current_page in page_options
        else 0,
        label_visibility="collapsed",
        key="page_navigation",
    )
    st.session_state.current_page = selected_page

    st.markdown(
        """
        <div class="sidebar-note">
            <div class="sidebar-note-title">🚀 Build a stronger profile</div>
            <div class="sidebar-note-copy">
                Get clear feedback, improve your resume, and prepare for your next opportunity.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='color:#91A3C9;font-size:0.72rem;margin-top:28px;text-align:center;'>RESUNOVA AI · YOUR CAREER, REIMAGINED</div>",
        unsafe_allow_html=True,
    )

    signed_in_email = st.user.get("email", "Signed in with Google")
    st.caption(f"Signed in: {signed_in_email}")
    if st.button("Sign out", use_container_width=True):
        st.logout()


# =========================================================
# DASHBOARD
# =========================================================

if selected_page == "Dashboard":
    render_hero(
        "Welcome to ResuNova AI!",
        "Your AI-powered resume analyzer and career assistant. Build an ATS-friendly, job-ready resume and present your skills with confidence.",
    )

    resume_status = "Resume uploaded" if st.session_state.resume_text else "Not uploaded yet"
    resume_score_text = "--"
    ats_score_text = "--"

    if st.session_state.analysis_result:
        try:
            current_criteria = extract_criteria(
                st.session_state.analysis_result,
                RESUME_WEIGHTS,
            )
            resume_score_text = f"{calculate_resume_score(current_criteria)['score']}/100"
        except Exception:
            pass

    if st.session_state.ats_result:
        try:
            current_ats_criteria = extract_criteria(
                st.session_state.ats_result,
                ATS_WEIGHTS,
            )
            ats_score_text = f"{calculate_ats_score(current_ats_criteria)['score']}/100"
        except Exception:
            pass

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""<div class="metric-card"><div class="metric-label">Resume status</div>
            <div class="metric-value" style="font-size:1.25rem;">{resume_status}</div>
            <div class="metric-hint">Your current workspace</div></div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="metric-card"><div class="metric-label">Resume quality score</div>
            <div class="metric-value">{resume_score_text}</div>
            <div class="metric-hint">Based on your resume analysis</div></div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="metric-card"><div class="metric-label">ATS compatibility</div>
            <div class="metric-value">{ats_score_text}</div>
            <div class="metric-hint">Based on your latest job match</div></div>""",
            unsafe_allow_html=True,
        )

    st.write("")
    section_header(
        "GET STARTED",
        "Your career workspace",
        "Choose a tool to start improving your resume.",
    )

    feature_cols = st.columns(3)
    feature_data = [
        ("📊", "Resume Analyzer", "Get an overall quality score and detailed feedback."),
        ("🎯", "ATS Checker", "Compare your resume with a specific job description."),
        ("✨", "Resume Improver", "Generate a clearer, more professional resume draft."),
    ]

    for col, (icon, title, copy) in zip(feature_cols, feature_data):
        with col:
            st.markdown(
                f"""<div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-copy">{copy}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.write("")
    with st.container(border=True):
        left, right = st.columns([3, 1])
        with left:
            st.markdown("### Ready to get started?")
            st.write("Upload your resume first. ResuNova AI will help you understand what is working and what can be improved.")
        with right:
            st.write("")
            if st.button("Open Resume Analyzer →", type="primary", use_container_width=True):
                st.session_state.current_page = "Resume Analyzer"
                st.rerun()

    st.caption("Scores are AI-generated estimates and are not official scores from an employer's ATS.")


# =========================================================
# RESUME ANALYZER
# =========================================================

elif selected_page == "Resume Analyzer":
    render_hero(
        "Resume Analyzer",
        "Upload your resume and receive structured feedback on its quality, strengths, weaknesses, and areas to improve.",
        "RESUME HEALTH CHECK",
    )

    section_header(
        "STEP 1",
        "Upload your resume",
        "Choose a PDF or DOCX file. Extract the text before running the analysis.",
    )

    with st.container(border=True):
        uploaded_file = st.file_uploader(
            "Choose your resume",
            type=["pdf", "docx"],
            help="Supported formats: PDF and DOCX.",
            key="resume_uploader",
        )

        if uploaded_file is not None:
            st.markdown(
                f"""<div class="upload-hint">📎 <b>{uploaded_file.name}</b> · {uploaded_file.size / 1024:.1f} KB</div>""",
                unsafe_allow_html=True,
            )

            if st.button("Extract Resume Text", type="primary"):
                try:
                    with st.spinner("Extracting text from your resume..."):
                        extracted_text = extract_resume_text(uploaded_file)

                    if extracted_text and extracted_text.strip():
                        extracted_text = normalize_text(extracted_text)
                        old_hash = create_hash(st.session_state.resume_text) if st.session_state.resume_text else ""
                        new_hash = create_hash(extracted_text)

                        if new_hash != old_hash:
                            st.session_state.analysis_result = ""
                            st.session_state.ats_result = ""
                            st.session_state.improved_resume_result = ""

                        st.session_state.resume_text = extracted_text
                        st.success("Resume text extracted successfully.")
                    else:
                        st.error("No readable text was found. If this is a scanned PDF, it may need OCR.")
                except Exception as error:
                    st.error(f"Resume extraction failed: {error}")

        if st.session_state.resume_text:
            st.success("A resume is ready for analysis.")
            with st.expander("Preview extracted resume text"):
                st.text_area(
                    "Extracted content",
                    st.session_state.resume_text,
                    height=240,
                    disabled=True,
                )
        else:
            st.info("Your extracted resume text will appear here after upload and extraction.")

    st.write("")
    section_header(
        "STEP 2",
        "Analyze your resume",
        "The AI reviews the information in your resume and scores six quality categories.",
    )

    if not st.session_state.resume_text:
        st.warning("Upload and extract your resume before starting the analysis.")
    else:
        if st.button("✨ Analyze My Resume", type="primary", use_container_width=True):
            resume_text = normalize_text(st.session_state.resume_text)
            resume_hash = create_hash(resume_text)
            cache_key = f"resume_{resume_hash}"

            if cache_key in st.session_state.analysis_cache:
                st.session_state.analysis_result = st.session_state.analysis_cache[cache_key]
                st.info("Loaded your previously saved analysis.")
            else:
                try:
                    with st.spinner("ResuNova AI is reviewing your resume. This may take a little time..."):
                        result = cached_resume_analysis(resume_text)

                    st.session_state.analysis_result = result
                    st.session_state.analysis_cache[cache_key] = result

                    try:
                        score = calculate_resume_score(
                            extract_criteria(result, RESUME_WEIGHTS)
                        )["score"]
                    except Exception:
                        score = None
                    add_history("Resume Analysis", score, "Overall resume quality review")
                    st.success("Resume analysis completed.")
                except Exception as error:
                    st.error(f"Resume analysis failed: {error}")

    if st.session_state.analysis_result:
        st.write("")
        section_header("YOUR RESULTS", "Resume quality overview", "Your score is calculated using the category weights configured in the scoring engine.")

        try:
            resume_criteria = extract_criteria(
                st.session_state.analysis_result,
                RESUME_WEIGHTS,
            )
            resume_result = calculate_resume_score(resume_criteria)

            score_col, breakdown_col = st.columns([1, 2])
            with score_col:
                display_score_card(resume_result, "Resume Quality Score")
            with breakdown_col:
                with st.container(border=True):
                    st.markdown("### Category breakdown")
                    display_categories(resume_criteria)

        except ValueError as error:
            st.warning(f"Resume scoring issue: {error}")

        with st.container(border=True):
            st.markdown("### Detailed AI feedback")
            st.markdown(st.session_state.analysis_result)


# =========================================================
# ATS CHECKER
# =========================================================

elif selected_page == "ATS Checker":
    render_hero(
        "ATS Compatibility Checker",
        "Understand how closely your resume matches a job description and identify the skills and keywords you may need to strengthen.",
        "JOB MATCH ANALYSIS",
    )

    section_header(
        "STEP 1",
        "Add the job description",
        "Paste the full job description for the role you are targeting.",
    )

    job_description = st.text_area(
        "Job description",
        value=st.session_state.job_description,
        height=230,
        placeholder="Paste the complete job description here...",
        key="ats_job_description_input",
    )
    st.session_state.job_description = job_description

    if not st.session_state.resume_text:
        st.warning("Please visit Resume Analyzer and upload/extract your resume first.")
    else:
        st.success("Your resume is available for comparison.")

    if st.button("🎯 Analyze ATS Compatibility", type="primary", use_container_width=True):
        if not st.session_state.resume_text:
            st.warning("Please upload and extract your resume first.")
        elif not job_description.strip():
            st.warning("Please paste a job description before continuing.")
        else:
            resume_text = normalize_text(st.session_state.resume_text)
            cleaned_job_description = normalize_text(job_description)
            combined_input = resume_text + "\n" + cleaned_job_description
            ats_hash = create_hash(combined_input)
            cache_key = f"ats_{ats_hash}"

            if cache_key in st.session_state.analysis_cache:
                st.session_state.ats_result = st.session_state.analysis_cache[cache_key]
                st.info("Loaded your previously saved ATS analysis.")
            else:
                try:
                    with st.spinner("Comparing your resume with the job description..."):
                        result = cached_ats_analysis(
                            resume_text,
                            cleaned_job_description,
                        )

                    st.session_state.ats_result = result
                    st.session_state.analysis_cache[cache_key] = result

                    try:
                        score = calculate_ats_score(
                            extract_criteria(result, ATS_WEIGHTS)
                        )["score"]
                    except Exception:
                        score = None
                    add_history("ATS Analysis", score, "Resume compared with a job description")
                    st.success("ATS analysis completed.")
                except Exception as error:
                    st.error(f"ATS analysis failed: {error}")

    if st.session_state.ats_result:
        st.write("")
        section_header("YOUR RESULTS", "ATS match overview", "The match score is an estimate based on the job description you provided.")

        try:
            ats_criteria = extract_criteria(
                st.session_state.ats_result,
                ATS_WEIGHTS,
            )
            ats_result = calculate_ats_score(ats_criteria)

            score_col, breakdown_col = st.columns([1, 2])
            with score_col:
                display_score_card(ats_result, "ATS Compatibility Score")
            with breakdown_col:
                with st.container(border=True):
                    st.markdown("### Match category breakdown")
                    display_categories(ats_criteria)

        except ValueError as error:
            st.warning(f"ATS scoring issue: {error}")

        with st.container(border=True):
            st.markdown("### Detailed ATS feedback")
            st.markdown(st.session_state.ats_result)


# =========================================================
# RESUME IMPROVER
# =========================================================

elif selected_page == "Resume Improver":
    render_hero(
        "Resume Improver",
        "Create a stronger, clearer resume draft with AI suggestions while keeping your real experience and achievements accurate.",
        "MAKE YOUR EXPERIENCE STAND OUT",
    )

    section_header(
        "STEP 1",
        "Choose how to improve your resume",
        "You can improve your resume generally or tailor it to a specific job description.",
    )

    if not st.session_state.resume_text:
        st.warning("Please upload and extract your resume in the Resume Analyzer page first.")
    else:
        tailor_resume = st.checkbox(
            "Tailor my resume to a job description",
            value=False,
            key="tailor_resume_checkbox",
        )

        selected_job_description = ""
        if tailor_resume:
            selected_job_description = st.text_area(
                "Paste the target job description",
                value=st.session_state.job_description,
                height=200,
                placeholder="Paste the job description you want to target...",
                key="improver_job_description",
            )
            if selected_job_description.strip():
                st.session_state.job_description = selected_job_description
        else:
            st.info("General improvement mode: the AI will improve clarity, structure, and professional wording without targeting a specific job.")

        if st.button("✨ Generate Improved Resume", type="primary", use_container_width=True):
            if tailor_resume and not selected_job_description.strip():
                st.warning("Please paste a job description or turn off job-specific tailoring.")
            else:
                try:
                    with st.spinner("Improving your resume. Please wait..."):
                        improved_result = improve_resume(
                            st.session_state.resume_text,
                            selected_job_description if tailor_resume else "",
                        )

                    if improved_result and not improved_result.startswith("Gemini API Error:"):
                        st.session_state.improved_resume_result = improved_result
                        st.success("Your improved resume draft is ready.")
                    else:
                        st.error(improved_result or "Resume improvement failed.")
                except Exception as error:
                    st.error(f"Resume improvement failed: {error}")

    if st.session_state.get("improved_resume_result"):
        st.write("")
        section_header("YOUR NEW DRAFT", "Improved resume preview", "Review the content carefully and verify every detail before using it.")

        with st.container(border=True):
            st.markdown(st.session_state.improved_resume_result)

        st.write("")
        section_header("EXPORT", "Download your improved resume", "Choose the format you need.")
        try:
            word_file = create_word_resume(st.session_state.improved_resume_result)
            pdf_file = create_pdf_resume(st.session_state.improved_resume_result)

            download_col1, download_col2 = st.columns(2)
            with download_col1:
                st.download_button(
                    "⬇ Download Word (DOCX)",
                    data=word_file,
                    file_name="resunova_improved_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
            with download_col2:
                st.download_button(
                    "⬇ Download PDF",
                    data=pdf_file,
                    file_name="resunova_improved_resume.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
        except Exception as error:
            st.error(f"Could not create download files: {error}")


# =========================================================
# ANALYSIS HISTORY
# =========================================================

elif selected_page == "Analysis History":
    render_hero(
        "Analysis History",
        "Review the analyses completed during this browser session.",
        "YOUR RECENT ACTIVITY",
    )

    if not st.session_state.analysis_history:
        with st.container(border=True):
            st.markdown("### No analysis history yet")
            st.write("Your completed resume and ATS analyses will appear here.")
    else:
        for item in st.session_state.analysis_history:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    st.markdown(f"**{item['type']}**")
                    st.caption(item["details"])
                with col2:
                    score_label = f"{item['score']}/100" if item["score"] is not None else "Available in results"
                    st.markdown(f"**{score_label}**")
                with col3:
                    st.caption(item["time"])

    st.caption("History is stored in the current Streamlit session. It is not a permanent database yet.")


# =========================================================
# ABOUT
# =========================================================

elif selected_page == "About":
    render_hero(
        "About ResuNova AI",
        "A student-built AI-powered resume analysis and improvement project designed to help candidates understand and strengthen their resumes.",
        "ABOUT THE PROJECT",
    )

    with st.container(border=True):
        st.markdown("### What ResuNova AI can do")
        st.markdown(
            """
            - **Resume analysis:** reviews resume quality, strengths, weaknesses, and improvement areas.
            - **ATS compatibility:** compares resume content with a job description.
            - **Resume improvement:** generates a refined draft while aiming to preserve the candidate's actual information.
            - **Downloads:** exports the improved resume as Word and PDF documents.
            """
        )

    with st.container(border=True):
        st.markdown("### Important note")
        st.write(
            "AI-generated feedback and scores are estimates for guidance. They are not official scores from an employer's applicant tracking system. Always review AI-generated content for accuracy before submitting a resume."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        <b>ResuNova AI</b> · Analyze · Improve · Get Hired<br>
        AI-generated scores are estimates and are not official employer ATS results.
    </div>
    """,
    unsafe_allow_html=True,
)
