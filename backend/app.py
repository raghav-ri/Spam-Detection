from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)
CORS(app)

# -------- SAFE MODEL LOADING --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "spam_model.pkl")

model = pickle.load(open(MODEL_PATH, "rb"))
# -----------------------------------

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    message = data.get("message", "")

    prediction = model.predict([message])[0]

    return jsonify({
        "prediction": "Spam" if prediction == 1 else "Not Spam"
    })

if __name__ == "__main__":
    app.run(debug=True)
