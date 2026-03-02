from flask import Flask, request, jsonify
from flask_cors import CORS
from prediction.predict_timeline import predict_case_duration

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Civic Justice Navigator API is running."


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    print("Incoming data:", data)

    result = predict_case_duration(data)

    print("Result:", result)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)