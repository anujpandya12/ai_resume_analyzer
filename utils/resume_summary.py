def generate_resume_summary(
    skills,
    experience
):

    summary = f"""

    Backend Developer skilled in
    {', '.join(skills[:5])}

    with experience level:
    {experience}.

    Passionate about building scalable
    web applications and backend systems.

    """

    return summary