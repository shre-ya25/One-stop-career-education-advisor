def calculate_resume_score(text, skills):
    score = 0

    if len(text.split()) > 300:
        score += 30

    if len(skills) >= 5:
        score += 30

    sections = ["experience", "education", "skills", "projects"]
    found = sum(1 for s in sections if s in text.lower())
    score += found * 10

    return min(score, 100)
