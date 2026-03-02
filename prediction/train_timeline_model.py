import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import numpy as np

# Load processed dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_cases.csv")

df = pd.read_csv(file_path)

print("Loaded dataset:", df.shape)

# Sample for faster experimentation (still strong size)
if len(df) > 100000:
    df = df.sample(n=100000, random_state=42)
    print("Sampled dataset:", df.shape)

# ---------------------------------------------------
# Feature Selection
# ---------------------------------------------------

features = [
    "year",
    "state_code",
    "dist_code",
    "court_no",
    "type_name"
]

X = df[features]
y = df["case_duration_days"]

# ---------------------------------------------------
# Train-Test Split
# ---------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Identify column types
categorical_cols = ["type_name"]
numeric_cols = ["year", "state_code", "dist_code", "court_no"]

# ---------------------------------------------------
# Preprocessing Pipelines
# ---------------------------------------------------

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", categorical_transformer, categorical_cols),
        ("num", numeric_transformer, numeric_cols)
    ]
)
# Model Pipeline
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=30,
        random_state=42,
        n_jobs=-1
    ))
])

# ---------------------------------------------------
# Train Model
# ---------------------------------------------------

print("Training model...")
model.fit(X_train, y_train)

# ---------------------------------------------------
# Evaluate Model
# ---------------------------------------------------

print("Evaluating model...")
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\nModel Performance:")
print("MAE (days):", round(mae, 2))
print("RMSE (days):", round(rmse, 2))

# ---------------------------------------------------
# Save Model
# ---------------------------------------------------

model_path = os.path.join(BASE_DIR, "models", "timeline_model.pkl")
joblib.dump(model, model_path)

print("\nModel saved successfully at:", model_path)
regressor = model.named_steps["regressor"]

feature_names = model.named_steps["preprocessor"].get_feature_names_out()

importances = regressor.feature_importances_

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

print("\nTop 15 Important Features:")
print(importance_df.head(15))