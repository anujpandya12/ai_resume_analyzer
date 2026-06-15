import re


def calculate_ats_score(text, skills):

    score = 0

    feedback = []

    text = text.lower()

    # -------------------------
    # Skills Score
    # -------------------------

    skills_score = min(len(skills) * 5, 40)

    score += skills_score

    if skills_score >= 20:
        feedback.append("✔ Good technical skills detected")
    else:
        feedback.append("✘ Add more technical skills")

    # -------------------------
    # Resume Length
    # -------------------------

    word_count = len(text.split())

    if word_count > 300:
        score += 15
        feedback.append("✔ Resume content length is good")
    else:
        feedback.append("✘ Resume content is too short")

    # -------------------------
    # Projects Section
    # -------------------------

    if "project" in text or "projects" in text:
        score += 15
        feedback.append("✔ Projects section found")
    else:
        feedback.append("✘ Add projects section")

    # -------------------------
    # Education Section
    # -------------------------

    if "education" in text:
        score += 10
        feedback.append("✔ Education section found")
    else:
        feedback.append("✘ Add education details")

    # -------------------------
    # Contact Information
    # -------------------------

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    phone_pattern = r"\d{10}"

    if re.search(email_pattern, text):
        score += 5

    if re.search(phone_pattern, text):
        score += 5

    if re.search(email_pattern, text) and re.search(phone_pattern, text):
        feedback.append("✔ Contact information found")
    else:
        feedback.append("✘ Add proper contact information")

    # -------------------------
    # GitHub / LinkedIn
    # -------------------------

    if "github" in text:
        score += 5
        feedback.append("✔ GitHub profile added")
    else:
        feedback.append("✘ Add GitHub profile")

    if "linkedin" in text:
        score += 5
        feedback.append("✔ LinkedIn profile added")
    else:
        feedback.append("✘ Add LinkedIn profile")

    return score, feedback