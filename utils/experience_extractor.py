import re


def extract_experience(text):

    text = text.lower()

    experience_patterns = [

        r'(\d+)\s+years',
        r'(\d+)\s+year',
        r'(\d+)\+?\s+years'
    ]

    for pattern in experience_patterns:

        match = re.search(pattern, text)

        if match:

            return match.group(0)

    # Fresher Detection
    if "fresher" in text:
        return "Fresher"

    return "Experience Not Found"