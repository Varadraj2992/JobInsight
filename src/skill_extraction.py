from pathlib import Path
import pandas as pd
import re


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "data" / "cleaned_jobs.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "jobs_with_skills.csv"


# =========================================================
# SKILL LIST
# =========================================================

SKILLS = [
    "Python",
    "SQL",
    "R",
    "Java",
    "JavaScript",
    "TypeScript",
    "C++",
    "C#",
    "HTML",
    "CSS",
    "React",
    "Angular",
    "Vue",
    "Node.js",
    "Django",
    "Flask",
    "FastAPI",
    "AWS",
    "Azure",
    "Google Cloud",
    "GCP",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "Jenkins",
    "Linux",
    "Terraform",
    "Power BI",
    "Tableau",
    "Excel",
    "Looker",
    "Spark",
    "Hadoop",
    "Kafka",
    "Databricks",
    "Snowflake",
    "MongoDB",
    "MySQL",
    "PostgreSQL",
    "Oracle",
    "SQL Server",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Statistics",
    "Data Analysis",
    "Data Science",
    "Data Visualization",
    "Business Intelligence",
    "ETL",
    "Data Engineering",
    "Generative AI",
    "LLM",
    "Project Management",
    "Communication",
    "Leadership",
    "Agile",
    "Scrum",
]


# =========================================================
# SKILL EXTRACTION FUNCTION
# =========================================================

def extract_skills(text):

    if pd.isna(text):
        return []

    text = str(text).lower()

    found = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(
            skill.lower()
        ) + r"\b"

        if re.search(pattern, text):

            found.append(skill)

    return found

def build_jobs_with_skills():
    print("Loading cleaned job dataset...")

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    print(f"Loaded {len(df)} job records.")
    print("Creating combined job text...")

    text_columns = [
        "title",
        "skills_required",
        "minimum_qualifications",
        "preferred_qualifications",
        "responsibilities",
        "job_description"
    ]

    available_columns = [
        column
        for column in text_columns
        if column in df.columns
    ]

    df["job_text"] = (
        df[available_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
    )

    print("Extracting skills...")

    df["extracted_skills"] = (
        df["job_text"]
        .apply(extract_skills)
    )

    df["skill_count"] = (
        df["extracted_skills"]
        .apply(len)
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("======================================")
    print("SKILL EXTRACTION COMPLETED!")
    print("======================================")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Total jobs: {len(df)}")
    print("======================================")

    return df


if __name__ == "__main__":
    build_jobs_with_skills()