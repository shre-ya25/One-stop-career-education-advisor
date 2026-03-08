# skill_gap.py

def find_skill_gap(user_skills, required_skills):
    """
    Compares user skills with required job skills
    and returns a list of missing skills.
    """

    # Convert user skills to lowercase for comparison
    user_skills_lower = [skill.lower() for skill in user_skills]

    missing_skills = []

    for skill in required_skills:
        if skill.lower() not in user_skills_lower:
            missing_skills.append(skill)

    return missing_skills