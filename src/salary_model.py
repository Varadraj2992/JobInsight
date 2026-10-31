from pathlib import Path

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "data" / "cleaned_jobs.csv"

MODEL_DIR = PROJECT_ROOT / "models"

MODEL_FILE = MODEL_DIR / "salary_model.joblib"


# =========================================================
# LOAD DATA
# =========================================================

print("Loading salary data...")

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

print(
    f"Total job records: {len(df)}"
)


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "salary_min",
    "salary_max",
    "title",
    "country",
    "years_experience_numeric"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print(
        "\nMissing required columns:"
    )

    print(
        missing_columns
    )

    raise SystemExit


# =========================================================
# CREATE TARGET SALARY
# =========================================================

print(
    "\nCreating average salary..."
)

df["salary_min"] = pd.to_numeric(
    df["salary_min"],
    errors="coerce"
)

df["salary_max"] = pd.to_numeric(
    df["salary_max"],
    errors="coerce"
)


df["average_salary"] = df[
    [
        "salary_min",
        "salary_max"
    ]
].mean(
    axis=1
)


# =========================================================
# SELECT VALID SALARY RECORDS
# =========================================================

model_data = df[
    df["average_salary"].notna()
].copy()


model_data = model_data[
    model_data["average_salary"] > 0
]


print(
    f"Salary records available: "
    f"{len(model_data)}"
)


# =========================================================
# CHECK DATA
# =========================================================

if len(model_data) < 20:

    print(
        "Not enough salary records "
        "to train the model."
    )

    raise SystemExit


# =========================================================
# FEATURES
# =========================================================

features = [

    "title",

    "country",

    "years_experience_numeric",

    "industry",

    "function",

    "experience_level",

    "education_level",

    "work_model"

]


target = "average_salary"


# Keep only features that actually
# exist in the dataset.

features = [
    column
    for column in features
    if column in model_data.columns
]


X = model_data[
    features
].copy()


y = model_data[
    target
].copy()


# =========================================================
# CLEAN FEATURES
# =========================================================

categorical_features = [

    column

    for column in [

        "title",
        "country",
        "industry",
        "function",
        "experience_level",
        "education_level",
        "work_model"

    ]

    if column in features

]


numeric_features = [

    column

    for column in [

        "years_experience_numeric"

    ]

    if column in features

]


for column in categorical_features:

    X[column] = (
        X[column]
        .fillna("Unknown")
        .astype(str)
    )


for column in numeric_features:

    X[column] = pd.to_numeric(
        X[column],
        errors="coerce"
    )


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)


print(
    f"Training records: {len(X_train)}"
)

print(
    f"Testing records: {len(X_test)}"
)


# =========================================================
# PREPROCESSING
# =========================================================

preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",

            Pipeline(
                steps=[

                    (
                        "imputer",

                        SimpleImputer(
                            strategy="most_frequent"
                        )
                    ),

                    (
                        "encoder",

                        OneHotEncoder(
                            handle_unknown="ignore"
                        )
                    )

                ]
            ),

            categorical_features

        ),

        (
            "numeric",

            SimpleImputer(
                strategy="median"
            ),

            numeric_features

        )

    ]

)


# =========================================================
# RANDOM FOREST MODEL
# =========================================================

model = RandomForestRegressor(

    n_estimators=100,

    random_state=42,

    n_jobs=-1

)


# =========================================================
# PIPELINE
# =========================================================

pipeline = Pipeline(

    steps=[

        (
            "preprocessor",

            preprocessor

        ),

        (
            "model",

            model

        )

    ]

)


# =========================================================
# TRAIN MODEL
# =========================================================

print(
    "\nTraining salary prediction model..."
)


pipeline.fit(

    X_train,

    y_train

)


# =========================================================
# PREDICTIONS
# =========================================================

predictions = pipeline.predict(

    X_test

)


# =========================================================
# EVALUATION
# =========================================================

mae = mean_absolute_error(

    y_test,

    predictions

)


rmse = mean_squared_error(

    y_test,

    predictions

) ** 0.5


r2 = r2_score(

    y_test,

    predictions

)


# =========================================================
# RESULTS
# =========================================================

print(
    "\n======================================"
)

print(
    "SALARY MODEL RESULTS"
)

print(
    "======================================"
)


print(
    f"MAE  : ${mae:,.2f}"
)


print(
    f"RMSE : ${rmse:,.2f}"
)


print(
    f"R²   : {r2:.4f}"
)


print(
    "======================================"
)


# =========================================================
# SAVE MODEL
# =========================================================

MODEL_DIR.mkdir(

    exist_ok=True

)


joblib.dump(

    pipeline,

    MODEL_FILE

)


print(
    "\nModel saved successfully:"
)


print(
    MODEL_FILE
)


print(
    "\nSALARY MODEL TRAINING COMPLETED!"
)