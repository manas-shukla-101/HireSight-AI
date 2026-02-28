# HireSight AI 🚀

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white) 
![Flask](https://img.shields.io/badge/Flask-2.3-orange?logo=flask&logoColor=white) 
![SQLite](https://img.shields.io/badge/SQLite-3.41-lightgrey?logo=sqlite&logoColor=blue) 
![License](https://img.shields.io/badge/License-MIT-green) 
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)

**HireSight AI** is a cutting-edge **Smart Resume Analyzer** that helps recruiters and job seekers optimize hiring processes using **AI-powered resume evaluation**. It matches resumes to job descriptions, detects skill gaps, and provides actionable recommendations—all with NLP and semantic similarity techniques.

---

## 📌 Table of Contents

1. [Features](#-features)  
2. [Tech Stack & Architecture](#-tech-stack--architecture)  
3. [Project Structure](#-project-structure)  
4. [Live Demo](#-live-demo)  
5. [Local Setup](#-local-setup)  
6. [Default Admin Login](#-default-admin-login)  
7. [Environment Variables](#-environment-variables)  
8. [GitHub Upload Guidelines](#-github-upload-guidelines)  
9. [Why HireSight AI](#-why-hiresight-ai)  
10. [Roadmap](#-roadmap)

---

## 🌟 Features

- **Secure Authentication:** Role-based access (`user`, `admin`)  
- **Smart Resume Parsing:** Extract skills, experience, and education from PDFs  
- **AI-Powered Matching:** Semantic similarity scoring using **Sentence Transformers**  
- **Skill Gap Detection:** Identify missing or underrepresented skills  
- **Actionable Recommendations:** Personalized tips to improve resumes  
- **User History:** Track past analyses and improvements  
- **Admin Dashboard:** Analytics for recruiters and team insights  
- **Downloadable Reports:** Generate detailed PDF reports for sharing or records  

---

## 🛠 Tech Stack & Architecture

| Layer | Technologies |
|-------|-------------|
| Backend | Flask, SQLite, Python |
| NLP/ML | spaCy, Sentence Transformers, scikit-learn |
| Frontend | Jinja2 Templates, HTML5, CSS3, JavaScript, Chart.js |
| Security | Session management, role-based access, environment variables |
| Reporting | PDF generation via `reports.py` |

**Architecture Diagram (conceptual):**  
![Architecture Diagram](architecture-diagram.svg)

---

## 📂 Project Structure

```text
HireSight-AI/
├─ app.py               # Main Flask app
├─ auth.py              # Authentication & roles
├─ database.py          # SQLite connection & models
├─ utils.py             # Helpers (parsing, scoring)
├─ reports.py           # PDF generation
├─ requirements.txt     # Python dependencies
├─ templates/           # HTML Templates
│  ├─ base.html
│  ├─ index.html
│  ├─ dashboard.html
│  ├─ analyzer.html
│  ├─ history.html
│  └─ admin.html
└─ static/
   ├─ css/style.css
   └─ js/main.js
```
---

## 🎬 Live Demo

![App Demo](HireSight-AI.gif)  
> Demo showing resume upload, skill analysis, and AI scoring. 
  

---

## ⚡ Local Setup

1. **Clone the repository:**
```bash
git clone https://github.com/manas-shukla-101/HireSight-AI
cd HireSight-AI
```
2. **Create and activate a virtual environment:**
```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```
3. **Install dependencies:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
4. **Run the application locally:**
```bash
python app.py
```
5. **Open in browser:**
```bash
http://127.0.0.1:5000
```
---

## 🔐 Default Admin Login

- **Username:** `admin`  
- **Password:** `admin123`  

> ⚠️ **Important:** Change the admin password immediately after first login to ensure platform security.

---

## 🔑 Environment Variables

Set a secure secret key to protect session data and user authentication:

```bash
# Windows (PowerShell)
$env:HIRESIGHT_SECRET="your-strong-random-secret"

# macOS/Linux
export HIRESIGHT_SECRET="your-strong-random-secret"
```
---

## ⚠️ GitHub Upload Guidelines

To keep your repository clean and secure, avoid committing the following:

- `.venv/` – virtual environment files  
- `*.db` – database files (e.g., `hiresight.db`)  
- `__pycache__/` – Python cache files  
- Generated reports: `*.pdf`  
- `.env` files containing secrets  

---

## 🎯 Why HireSight AI?

**For Recruiters:** Quickly evaluate resumes, identify top talent, and reduce hiring bias.  
**For Job Seekers:** Understand skill gaps, optimize resumes, and improve interview chances.  
**For Teams:** Track analytics, monitor improvements, and maintain insights.  

> **HireSight AI combines AI intelligence, NLP precision, and user-focused design to make recruitment smarter, faster, and fairer.**

---

## 🚀 Roadmap

- [ ] Multi-language resume support  
- [ ] LinkedIn profile integration for enhanced analysis  
- [ ] Cloud deployment (AWS / Heroku) with HTTPS and authentication  
- [ ] Interactive visualizations for recruiters  
- [ ] Email notifications for analysis reports  

---

**Made with ❤️ by Manas Shukla – Data Science & AI Enthusiast**
