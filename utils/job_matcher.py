def match_resume_with_job(
    resume_skills,
    job_description
):

    job_description = job_description.lower()

    matched_skills = []

    missing_skills = []

    for skill in resume_skills:

        if skill.lower() in job_description:

            matched_skills.append(skill)

    # Skills required in job but missing in resume
    REQUIRED_SKILLS = [

        "python",
        "flask",
        "django",
        "mysql",
        "postgresql",
        "docker",
        "aws",
        "git",
        "rest api",
        "kubernetes"
    ]

    for skill in REQUIRED_SKILLS:

        if skill in job_description and skill not in resume_skills:

            missing_skills.append(skill)

    # Match Score
    total_required = len(matched_skills) + len(missing_skills)

    if total_required == 0:
        match_score = 0
    else:
        match_score = int(
            (len(matched_skills) / total_required) * 100
        )

    return (
        match_score,
        matched_skills,
        missing_skills
    )