import pandas as pd
import os

# ---------------------------------------------------
# Base path setup
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

raw_path = os.path.join(BASE_DIR, "data", "raw", "raw_cases.csv")
processed_dir = os.path.join(BASE_DIR, "data", "processed")
processed_path = os.path.join(processed_dir, "cleaned_cases.csv")
type_key_path = os.path.join(BASE_DIR, "data", "keys", "type_name_key.csv")

print("Loading raw dataset from:", raw_path)

# Ensure processed directory exists
os.makedirs(processed_dir, exist_ok=True)

# ---------------------------------------------------
# Load raw dataset
# ---------------------------------------------------

df = pd.read_csv(
    raw_path,
    low_memory=False
)

print("Initial dataset shape:", df.shape)

# ---------------------------------------------------
# Early sampling (important for large datasets)
# ---------------------------------------------------

if len(df) > 500000:
    df = df.sample(n=300000, random_state=42)
    print("Sampled dataset for faster processing:", df.shape)

# ---------------------------------------------------
# Clean column names
# ---------------------------------------------------

df.columns = df.columns.str.strip()

# Replace placeholder missing values
df.replace([-9998, -9999], pd.NA, inplace=True)

# ---------------------------------------------------
# Convert date columns
# ---------------------------------------------------

df["date_of_filing"] = pd.to_datetime(
    df["date_of_filing"],
    errors="coerce",
    dayfirst=True
)

df["date_of_decision"] = pd.to_datetime(
    df["date_of_decision"],
    errors="coerce",
    dayfirst=True
)

# Remove rows with missing critical dates
df = df.dropna(subset=["date_of_filing", "date_of_decision"])

# ---------------------------------------------------
# Create target variable (case duration)
# ---------------------------------------------------

df["case_duration_days"] = (
    df["date_of_decision"] - df["date_of_filing"]
).dt.days

# Remove invalid durations
df = df[df["case_duration_days"] > 0]

print("After cleaning dates:", df.shape)

# ---------------------------------------------------
# Merge type_name mapping
# ---------------------------------------------------

print("Loading type_name key from:", type_key_path)

type_key = pd.read_csv(type_key_path)
type_key.columns = type_key.columns.str.strip()

df = df.merge(
    type_key[["year", "type_name", "type_name_s"]],
    on=["year", "type_name"],
    how="left"
)

# Replace numeric type_name with readable label
df["type_name"] = df["type_name_s"].fillna(df["type_name"].astype(str))

df.drop(columns=["type_name_s"], inplace=True)

print("Merged type_name labels")
print("Missing mapped type_name values:", df["type_name"].isna().sum())

# ---------------------------------------------------
# Clean gender columns
# ---------------------------------------------------

gender_cols = [
    "female_defendant",
    "female_petitioner",
    "female_adv_def",
    "female_adv_pet"
]

for col in gender_cols:
    if col in df.columns:
        df[col] = df[col].replace("-9998 unclear", pd.NA)

# ---------------------------------------------------
# Final sampling for ML (optional)
# ---------------------------------------------------

if len(df) > 200000:
    df = df.sample(n=200000, random_state=42)
    print("Final sampled dataset for ML:", df.shape)

# ---------------------------------------------------
# Save processed dataset
# ---------------------------------------------------

df.to_csv(processed_path, index=False)

print("Final dataset shape:", df.shape)
print("Cleaned dataset saved successfully at:", processed_path)