import pandas as pd
import numpy as np
import os


# ==========================================
# 1. LOAD DATA
# ==========================================

INPUT_FILE = "data/jobs.csv"
OUTPUT_FILE = "data/cleaned_jobs.csv"


print("Loading dataset...")

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

print(f"Original dataset shape: {df.shape}")


# ==========================================
# 2. REMOVE DUPLICATES
# ==========================================

print("\nChecking duplicates...")

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows found: {duplicate_count}")

df = df.drop_duplicates()

print(f"Shape after removing duplicates: {df.shape}")


# ==========================================
# 3. CLEAN COLUMN NAMES
# ==========================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# ==========================================
# 4. CLEAN TEXT COLUMNS
# ==========================================

text_columns = df.select_dtypes(
    include=["object"]
).columns

for column in text_columns:

    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ==========================================
# 5. CLEAN IMPORTANT TEXT FIELDS
# ==========================================

important_text_columns = [
    "title",
    "normalized_title",
    "company_name",
    "skills_required",
    "minimum_qualifications",
    "preferred_qualifications",
    "job_description",
    "city",
    "country",
    "work_model",
    "experience_level",
    "education_level"
]

for column in important_text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )


# ==========================================
# 6. CLEAN NUMERIC COLUMNS
# ==========================================

numeric_columns = [
    "salary_min",
    "salary_max",
    "years_experience_numeric",
    "latitude",
    "longitude",
    "travel_percentage"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ==========================================
# 7. CREATE AVERAGE SALARY
# ==========================================

if "salary_min" in df.columns and "salary_max" in df.columns:

    df["average_salary"] = df[
        ["salary_min", "salary_max"]
    ].mean(axis=1)


# ==========================================
# 8. CREATE SALARY RANGE
# ==========================================

if "salary_min" in df.columns and "salary_max" in df.columns:

    df["salary_range"] = (
        df["salary_max"] - df["salary_min"]
    )


# ==========================================
# 9. NORMALIZE WORK MODEL
# ==========================================

if "work_model" in df.columns:

    df["work_model"] = (
        df["work_model"]
        .str.lower()
        .str.strip()
    )


# ==========================================
# 10. NORMALIZE EXPERIENCE LEVEL
# ==========================================

if "experience_level" in df.columns:

    df["experience_level"] = (
        df["experience_level"]
        .str.lower()
        .str.strip()
    )


# ==========================================
# 11. NORMALIZE COUNTRY
# ==========================================

if "country" in df.columns:

    df["country"] = (
        df["country"]
        .str.lower()
        .str.strip()
    )


# ==========================================
# 12. REMOVE JOBS WITHOUT BASIC INFORMATION
# ==========================================

required_columns = [
    "title",
    "job_description"
]

for column in required_columns:

    if column in df.columns:

        df = df[
            df[column].notna()
        ]

        df = df[
            df[column].astype(str).str.strip() != ""
        ]


# ==========================================
# 13. RESET INDEX
# ==========================================

df = df.reset_index(drop=True)


# ==========================================
# 14. SAVE CLEAN DATA
# ==========================================

os.makedirs("data", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# 15. DISPLAY SUMMARY
# ==========================================

print("\n====================================")
print("DATA PREPROCESSING COMPLETED")
print("====================================")

print(f"Final dataset shape: {df.shape}")

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(
    df.isna()
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

print("\nClean dataset saved to:")
print(OUTPUT_FILE)

