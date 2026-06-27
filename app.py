from flask import Flask, render_template, request
import os

# Utils Imports
from utils.parser import extract_text_from_file
from utils.skill_extractor import extract_skills
from utils.ats_score import calculate_ats_score
from utils.job_matcher import match_resume_with_job
from utils.ai_suggestions import generate_ai_feedback
from utils.pdf_generator import generate_pdf_report

from utils.experience_extractor import extract_experience
from utils.interview_questions import generate_interview_questions
from utils.recommendations import generate_recommendations
from utils.resume_summary import generate_resume_summary
from utils.semantic_match import semantic_match_score
from utils.resume_parser import (
    extract_name,
    extract_email,
    extract_mobile
)
from flask import Flask, render_template, request, redirect, session
from models import db, Candidate
from datetime import datetime
from flask_mail import Mail, Message
from flask import jsonify
from flask import send_from_directory
from dotenv import load_dotenv
load_dotenv()






app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

app.secret_key = "anuj123"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

db.init_app(app)


# ======================================================
# HOME PAGE
# ======================================================

@app.route('/')
def home():

    return render_template(
        'index.html'
    )
#

@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

#====================================================

@app.route('/admin-login', methods=['POST'])
def admin_login():

    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin123":

        session["admin"] = True

        return redirect("/dashboard")

    return "Invalid Username or Password"

#===========================================================================

#

@app.route('/dashboard')
def dashboard():

    if not session.get("admin"):

      return redirect("/login")

    search = request.args.get('search', '').lower().strip()
    

    print("Search:", search)

    if search:

        candidates = Candidate.query.filter(
            Candidate.skills.ilike(f"%{search}%")
        ).order_by(
            Candidate.final_score.desc()
        ).all()

    else:

        candidates = Candidate.query.order_by(
            Candidate.final_score.desc()
        ).all()

    # Total Candidates
    total_candidates = Candidate.query.count()

    # Average ATS Score
    all_candidates = Candidate.query.all()

    if all_candidates:

        avg_ats = round(
            sum(c.ats_score for c in all_candidates)
            / len(all_candidates),
            1
        )

    else:

        avg_ats = 0

    print("Found:", len(candidates))
    for c in candidates:
        print(
            c.id,
            c.ats_score,
            c.match_score,
            c.final_score,
            c.name,
            c.email,
            c.mobile,
            c.address
        )


    top_candidates = Candidate.query.order_by(
    Candidate.final_score.desc()
    ).limit(5).all()

    selected_count = Candidate.query.filter_by(
    status="Selected"
    ).count()

    rejected_count = Candidate.query.filter_by(
        status="Rejected"
    ).count()

    shortlisted_count = Candidate.query.filter_by(
        status="Shortlisted"
    ).count()

    interview_count = Candidate.query.filter_by(
        status="Interview Scheduled"
    ).count()

    applied_count = Candidate.query.filter_by(
        status="Applied"
    ).count()

    return render_template(
        'dashboard.html',
        candidates=candidates,
        top_candidates=top_candidates,
        search=search,
        total_candidates=total_candidates,
        selected_count=selected_count,
        rejected_count=rejected_count,
        shortlisted_count=shortlisted_count,
        interview_count=interview_count,
        applied_count=applied_count,
        avg_ats=avg_ats
    )
#============================================

@app.route('/candidate/<int:id>')
def candidate_details(id):

    candidate = Candidate.query.get_or_404(id)

    return render_template(
        'candidate.html',
        candidate=candidate
    )

@app.route('/update-status/<int:id>', methods=['POST'])
def update_status(id):

    candidate = Candidate.query.get_or_404(id)

    candidate.status = request.form.get("status")

    db.session.commit()

    return redirect(f"/candidate/{id}")

#======================================================
@app.route('/download_resume/<int:id>')
def download_resume(id):

    candidate = Candidate.query.get_or_404(id)

    return send_from_directory(

        app.config['UPLOAD_FOLDER'],
        candidate.resume_file,
        as_attachment=True

    )

@app.route("/move_candidate", methods=["POST"])
def move_candidate():

    data = request.get_json()

    print(data)

    return "OK"

    candidate = Candidate.query.get(data["id"])

    candidate.status = data["status"]

    db.session.commit()

    return jsonify({
        "success": True
    })

#==========================================================

@app.route('/pipeline')
def pipeline():

    if not session.get("admin"):
        return redirect("/login")

    applied = Candidate.query.filter_by(status="Applied").all()
    shortlisted = Candidate.query.filter_by(status="Shortlisted").all()
    interview = Candidate.query.filter_by(status="Interview Scheduled").all()
    selected = Candidate.query.filter_by(status="Selected").all()
    rejected = Candidate.query.filter_by(status="Rejected").all()

    return render_template(
        "pipeline.html",
        applied=applied,
        shortlisted=shortlisted,
        interview=interview,
        selected=selected,
        rejected=rejected
    )
#=======================================================

@app.route('/send_interview_email/<int:id>')
def send_interview_email(id):

    candidate = Candidate.query.get_or_404(id)

    msg = Message(

        subject="Interview Invitation",

        sender=app.config['MAIL_USERNAME'],

        recipients=[candidate.email]

    )

    msg.body = f"""
Hello {candidate.name},

Congratulations!

Your interview has been scheduled.

Date: {candidate.interview_date}

Time: {candidate.interview_time}

Round: {candidate.interview_round}

Regards,
HR Team
"""

    mail.send(msg)

    return redirect(f"/candidate/{id}")

@app.route('/update-notes/<int:id>', methods=['POST'])
def update_notes(id):

    candidate = Candidate.query.get_or_404(id)

    notes = request.form.get("notes")

    print("NOTES =", notes)

    candidate.notes = notes

    db.session.commit()

    print("SAVED SUCCESSFULLY")

    return redirect(f"/candidate/{id}")

@app.route('/schedule_interview/<int:id>', methods=['POST'])
def schedule_interview(id):

    candidate = Candidate.query.get_or_404(id)

    candidate.interview_date = request.form.get(
        "interview_date"
    )

    candidate.interview_time = request.form.get(
        "interview_time"
    )

    candidate.interview_round = request.form.get(
        "interview_round"
    )

    candidate.status = "Interview Scheduled"

    db.session.commit()

    return redirect(f"/candidate/{id}")

#============================================
# RESUME UPLOAD & ANALYSIS
# ======================================================

@app.route('/upload', methods=['POST'])
def upload_resume():

    # --------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------

    if 'resume' not in request.files:

        return "No File Uploaded"

    file = request.files['resume']

    if file.filename == '':

        return "No Selected File"

    # --------------------------------------------------
    # SAVE FILE
    # --------------------------------------------------

    filepath = os.path.join(

        app.config['UPLOAD_FOLDER'],
        file.filename

    )

    file.save(filepath)

    # --------------------------------------------------
    # EXTRACT RESUME TEXT
    # --------------------------------------------------

    extracted_text = extract_text_from_file(
        filepath
    )
    name = extract_name(extracted_text)

    email = extract_email(extracted_text)

    mobile = extract_mobile(extracted_text)

    # --------------------------------------------------
    # EXTRACT SKILLS
    # --------------------------------------------------

    skills = extract_skills(
        extracted_text
    )

    # --------------------------------------------------
    # ATS SCORE
    # --------------------------------------------------

    ats_score, feedback = calculate_ats_score(

        extracted_text,
        skills

    )

    # --------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------

    job_description = request.form.get('job_description')

    print("Name:", request.form.get("name"))
    print("Email:", request.form.get("email"))
    print("Mobile:", request.form.get("mobile"))
    print("Address:", request.form.get("address"))

    # --------------------------------------------------
    # JOB MATCHING
    # --------------------------------------------------

    match_score, matched_skills, missing_skills = match_resume_with_job(

        skills,
        job_description

    )
    
    final_score = (

        ats_score + match_score

     ) / 2

    # --------------------------------------------------
    # AI RESUME SUGGESTIONS
    # --------------------------------------------------

    ai_feedback = generate_ai_feedback(
        extracted_text
    )

    # --------------------------------------------------
    # EXPERIENCE EXTRACTION
    # --------------------------------------------------
         # --------------------------------------------------
    # EXPERIENCE EXTRACTION
    # --------------------------------------------------

    experience = extract_experience(
        extracted_text
    )

    # --------------------------------------------------
    # SAVE CANDIDATE TO DATABASE
    # --------------------------------------------------
    
    candidate = Candidate(
        name=name,
        email=email,
        mobile=mobile,
        resume_file=file.filename,
        address=request.form.get("address"),
        ats_score=ats_score,
        match_score=match_score,
        final_score=final_score,
        skills=", ".join(skills),
        experience=experience,
        status="Applied",
        created_at=datetime.now()
    )
    db.session.add(candidate)
    print("Extracted Name:", name)
    print("EMAIL FROM RESUME =", email)
    print("Extracted Mobile:", mobile)
    
    db.session.commit()

    # --------------------------------------------------
    # AI INTERVIEW QUESTIONS
    # --------------------------------------------------

    interview_questions = generate_interview_questions(
        skills
    )

    # --------------------------------------------------
    # SMART RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = generate_recommendations(

        skills,
        missing_skills

    )
    
    # --------------------------------------------------
    # AI INTERVIEW QUESTIONS
    # --------------------------------------------------

    interview_questions = generate_interview_questions(
        skills
    )

    # --------------------------------------------------
    # SMART RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = generate_recommendations(

        skills,
        missing_skills

    )

    # --------------------------------------------------
    # AI RESUME SUMMARY
    # --------------------------------------------------

    resume_summary = generate_resume_summary(

        skills,
        experience

    )

    # --------------------------------------------------
    # SEMANTIC MATCH SCORE
    # --------------------------------------------------

    semantic_score = semantic_match_score(

        extracted_text,
        job_description

    )

    # --------------------------------------------------
    # GENERATE PDF REPORT
    # --------------------------------------------------

    pdf_report = generate_pdf_report(

        ats_score,
        match_score,
        skills,
        missing_skills,
        feedback,
        ai_feedback

    )
 
    # --------------------------------------------------
    # RENDER RESULT PAGE
    # --------------------------------------------------

    return render_template(

        'result.html',

        # Resume
        text=extracted_text,

        # Skills
        skills=skills,

        # ATS
        ats_score=ats_score,
        feedback=feedback,

        # Job Match
        match_score=match_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,

        # AI Suggestions
        ai_feedback=ai_feedback,

        # Experience
        experience=experience,

        # AI Interview Questions
        interview_questions=interview_questions,

        # Recommendations
        recommendations=recommendations,

        # Resume Summary
        resume_summary=resume_summary,

        # Semantic Matching
        semantic_score=semantic_score,

        # PDF
        pdf_report=pdf_report,

        #FINAL SCORE
        final_score=final_score

    )


# ======================================================
# MAIN
# ======================================================

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )
    print(app.url_map)
    

    app.run(debug=True)