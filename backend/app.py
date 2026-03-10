import sys
import os

# Allow Python to access project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS

from prediction.predict_timeline import predict_case_duration
from nlp.process_query import process_user_query
from backend.adr_recommendation import recommend_resolution


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Civic Justice Navigator API is running."


@app.route("/predict", methods=["POST"])
def predict():

    # Get incoming JSON data
    data = request.get_json()

    # Extract user query
    user_query = data.get("query")

    # Extract case features
    case_features = data.get("features")

    # -------------------------
    # NLP Processing
    # -------------------------
    nlp_output = process_user_query(user_query)

    # -------------------------
    # ML Prediction
    # -------------------------
    prediction = predict_case_duration(case_features)

    # -------------------------
    # ADR Recommendation
    # -------------------------
    adr_advice = recommend_resolution(case_features["type_name"])

    # -------------------------
    # Citizen Friendly Message
    # -------------------------
    years = prediction["predicted_duration_years"]
    risk = prediction["risk_level"]

    citizen_message = (
        f"Your case may take approximately {years} years in court. "
        f"The risk of delay is {risk.lower()}."
    )

    # -------------------------
    # Final Response
    # -------------------------
    return jsonify({
        "query_language": nlp_output["language"],
        "translated_query": nlp_output["translated"],
        "simplified_query": nlp_output["simplified"],
        "prediction": prediction,
        "adr_recommendation": adr_advice,
        "citizen_message": citizen_message
    })


if __name__ == "__main__":
    app.run(debug=True)