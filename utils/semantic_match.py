def semantic_match_score(
    resume_text,
    job_description
):

    resume_words = set(
        resume_text.lower().split()
    )

    job_words = set(
        job_description.lower().split()
    )

    common_words = resume_words.intersection(
        job_words
    )

    if len(job_words) == 0:
        return 0

    score = int(
        (len(common_words) / len(job_words)) * 100
    )

    return score