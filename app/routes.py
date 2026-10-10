
from flask import Blueprint, jsonify, request
import pandas as pd

api = Blueprint("api", __name__)


FEATURES = [
    "Area",
    "Perimeter",
    "MajorAxisLength",
    "MinorAxisLength",
    "AspectRatio",
    "Eccentricity",
    "ConvexArea",
    "EquivDiameter",
    "Extent",
    "Solidity",
    "Roundness",
    "Compactness",
    "ShapeFactor1",
    "ShapeFactor2",
    "ShapeFactor3",
    "ShapeFactor4",
]


def get_model():
    from app import model
    return model


@api.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body phải là JSON object."
        }), 400

    missing = [name for name in FEATURES if name not in data]
    if missing:
        return jsonify({
            "error": "Thiếu đặc trưng đầu vào.",
            "missing_features": missing,
        }), 400

    try:
        values = {}
        for name in FEATURES:
            value = data[name]

            if isinstance(value, bool):
                raise ValueError(f"{name} phải là số.")

            values[name] = float(value)

            if not pd.notna(values[name]):
                raise ValueError(f"{name} phải là số hữu hạn.")

            import math
            if not math.isfinite(values[name]):
                raise ValueError(f"{name} phải là số hữu hạn.")

            if values[name] <= 0:
                raise ValueError(f"{name} phải lớn hơn 0.")

    except (TypeError, ValueError) as exc:
        return jsonify({
            "error": "Dữ liệu đầu vào không hợp lệ.",
            "details": str(exc),
        }), 400

    X = pd.DataFrame([values], columns=FEATURES)
    model = get_model()

    prediction = str(model.predict(X)[0])
    probabilities = model.predict_proba(X)[0]
    classes = model.named_steps["knn"].classes_

    probability_result = {
        str(label): round(float(prob), 4)
        for label, prob in zip(classes, probabilities)
    }

    return jsonify({
        "prediction": prediction,
        "probabilities": probability_result,
        "model": "KNN",
    })


@api.route("/api/predict-batch", methods=["POST"])
def predict_batch():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not isinstance(data.get("samples"), list):
        return jsonify({
            "error": "Request body phải có dạng {'samples': [...]}"
        }), 400

    samples = data["samples"]

    if not samples:
        return jsonify({"error": "Danh sách samples không được rỗng."}), 400

    if len(samples) > 100:
        return jsonify({
            "error": "Mỗi lần chỉ được dự đoán tối đa 100 mẫu."
        }), 400

    model = get_model()
    rows = []

    for index, sample in enumerate(samples):
        if not isinstance(sample, dict):
            return jsonify({
                "error": f"Mẫu thứ {index + 1} phải là JSON object."
            }), 400

        missing = [name for name in FEATURES if name not in sample]
        if missing:
            return jsonify({
                "error": f"Mẫu thứ {index + 1} thiếu đặc trưng.",
                "missing_features": missing,
            }), 400

        try:
            import math

            row = {}
            for name in FEATURES:
                value = sample[name]

                if isinstance(value, bool):
                    raise ValueError(f"{name} phải là số.")

                value = float(value)

                if not math.isfinite(value) or value <= 0:
                    raise ValueError(f"{name} phải là số hữu hạn lớn hơn 0.")

                row[name] = value

            rows.append(row)

        except (TypeError, ValueError) as exc:
            return jsonify({
                "error": f"Dữ liệu mẫu thứ {index + 1} không hợp lệ.",
                "details": str(exc),
            }), 400

    X = pd.DataFrame(rows, columns=FEATURES)
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    classes = model.named_steps["knn"].classes_

    results = []

    for prediction, probs in zip(predictions, probabilities):
        results.append({
            "prediction": str(prediction),
            "probabilities": {
                str(label): round(float(prob), 4)
                for label, prob in zip(classes, probs)
            },
        })

    return jsonify({
        "count": len(results),
        "results": results,
        "model": "KNN",
    })
