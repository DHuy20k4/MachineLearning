
from pathlib import Path

import joblib
from flask import Flask, jsonify

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "dry_bean_knn.joblib"

model = joblib.load(MODEL_PATH)


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    from app.routes import api
    app.register_blueprint(api)

    from flask import render_template

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/predict", methods=["GET"])
    def predict_page():
        return render_template("predict.html")

    @app.route("/evaluation", methods=["GET"])
    def evaluation_page():
        return render_template("evaluation.html")
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "model_loaded": True,
            "features": int(model.n_features_in_),
        })

    return app
