from flask import Flask, render_template, request
from pypdf import PdfReader

app = Flask(__name__)

REQUIRED_SKILLS = ["python", "flask", "sql", "machine learning", "data analysis"]

@app.route("/", methods=["GET", "POST"])
def home():
    ats_score = 0
    matched = []
    missing = []
    suggestions = []
    jd_text = ""

    if request.method == "POST":
        pdf = request.files["pdf"]
        jd_text = request.form["jd"]

        reader = PdfReader(pdf)
        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text()

        resume_text = resume_text.lower()
        jd_text = jd_text.lower()

        for skill in REQUIRED_SKILLS:
            if skill in resume_text:
                matched.append(skill)
            else:
                missing.append(skill)

        ats_score = int((len(matched) / len(REQUIRED_SKILLS)) * 100)

        if ats_score < 50:
            suggestions.append("Improve technical skills section.")
        if "project" not in resume_text:
            suggestions.append("Add projects section.")
        if "experience" not in resume_text:
            suggestions.append("Add work experience section.")
        if len(resume_text) < 800:
            suggestions.append("Resume content is too short.")

    return render_template(
        "index.html",
        ats_score=ats_score,
        matched=matched,
        missing=missing,
        suggestions=suggestions,
        jd_text=jd_text
    )

if __name__ == "__main__":
    app.run(debug=True)
