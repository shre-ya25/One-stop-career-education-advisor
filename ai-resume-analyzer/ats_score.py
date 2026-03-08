def calculate_ats_score(resume_skills, required_skills):
    if not required_skills:
        return 0

    resume_lower = set(s.lower() for s in resume_skills)
    required_lower = set(s.lower() for s in required_skills)

    matched = resume_lower.intersection(required_lower)
    score = (len(matched) / len(required_lower)) * 100

    return int(round(score))
