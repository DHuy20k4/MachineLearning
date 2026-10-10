
from pathlib import Path

import pandas as pd
import joblib

from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DATA_DIR = Path("data/processed")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Doc train va validation
train_df = pd.read_csv(DATA_DIR / "train.csv")
val_df = pd.read_csv(DATA_DIR / "validation.csv")

X_train = train_df.drop(columns=["Class"])
y_train = train_df["Class"]

X_val = val_df.drop(columns=["Class"])
y_val = val_df["Class"]


def evaluate_model(name, model, X, y):
    predictions = model.predict(X)

    accuracy = accuracy_score(y, predictions)
    macro_f1 = f1_score(y, predictions, average="macro")
    balanced_acc = balanced_accuracy_score(y, predictions)

    print(f"\n{name}")
    print("-" * 40)
    print(f"Accuracy:          {accuracy:.4f}")
    print(f"Macro-F1:          {macro_f1:.4f}")
    print(f"Balanced Accuracy: {balanced_acc:.4f}")

    return {
        "model": name,
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "balanced_accuracy": balanced_acc,
    }


results = []

# 1. Baseline
baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)

results.append(
    evaluate_model("Baseline - Most Frequent", baseline, X_val, y_val)
)

# 2. k-NN chua chuan hoa
knn_raw = KNeighborsClassifier(
    n_neighbors=5,
    weights="distance",
    metric="minkowski",
    p=2,
    n_jobs=-1,
)
knn_raw.fit(X_train, y_train)

results.append(
    evaluate_model("KNN - Unscaled (K=5)", knn_raw, X_val, y_val)
)

# 3. k-NN co chuan hoa
knn_scaled = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(
        n_neighbors=5,
        weights="distance",
        metric="minkowski",
        p=2,
        n_jobs=-1,
    )),
])

knn_scaled.fit(X_train, y_train)

results.append(
    evaluate_model("KNN - StandardScaler (K=5)", knn_scaled, X_val, y_val)
)

# Luu pipeline da chuan hoa de tiep tuc thu nghiem
joblib.dump(knn_scaled, MODEL_DIR / "knn_scaled_baseline.joblib")

# Luu ket qua validation
results_df = pd.DataFrame(results)
results_df.to_csv("validation_results.csv", index=False)

print("\n" + "=" * 50)
print("DA HOAN THANH THU NGHIEM BAN DAU")
print("Model da luu: models/knn_scaled_baseline.joblib")
print("Ket qua da luu: validation_results.csv")
print("=" * 50)
