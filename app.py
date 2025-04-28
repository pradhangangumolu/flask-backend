from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS  # Add this to handle CORS issues

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load models and scaler (make sure your .pkl files are correct paths)
rul_model = pickle.load(open("rul_model.pkl", "rb"))
clf_model = pickle.load(open("failure_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

@app.route("/", methods=["GET"])
def home():
    return "<h2>Welcome to the Predictive Maintenance API</h2><p>Use the <code>/predict</code> route to send POST requests with sensor data.</p>"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Example: Process input data (adjust this based on how your model works)
    features = [
        data.get("op_setting_1", 0),
        data.get("op_setting_2", 0),
        data.get("op_setting_3", 0)
    ] + [
        data.get(f"sensor_measurement_{i}", 0) for i in range(1, 22)
    ]
    features = np.array(features).reshape(1, -1)
    features_scaled = scaler.transform(features)

    # Make predictions
    predicted_rul = rul_model.predict(features_scaled)[0]
    failure_type = clf_model.predict(features_scaled)[0]

    return jsonify({
        "failure_type": failure_type,
        "predicted_rul": round(predicted_rul, 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)