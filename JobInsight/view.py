import pandas as pd

# Read the parquet file
df = pd.read_parquet(r"C:\Users\bhand\Downloads\nextgig_jobs_2026-06.parquet")

# View the first few rows
print(df.head())

# Optional: Save as a CSV file to open in Excel
df.to_csv("output.csv", index=False)