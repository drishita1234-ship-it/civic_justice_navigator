import pandas as pd
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_cases.csv")

df = pd.read_csv(file_path)

categories = {
    "judge_position": sorted(df["judge_position"].dropna().unique().tolist()),
    "type_name": sorted(df["type_name"].dropna().unique().tolist())
}

output_path = os.path.join(BASE_DIR, "frontend", "src", "categories.json")

with open(output_path, "w") as f:
    json.dump(categories, f, indent=4)

print("Categories exported.")