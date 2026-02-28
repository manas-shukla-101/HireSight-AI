# HireSight AI

An advanced **Smart Resume Analyzer** built with **Flask + HTML/CSS/JS** that compares a resume against a job description using NLP and semantic similarity.

## Features

- Secure login/register system with role support (`user`, `admin`)
- Resume parsing from PDF
- AI match scoring using Sentence Transformers
- Skill extraction and missing-skill detection
- Actionable recommendations for resume improvement
- User analysis history
- Admin dashboard for platform insights
- Downloadable analysis report

## Tech Stack

- Backend: Flask, SQLite
- NLP/ML: spaCy, Sentence Transformers, scikit-learn
- Frontend: Jinja2 templates, custom CSS, vanilla JavaScript, Chart.js

## Project Structure

```text
SRA/
├─ app.py
├─ auth.py
├─ database.py
├─ utils.py
├─ reports.py
├─ requirements.txt
├─ templates/
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

## Local Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd SRA
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. Run the app:
```bash
python app.py
```

5. Open:
`http://127.0.0.1:5000`

## Default Admin Login

- Username: `admin`
- Password: `admin123`

Change this password after first login.

## Environment Variable (Recommended)

Set a strong secret key:

```bash
# PowerShell
$env:HIRESIGHT_SECRET="your-strong-random-secret"
```

## What Not To Upload To GitHub

This repository already includes a `.gitignore` to exclude sensitive/local files.  
Avoid uploading:

- `.venv/`
- `__pycache__/`
- `*.db` (for example `hiresight.db`)
- corrupted/backups like `hiresight.corrupt.*.db`
- generated reports like `*.pdf`
- `.env` files

## Deployment Notes

For production deployment:

- Use `gunicorn` as WSGI server
- Keep `HIRESIGHT_SECRET` in platform env vars
- Use a managed database or persistent disk for SQLite

---

If you want, I can also generate:
- `LICENSE`
- `CONTRIBUTING.md`
- a cleaner deployment-ready folder (`instance/`, `migrations/`, `config.py`)

