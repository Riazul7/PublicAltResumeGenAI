# 🌟 PublicAltResumeGenAI

🎯 **AI Job Matcher & Resume Generator**  
Powered by **Groq + Phi + SentenceTransformers**

---

## 🔥 What It Does

**PublicAltResumeGenAI** is a Streamlit-based application that allows users to:

✅ Upload their existing resume (PDF)  
✅ Paste any job description  
✅ Get a **match score** using semantic similarity  
✅ Generate a **tailored AI resume** using Groq's LLaMA3 model  
✅ Receive smart **resume improvement suggestions**  
✅ Download the final resume as a clean **PDF**

---

## 🛠 Features

- ✨ AI-powered resume rewriting based on job description  
- 🤖 Uses [Groq + Phi](https://groq.com/) for ultra-fast LLM response  
- 🔍 Resume-to-job match scoring using SentenceTransformers  
- 🧠 Improvement suggestions based on your existing resume  
- 📄 PDF generation with auto Unicode cleanup  
- 🔐 API Key input via UI (no .env required)

---

## 🚀 How to Run Locally

### 1. Clone this repository

git clone https://github.com/Riazul7/PublicAltResumeGenAI.git
cd PublicAltResumeGenAI

### 2. Create a virtual environment and activate it
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate  # Windows
### 3. Install dependencies
pip install -r requirements.txt
### 4. Run the app
streamlit run streamlit_app.py
🔑 Setup
This app does not use .env files. You provide your Groq API Key securely through the sidebar input.

📦 Dependencies
streamlit

fpdf

pdfplumber

sentence-transformers

phidata 

langchain-groq

Install them via:
pip install -r requirements.txt


📂 File Structure
.
├── streamlit_app.py         # Main app
├── requirements.txt         # All dependencies
├── README.md                # You're here
└── .venv/                   # Virtual environment (optional)
🧠 Future Ideas
 Resume formatting via HTML + WeasyPrint or Cloud APIs

 Multiple resume templates (modern, classic, minimalist)

 Export to .docx format

 LinkedIn + GitHub integration

🤝 Contributing
Contributions, ideas, and pull requests are welcome! Feel free to fork or raise issues.

💬 License
MIT License. Use freely for personal and professional purposes.

🔗 Demo 
https://publicaltresumegenai.streamlit.app/

👨‍💻 Built by
Riazul Azim — Associate Programmer Analyst | MG Tathya Solution Private Limited | Resume Matchmaker