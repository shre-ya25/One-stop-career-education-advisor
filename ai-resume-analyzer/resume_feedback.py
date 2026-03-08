def analyze_resume_sections(text):
    feedback = []

    text_lower = text.lower()

    sections = {
        "experience": "Experience section is missing or weak.",
        "project": "Projects section is missing.",
        "education": "Education section not clearly found.",
        "skill": "Skills section is missing.",
        "certification": "No certifications found."
    }

    for section, message in sections.items():
        if section in text_lower:
            feedback.append(f"✅ {section.capitalize()} section looks good.")
        else:
            feedback.append(f"❌ {message}")

    return feedback
