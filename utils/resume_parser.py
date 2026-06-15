import re

def extract_email(text):

    text = text.replace(" ", "")

    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    match = re.search(email_pattern, text)

    if match:
        return match.group(0)

    return "Not Found"

def extract_mobile(text):

    patterns = [

        r'(\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}',

        r'\d{3}-\d{3}-\d{4}',

        r'\(\d{3}\)\s?\d{3}-\d{4}'

    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group()

    return "Not Found"


def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line.split()) >= 2 and len(line.split()) <= 4:

            return line

    return "Unknown"