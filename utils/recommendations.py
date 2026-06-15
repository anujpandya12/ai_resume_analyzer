def generate_recommendations(

    skills,
    missing_skills

):

    recommendations = []

    # Convert to lowercase
    missing_skills = [
        skill.lower()
        for skill in missing_skills
    ]

    # Docker
    if "docker" in missing_skills:

        recommendations.append(
            "Learn Docker for deployment and DevOps skills."
        )

    # PostgreSQL
    if "postgresql" in missing_skills:

        recommendations.append(
            "Learn PostgreSQL for advanced database management."
        )

    # REST API
    if "rest api" in missing_skills:

        recommendations.append(
            "Build REST API projects using Flask."
        )

    # AWS
    if "aws" in missing_skills:

        recommendations.append(
            "Learn AWS cloud deployment and EC2."
        )

    # No Recommendations
    if len(recommendations) == 0:

        recommendations.append(
            "Your resume matches most required skills."
        )

    return recommendations