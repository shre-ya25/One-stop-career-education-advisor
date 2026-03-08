def resume_agent(resume_score, ats_score, job_match, missing_skills):
    actions = []

    if resume_score < 70:
        actions.append("Improve resume structure")

    if ats_score < 70:
        actions.append("Optimize resume for ATS")

    if job_match < 60:
        actions.append("Recommend skill learning path")

    if missing_skills:
        actions.append("Generate skill roadmap")

    if not actions:
        actions.append("Resume is job-ready")

    return actions
