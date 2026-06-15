import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [

    "python",
    "java",
    "javascript",
    "c",
    "c++",
    "php",

    "flask",
    "django",
    "react",
    "nodejs",

    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",

    "git",
    "github",
    "docker",

    "aws",
    "azure",

    "html",
    "css",
    "bootstrap",
    "tailwind",

    "rest api",
    "linux"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:

        if skill.lower() in text:

            found_skills.append(skill)

    return list(set(found_skills))