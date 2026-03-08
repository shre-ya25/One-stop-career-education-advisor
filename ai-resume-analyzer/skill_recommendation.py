SKILL_SUGGESTIONS = {
    "python": "Practice advanced Python and build real-world projects.",
    "sql": "Learn advanced SQL queries and optimization.",
    "machine learning": "Study model evaluation and deployment.",
    "docker": "Learn containerization and DevOps basics.",
    "react": "Build frontend projects using React.",
    "javascript": "Improve ES6 concepts and async programming.",
    "git": "Practice version control workflows.",
}

def get_skill_recommendations(missing_skills):
    suggestions = []
    for skill in missing_skills:
        key = skill.lower()
        if key in SKILL_SUGGESTIONS:
            suggestions.append(f"{skill}: {SKILL_SUGGESTIONS[key]}")
        else:
            suggestions.append(f"{skill}: Learn this skill from online courses and practice.")
    return suggestions
