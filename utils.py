import re
from functools import lru_cache

import PyPDF2
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


SKILL_KEYWORDS = {
    "python", "java", "javascript", "typescript", "c", "c++", "sql", "nosql", "mongodb", "postgresql",
    "mysql", "redis", "flask", "fastapi", "django", "spring", "react", "nextjs", "angular", "vue",
    "html", "css", "bootstrap", "tailwind", "node", "express", "rest", "graphql", "git", "github",
    "docker", "kubernetes", "aws", "azure", "gcp", "linux", "ci/cd", "jenkins", "terraform", "ansible",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "nlp", "llm", "machine learning",
    "data analysis", "power bi", "tableau", "excel", "spark", "hadoop", "communication", "leadership",
    "problem solving", "agile", "scrum", "microservices", "testing", "pytest", "unit testing",
}


@lru_cache(maxsize=1)
def get_nlp():
    return spacy.load("en_core_web_sm")


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(file_obj):
    reader = PyPDF2.PdfReader(file_obj)
    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text).strip()


def preprocess_text(text):
    cleaned = re.sub(r"\s+", " ", (text or "").lower()).strip()
    if not cleaned:
        return ""

    doc = get_nlp()(cleaned)
    tokens = [tok.lemma_ for tok in doc if not tok.is_stop and not tok.is_punct and tok.lemma_.strip()]
    return " ".join(tokens)


def extract_skills(text):
    lowered = (text or "").lower()
    found = sorted({skill for skill in SKILL_KEYWORDS if skill in lowered})
    return found


def calculate_similarity(resume_text, jd_text):
    if not resume_text or not jd_text:
        return 0.0
    embeddings = get_model().encode([resume_text, jd_text])
    return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])


def grade_resume(score):
    if score >= 0.8:
        return "A - Excellent"
    if score >= 0.65:
        return "B - Strong"
    if score >= 0.5:
        return "C - Fair"
    return "D - Needs Improvement"


def build_recommendations(score, missing_skills):
    recs = []
    if score < 0.5:
        recs.append("Rewrite the resume summary to align directly with the role requirements.")
    if len(missing_skills) > 6:
        recs.append("Prioritize the top 5 required skills in a dedicated skills section.")
    if score < 0.7:
        recs.append("Add measurable impact in bullet points (numbers, percentages, outcomes).")
    if missing_skills:
        recs.append("Close skill gaps with project evidence for: " + ", ".join(missing_skills[:5]) + ".")
    if not recs:
        recs.append("Resume is well aligned. Focus on role-specific achievements and concise formatting.")
    return recs


def analyze_resume(resume_raw_text, jd_raw_text):
    resume_processed = preprocess_text(resume_raw_text)
    jd_processed = preprocess_text(jd_raw_text)

    score = calculate_similarity(resume_processed, jd_processed)
    grade = grade_resume(score)

    resume_skills = extract_skills(resume_raw_text)
    jd_skills = extract_skills(jd_raw_text)

    matched_skills = sorted(set(resume_skills).intersection(jd_skills))
    missing_skills = sorted(set(jd_skills) - set(resume_skills))

    strengths = []
    if score >= 0.75:
        strengths.append("High semantic alignment with the job description.")
    if matched_skills:
        strengths.append(f"Matched {len(matched_skills)} key skills required for the role.")
    if not strengths:
        strengths.append("Base structure exists, but role alignment needs improvement.")

    recommendations = build_recommendations(score, missing_skills)

    return {
        "score": score,
        "grade": grade,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "strengths": strengths,
        "recommendations": recommendations,
    }
