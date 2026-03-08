def simulate_future(job_match, missing_skills):
    improvement = len(missing_skills) * 5
    future_score = min(job_match + improvement, 95)

    return {
        "current": job_match,
        "future": future_score,
        "message": f"If you learn {len(missing_skills)} missing skills, your job match may increase to {future_score}%."
    }
