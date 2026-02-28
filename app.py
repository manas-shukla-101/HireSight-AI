import json
import os
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, send_file, session, url_for

from auth import ensure_admin_exists, login_user, register_user
from database import create_connection, create_tables
from reports import generate_report_file
from utils import analyze_resume, extract_text_from_pdf


app = Flask(__name__)
app.secret_key = os.environ.get("HIRESIGHT_SECRET", "dev-secret-change-me")

create_tables()
ensure_admin_exists()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("index"))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access required.", "error")
            return redirect(url_for("dashboard"))
        return view(*args, **kwargs)

    return wrapped


@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("user"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if action == "register":
            ok, msg = register_user(username, password)
            flash(msg, "success" if ok else "error")
        elif action == "login":
            user = login_user(username, password)
            if user:
                session["user"] = user["username"]
                session["role"] = user["role"]
                return redirect(url_for("dashboard"))
            flash("Invalid username or password.", "error")

    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    conn = create_connection()
    rows = conn.execute(
        "SELECT match_score FROM history WHERE username = ? ORDER BY id DESC LIMIT 20",
        (session["user"],),
    ).fetchall()
    conn.close()

    scores = [round(row["match_score"] * 100, 2) for row in rows]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0

    return render_template(
        "dashboard.html",
        scores=list(reversed(scores)),
        total_analyses=len(scores),
        avg_score=avg_score,
    )


@app.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    analysis = None

    if request.method == "POST":
        uploaded = request.files.get("resume")
        jd_text = request.form.get("job_description", "").strip()

        if not uploaded or uploaded.filename == "":
            flash("Upload a resume PDF.", "error")
            return render_template("analyzer.html", analysis=None)

        if not uploaded.filename.lower().endswith(".pdf"):
            flash("Only PDF files are supported.", "error")
            return render_template("analyzer.html", analysis=None)

        if not jd_text:
            flash("Paste a job description.", "error")
            return render_template("analyzer.html", analysis=None)

        resume_text = extract_text_from_pdf(uploaded)
        if not resume_text:
            flash("Could not extract text from this PDF.", "error")
            return render_template("analyzer.html", analysis=None)

        analysis = analyze_resume(resume_text, jd_text)
        analysis["filename"] = uploaded.filename

        conn = create_connection()
        conn.execute(
            """
            INSERT INTO history (
                username, filename, match_score, grade, missing_skills, strengths, recommendations, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                session["user"],
                uploaded.filename,
                analysis["score"],
                analysis["grade"],
                json.dumps(analysis["missing_skills"]),
                json.dumps(analysis["strengths"]),
                json.dumps(analysis["recommendations"]),
            ),
        )
        conn.commit()
        conn.close()

    return render_template("analyzer.html", analysis=analysis)


@app.route("/download-report", methods=["POST"])
@login_required
def download_report():
    payload = request.form.get("analysis_payload", "")
    if not payload:
        flash("No analysis available for download.", "error")
        return redirect(url_for("analyze"))

    analysis = json.loads(payload)
    report_file = generate_report_file(analysis)
    report_file.seek(0)

    base_name = (analysis.get("filename") or "resume").rsplit(".", 1)[0]
    return send_file(
        report_file,
        as_attachment=True,
        download_name=f"{base_name}_analysis.txt",
        mimetype="text/plain",
    )


@app.route("/history")
@login_required
def history():
    conn = create_connection()
    rows = conn.execute(
        """
        SELECT filename, match_score, grade, created_at
        FROM history
        WHERE username = ?
        ORDER BY id DESC
        """,
        (session["user"],),
    ).fetchall()
    conn.close()

    return render_template("history.html", rows=rows)


@app.route("/admin")
@login_required
@admin_required
def admin():
    conn = create_connection()

    users = conn.execute(
        "SELECT id, username, role, created_at FROM users ORDER BY id DESC"
    ).fetchall()

    analyses = conn.execute(
        """
        SELECT username, filename, match_score, grade, created_at
        FROM history
        ORDER BY id DESC
        LIMIT 100
        """
    ).fetchall()

    user_count = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()["count"]
    analysis_count = conn.execute("SELECT COUNT(*) AS count FROM history").fetchone()["count"]

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        analyses=analyses,
        user_count=user_count,
        analysis_count=analysis_count,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
