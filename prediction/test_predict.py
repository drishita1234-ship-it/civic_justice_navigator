from predict_timeline import predict_case_duration

sample_input = {
    "year": 2015,
    "state_code": 33,
    "dist_code": 1,
    "court_no": 1,
    "judge_position": "metropolitan magistrate court",
    "female_defendant": 0,
    "female_petitioner": 1,
    "female_adv_def": 0,
    "female_adv_pet": 1,
    "type_name": "04 criminal case"
}

result = predict_case_duration(sample_input)

print("Prediction Result:")
print(result)

print("\nPredicted Duration (days):", result["predicted_duration_days"])
print("Predicted Duration (years):", result["predicted_duration_years"])
print("Risk Level:", result["risk_level"])
print("Key Influencing Factors:", result["key_influencing_factors"])