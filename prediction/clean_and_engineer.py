import pandas as pd
import os

# ---------------------------------------------------
# Base path setup (robust)
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

raw_path = os.path.join(BASE_DIR, "data", "raw", "raw_cases.csv")
processed_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_cases.csv")
type_key_path = os.path.join(BASE_DIR, "data", "keys", "type_name_key.csv")

print("Loading raw dataset from:", raw_path)

# ---------------------------------------------------
# Load raw dataset
# ---------------------------------------------------

df = pd.read_csv(raw_path)

print("Initial shape:", df.shape)

# Clean column names
df.columns = df.columns.str.strip()

# Replace placeholder missing values
df.replace([-9998, -9999], pd.NA, inplace=True)

# ---------------------------------------------------
# Convert date columns (important: dayfirst=True)
# ---------------------------------------------------

df["date_of_filing"] = pd.to_datetime(
    df["date_of_filing"], errors="coerce", dayfirst=True
)

df["date_of_decision"] = pd.to_datetime(
    df["date_of_decision"], errors="coerce", dayfirst=True
)

# Drop rows missing critical dates
df = df.dropna(subset=["date_of_filing", "date_of_decision"])

# ---------------------------------------------------
# Create target variable
# ---------------------------------------------------

df["case_duration_days"] = (
    df["date_of_decision"] - df["date_of_filing"]
).dt.days

# Remove invalid durations
df = df[df["case_duration_days"] > 0]

print("After cleaning dates:", df.shape)

# ---------------------------------------------------
# Merge type_name mapping (year-aware)
# ---------------------------------------------------

print("Loading type_name key from:", type_key_path)

type_key = pd.read_csv(type_key_path)
type_key.columns = type_key.columns.str.strip()

# Merge on (year, type_name)
df = df.merge(
    type_key[["year", "type_name", "type_name_s"]],
    on=["year", "type_name"],
    how="left"
)

# Safely replace numeric type_name with readable label
df["type_name"] = df["type_name_s"].fillna(df["type_name"].astype(str))

df.drop(columns=["type_name_s"], inplace=True)

print("Merged type_name labels.")
print("Missing mapped type_name values:", df["type_name"].isna().sum())

# ---------------------------------------------------
# Optional sampling for ML speed
# ---------------------------------------------------

if len(df) > 200000:
    df = df.sample(n=200000, random_state=42)
    print("Sampled dataset for ML:", df.shape)

# ---------------------------------------------------
# Save processed dataset
# ---------------------------------------------------

df.to_csv(processed_path, index=False)
# Replace unclear gender categories with NaN
gender_cols = [
    "female_defendant",
    "female_petitioner",
    "female_adv_def",
    "female_adv_pet"
]

for col in gender_cols:
    df[col] = df[col].replace("-9998 unclear", pd.NA)
print("Final dataset shape:", df.shape)
print("Cleaned dataset saved successfully at:", processed_path)
