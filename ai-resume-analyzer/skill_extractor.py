# skill_extractor.py

import re

# Basic skill list (you can expand later)
SKILL_LIST = [
    "python", "java", "c", "c++", "html", "css", "javascript", "react",
    "django", "flask", "sql", "mysql", "mongodb", "git", "github",
    "machine learning", "data analysis", "power bi", "excel", "tableau",
    "spring", "hibernate", "bootstrap"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILL_LIST:
        # use word boundary to avoid partial matches
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills