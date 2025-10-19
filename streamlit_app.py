import streamlit as st
import tempfile
import os
from sentence_transformers import SentenceTransformer, util
from fpdf import FPDF
import pdfplumber
from phi.agent import Agent
from phi.model.groq import Groq

# ==== Streamlit UI ====
st.set_page_config(page_title="PublicAltResumeGenAI", layout="wide")
st.title("🌟 AI Job Matcher & Resume Generator (Powered by Groq + Phi)")

# ==== Sidebar ====
with st.sidebar:
    st.header("🔑 API Key")
    user_groq_api_key = st.text_input("Enter your GROQ API Key", type="password")

    st.header("📄 Resume Upload")
    uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    st.header("📝 Job Description")
    job_description = st.text_area("Paste the job description here")

# ==== Load Model ====
model = SentenceTransformer("all-MiniLM-L6-v2")

# ==== Helper Functions ====
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def get_embedding(text):
    return model.encode(text, convert_to_tensor=True)

def get_match_score(resume_text, job_text):
    emb_resume = get_embedding(resume_text)
    emb_job = get_embedding(job_text)
    score = util.cos_sim(emb_resume, emb_job).item() * 100
    return round(score, 2)

def sanitize_text(text):
    return (
        text.replace("•", "-")  # replace bullet with dash
            .replace("–", "-")
            .replace("—", "-")
            .replace("“", '"')
            .replace("”", '"')
            .replace("‘", "'")
            .replace("’", "'")
    )


def generate_ai_resume(name, email, phone, location, job_description):
    prompt = f"""
Create a resume using the following structure and formatting style. Be concise, use bullet points, and highlight relevant skills and projects aligned to the job description.

Example Structure:
---
PROFILE SUMMARY
One paragraph summary...

WORK EXPERIENCE
Job Title
Company Name
Duration
• Task 1
• Task 2

EDUCATION
Degree - Year
University
Grade

KEY SKILLS
Skill 1, Skill 2, Skill 3, ...

PROJECTS
• Project 1 - Duration
• Project 2 - Duration

CERTIFICATIONS
• Certification - Date

PERSONAL DETAILS
Name: {name}
Email: {email}
Phone: {phone}
Location: {location}

Generate this resume tailored for the following job description:
{job_description}
"""
    agent = Agent(model=Groq(id="llama-3.1-8b-instant", api_key=user_groq_api_key))
    return agent.run(prompt).content

def suggest_resume_improvements(resume_text, job_description):
    prompt = f"""
Below is a resume and a job description.

Resume:
{resume_text}

Job Description:
{job_description}

Suggest improvements in:
- Missing keywords/skills
- Gaps in experience
- Formatting issues
- Overall enhancements

Return suggestions as bullet points.
"""
    agent = Agent(model=Groq(id="llama-3.1-8b-instant", api_key=user_groq_api_key))
    return agent.run(prompt).content

def save_resume_pdf(resume_text, filename):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    sanitized_text = sanitize_text(resume_text)

    for line in sanitized_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)


# ==== Resume Match + Actions ====
download_ready = False
resume_pdf_path = None

if uploaded_resume and job_description and user_groq_api_key:
    resume_text = extract_text_from_pdf(uploaded_resume)
    score = get_match_score(resume_text, job_description)
    st.success(f"✅ Resume matches the job description with a score of **{score}%**")

    st.subheader("🧠 Suggestions to Improve Your Resume")
    if st.button("🔍 Analyze Resume and Suggest Improvements"):
        suggestions = suggest_resume_improvements(resume_text, job_description)
        st.markdown(suggestions)

    st.subheader("🚀 Generate Tailored AI Resume")
    with st.form("resume_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        location = st.text_input("Location")
        submitted = st.form_submit_button("Generate Resume")

    if submitted:
        ai_resume = generate_ai_resume(name, email, phone, location, job_description)
        st.text_area("Generated Resume", ai_resume, height=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            save_resume_pdf(ai_resume, tmp.name)
            resume_pdf_path = tmp.name
            download_ready = True

    if download_ready and resume_pdf_path:
        with open(resume_pdf_path, "rb") as f:
            st.download_button("📥 Download Resume as PDF", data=f, file_name="AI_Resume.pdf")

elif not uploaded_resume:
    st.warning("⚠️ Please upload your resume.")
elif not job_description:
    st.warning("⚠️ Please paste a job description.")
elif not user_groq_api_key:
    st.warning("⚠️ Please enter your GROQ API Key.")
