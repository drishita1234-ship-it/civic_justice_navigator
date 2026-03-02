import joblib
import os
import pandas as pd
import numpy as np
# Load model once at startup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "models", "timeline_model.pkl")

model = joblib.load(model_path)

def predict_case_duration(input_dict):

    required_features = [
        "year",
        "state_code",
        "dist_code",
        "court_no",
        "type_name"
    ]

    filtered_input = {k: input_dict[k] for k in required_features}

    input_df = pd.DataFrame([filtered_input])

    # -----------------------------
    # Make Prediction
    # -----------------------------
    prediction = model.predict(input_df)[0]

    years = prediction / 365

    if years < 1.5:
        risk_level = "Low Duration Risk"
    elif years < 3:
        risk_level = "Moderate Duration Risk"
    else:
        risk_level = "High Duration Risk"

    # -----------------------------
    # Feature Importance
    # -----------------------------
    regressor = model.named_steps["regressor"]
    feature_names = model.named_steps["preprocessor"].get_feature_names_out()
    importances = regressor.feature_importances_

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    }).sort_values(by="importance", ascending=False)

    top_features_raw = importance_df.head(5)["feature"].tolist()

    top_features_clean = []
    for f in top_features_raw:
        cleaned = (
            f.replace("cat__", "")
             .replace("num__", "")
             .replace("type_name_", "")
             .replace("_", " ")
        )
        top_features_clean.append(cleaned)

    # -----------------------------
    # Return Final Structured JSON
    # -----------------------------
    return {
        "predicted_duration_days": float(round(prediction, 2)),
        "predicted_duration_years": float(round(years, 2)),
        "risk_level": risk_level,
        "key_influencing_factors": top_features_clean
    }