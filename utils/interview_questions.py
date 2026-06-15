def generate_interview_questions(skills):

    questions = []

    skill_questions = {

        "python": [
            "What are Python decorators?",
            "Explain Python OOP concepts."
        ],

        "flask": [
            "Explain Flask routing.",
            "What is Jinja2 in Flask?"
        ],

        "mysql": [
            "What is normalization?",
            "Difference between DELETE and TRUNCATE?"
        ],

        "docker": [
            "What is Docker?",
            "Difference between Docker and Virtual Machine?"
        ],

        "aws": [
            "What is EC2?",
            "Explain cloud computing."
        ],

        "rest api": [
            "What is REST API?",
            "Difference between GET and POST?"
        ]
    }

    for skill in skills:

        if skill in skill_questions:

            questions.extend(
                skill_questions[skill]
            )

    return questions