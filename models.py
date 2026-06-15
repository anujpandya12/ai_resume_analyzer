from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Candidate(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    email = db.Column(
        db.String(100)
    )

    ats_score = db.Column(
        db.Integer
    )

    match_score = db.Column(
        db.Integer
    )

    skills = db.Column(
        db.Text
    )

    experience = db.Column(
        db.String(50)
    )

    created_at = db.Column(
        db.DateTime
    )
    final_score = db.Column(
       db.Float
    )
    mobile = db.Column(
        db.String(20)
    )
    address = db.Column( 
        db.Text
    )
    status = db.Column(
        db.String(50),
        default="Applied"
    )

    interview_date = db.Column(
        db.String(50)
    )

    interview_time = db.Column(
        db.String(50)
    )

    interview_round = db.Column(
        db.String(100)
    )
    notes = db.Column(
        db.Text,
        default=""
    )