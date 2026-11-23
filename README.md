# ResuNova AI 🚀

**AI-Powered Resume Analyzer, ATS Checker & Resume Improver**

ResuNova AI is an intelligent resume analysis application built using Python and Streamlit. It helps users evaluate their resumes, understand ATS compatibility, identify areas for improvement, and enhance their resumes using AI.

## ✨ Features

- **Resume Analyzer:** Extract and analyze resume content.
- **ATS Compatibility Checker:** Evaluate resumes for ATS compatibility.
- **AI Resume Improver:** Get AI-powered suggestions to improve resume content.
- **Google Authentication:** Secure Google sign-in.
- **Analysis History:** Access previous resume analysis results.
- **Resume File Support:** Upload PDF and DOCX resumes.
- **Resume Export:** Export improved resume content.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini AI
- Firebase / Google Authentication
- PDF and DOCX processing libraries

## 📂 Project Structure

```text
ResuNova-AI/
│
├── app.py
├── requirements.txt
├── modules/
│   ├── __init__.py
│   ├── resume_parser.py
│   ├── ats_analyzer.py
│   ├── resume_improver.py
│   └── resume_exporter.py
│
├── utils/
│   ├── __init__.py
│   ├── llm.py
│   └── scoring_engine.py
│
└── .gitignore
```

## 🚀 How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/polisettisvnamaanikanta-lgtm/ResuNova-AI.git
```

2. Open the project directory:

```bash
cd ResuNova-AI
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the environment on Windows:

```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Configure the required API credentials and authentication secrets locally.

7. Run the application:

```bash
python -m streamlit run app.py
```

## 🔐 Security

- API keys and authentication credentials should be stored securely.
- Never commit `.env` files or private authentication credentials.
- Keep sensitive configuration files out of version control.

## 👨‍💻 Project Status

ResuNova AI is an ongoing project. More features and improvements are planned.

---

**Built with Python, Streamlit and AI.**
