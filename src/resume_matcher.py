import re

import pandas as pd

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    TfidfVectorizer = None
    cosine_similarity = None
    SKLEARN_AVAILABLE = False


# ==========================================
# JOBINSIGHT - RESUME JOB MATCHING
# ==========================================


def create_job_text(jobs_df):

    # --------------------------------------
    # Check if job_text already exists
    # --------------------------------------

    if "job_text" in jobs_df.columns:

        return (
            jobs_df["job_text"]
            .fillna("")
            .astype(str)
        )


    # --------------------------------------
    # Create job text from available columns
    # --------------------------------------

    text_columns = [

        "title",

        "normalized_title",

        "skills_required",

        "minimum_qualifications",

        "preferred_qualifications",

        "responsibilities",

        "job_description"

    ]


    available_columns = [

        column

        for column in text_columns

        if column in jobs_df.columns

    ]


    if not available_columns:

        return pd.Series(
            [""] * len(jobs_df),
            index=jobs_df.index
        )


    job_text = (

        jobs_df[available_columns]

        .fillna("")

        .astype(str)

        .agg(" ".join, axis=1)

    )


    return job_text


# ==========================================
# MATCH RESUME TO JOBS
# ==========================================


def _tokenise(text):
    return set(
        token.lower()
        for token in re.findall(r"[a-z0-9+#.]+", str(text).lower())
        if token.strip()
    )


def _fallback_match_scores(resume_text, job_texts):
    resume_tokens = _tokenise(resume_text)
    if not resume_tokens:
        return [0.0 for _ in job_texts]

    scores = []
    for job_text in job_texts:
        job_tokens = _tokenise(job_text)
        if not job_tokens:
            scores.append(0.0)
            continue

        overlap = len(resume_tokens & job_tokens)
        union = len(resume_tokens | job_tokens)
        score = (overlap / union) * 100 if union else 0.0
        scores.append(round(score, 2))

    return scores


def match_resume_to_jobs(

    resume_text,

    jobs_df

):

    # --------------------------------------
    # Check resume
    # --------------------------------------

    if not resume_text:

        result = jobs_df.copy()

        result["match_score"] = 0.0

        return result


    # --------------------------------------
    # Clean resume text
    # --------------------------------------

    resume_text = str(
        resume_text
    ).strip()


    if not resume_text:

        result = jobs_df.copy()

        result["match_score"] = 0.0

        return result


    # --------------------------------------
    # Get job text
    # --------------------------------------

    job_texts = create_job_text(
        jobs_df
    )


    job_texts = (
        job_texts
        .fillna("")
        .astype(str)
        .tolist()
    )


    # --------------------------------------
    # TF-IDF when available; otherwise use a simple overlap fallback
    # --------------------------------------

    if not SKLEARN_AVAILABLE:
        scores = _fallback_match_scores(resume_text, job_texts)
    else:
        all_text = [resume_text] + job_texts

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=10000
        )

        matrix = vectorizer.fit_transform(all_text)
        similarity = cosine_similarity(matrix[0:1], matrix[1:])
        scores = (similarity[0] * 100).round(2)


    # --------------------------------------
    # Create result
    # --------------------------------------

    result = jobs_df.copy()


    result["match_score"] = scores


    # --------------------------------------
    # Sort highest match first
    # --------------------------------------

    result = (

        result

        .sort_values(

            "match_score",

            ascending=False

        )

        .reset_index(

            drop=True

        )

    )


    return result