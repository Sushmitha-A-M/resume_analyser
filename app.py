from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SKILLS = [
    "python",
    "java",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "flask",
    "machine learning",
    "git",
    "github"
]

@app.route('/')
def home():
    return "Resume Analyzer Backend is Running!"

def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text.lower()

    return text

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_resume():

    if request.method == 'GET':
        return jsonify({
            "message": "Analyze endpoint is working. Please send a POST request with a PDF file."
        })

    if 'resume' not in request.files:
        return jsonify({
            "error": "No resume file uploaded"
        }), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({
            "error": "No file selected"
        }), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        resume_text = extract_text(filepath)

        found_skills = []
        missing_skills = []

        for skill in SKILLS:
            if skill in resume_text:
                found_skills.append(skill)
            else:
                missing_skills.append(skill)

        score = int((len(found_skills) / len(SKILLS)) * 100)

        if score >= 80:
            prediction = "High Chance of Shortlisting"
        elif score >= 60:
            prediction = "Moderate Chance"
        else:
            prediction = "Needs Improvement"

        return jsonify({
            "score": score,
            "prediction": prediction,
            "found_skills": found_skills,
            "missing_skills": missing_skills
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)