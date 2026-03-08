def calculate_job_match(ats_score, resume_score):
    """
    Job Match is a weighted score:
    60% ATS score
    40% Resume quality score
    """

    job_match = (0.6 * ats_score) + (0.4 * resume_score)
    return int(round(job_match))
