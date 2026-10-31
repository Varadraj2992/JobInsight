from pathlib import Path
import pandas as pd
import ast


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "data" / "jobs_with_skills.csv"
SKILL_FILE = PROJECT_ROOT / "data" / "skill_frequency.csv"


# =========================================================
# LOAD DATA
# =========================================================

print("Loading job data...")

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

print(f"Loaded {len(df)} job records.")


# =========================================================
# PARSE EXTRACTED SKILLS
# =========================================================

def parse_skills(value):

    if pd.isna(value):
        return []

    try:

        result = ast.literal_eval(
            str(value)
        )

        if isinstance(result, list):
            return result

    except Exception:
        pass

    return []


df["parsed_skills"] = (
    df["extracted_skills"]
    .apply(parse_skills)
)


# =========================================================
# SKILL FREQUENCY
# =========================================================

print("Calculating skill frequency...")

all_skills = []

for skills in df["parsed_skills"]:

    all_skills.extend(skills)


skill_frequency = (
    pd.Series(all_skills)
    .value_counts()
    .reset_index()
)

skill_frequency.columns = [
    "skill",
    "frequency"
]


# =========================================================
# SAVE SKILL FREQUENCY
# =========================================================

skill_frequency.to_csv(
    SKILL_FILE,
    index=False
)


# =========================================================
# TOP JOB ROLES
# =========================================================

print("\n==============================")
print("TOP JOB ROLES")
print("==============================")

if "job_title" in df.columns:

    print(
        df["job_title"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
        .head(10)
    )


# =========================================================
# TOP LOCATIONS
# =========================================================

print("\n==============================")
print("TOP LOCATIONS")
print("==============================")

if "country" in df.columns:

    print(
        df["country"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
        .head(10)
    )


# =========================================================
# TOP COMPANIES
# =========================================================

print("\n==============================")
print("TOP COMPANIES")
print("==============================")

if "company" in df.columns:

    print(
        df["company"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
        .head(10)
    )


# =========================================================
# SALARY ANALYSIS
# =========================================================

if "annual_salary_usd" in df.columns:

    salary_data = df[
        df["annual_salary_usd"].notna()
    ]

    print("\n==============================")
    print("SALARY ANALYSIS")
    print("==============================")

    print(
        f"Salary records: {len(salary_data)}"
    )

    if len(salary_data) > 0:

        print(
            f"Average annual salary: "
            f"${salary_data['annual_salary_usd'].mean():,.2f}"
        )

        print(
            f"Minimum annual salary: "
            f"${salary_data['annual_salary_usd'].min():,.2f}"
        )

        print(
            f"Maximum annual salary: "
            f"${salary_data['annual_salary_usd'].max():,.2f}"
        )


# =========================================================
# TOP SKILLS
# =========================================================

print("\n==============================")
print("TOP 10 SKILLS")
print("==============================")

print(
    skill_frequency.head(10)
)


# =========================================================
# COMPLETED
# =========================================================

print("\n==============================")
print("MARKET ANALYTICS COMPLETED!")
print("==============================")

print(
    f"Skill frequency saved to:"
)

print(
    SKILL_FILE
)