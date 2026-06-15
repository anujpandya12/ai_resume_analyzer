def generate_ai_feedback(resume_text):

    resume_text = resume_text.lower()

    suggestions = []

    # -------------------------
    # GitHub
    # -------------------------

    if "github" not in resume_text:

        suggestions.append(
            "Add GitHub profile link."
        )

    # -------------------------
    # LinkedIn
    # -------------------------

    if "linkedin" not in resume_text:

        suggestions.append(
            "Add LinkedIn profile."
        )

    # -------------------------
    # REST API
    # -------------------------

    if "rest api" not in resume_text:

        suggestions.append(
            "Add REST API project experience."
        )

    # -------------------------
    # Docker
    # -------------------------

    if "docker" not in resume_text:

        suggestions.append(
            "Add Docker deployment skills."
        )

    # -------------------------
    # AWS
    # -------------------------

    if "aws" not in resume_text:

        suggestions.append(
            "Add cloud experience like AWS."
        )

    # -------------------------
    # Strong Action Verbs
    # -------------------------

    suggestions.append(
        "Use strong action verbs like Developed, Built, Implemented, Optimized."
    )

    # -------------------------
    # Project Descriptions
    # -------------------------

    suggestions.append(
        "Add measurable achievements in project descriptions."
    )

    # -------------------------
    # Professional Summary
    # -------------------------

    suggestions.append(
        "Write a strong professional summary for backend development roles."
    )

    return suggestions