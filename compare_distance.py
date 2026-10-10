
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    f1_score,
    balanced_accuracy_score,
    accuracy_score,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DATA_DIR = Path("data/processed")
RESULT_DIR = Path("results")
RESULT_DIR.mkdir(parents=True, exist_ok=True)

train_df = pd.read_csv(DATA_DIR / "train.csv")
val_df = pd.read_csv(DATA_DIR / "validation.csv")

X_train = train_df.drop(columns=["Class"])
y_train = train_df["Class"]
X_val = val_df.drop(columns=["Class"])
y_val = val_df["Class"]

# So sánh khoảng cách tại K=18 đã chọn từ bước trước.
results = []

for metric_name, p in [
    ("Euclidean", 2),
    ("Manhattan", 1),
]:
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(
            n_neighbors=18,
            weights="distance",
            metric="minkowski",
            p=p,
            n_jobs=-1,
        )),
    ])

    model.fit(X_train, y_train)
    predictions = model.predict(X_val)

    row = {
        "Distance": metric_name,
        "K": 18,
        "Accuracy": accuracy_score(y_val, predictions),
        "Macro_F1": f1_score(
            y_val, predictions, average="macro"
        ),
        "Balanced_Accuracy": balanced_accuracy_score(
            y_val, predictions
        ),
    }
    results.append(row)

    print(f"\n{metric_name}")
    print("-" * 35)
    print(f"Accuracy:          {row['Accuracy']:.4f}")
    print(f"Macro-F1:          {row['Macro_F1']:.4f}")
    print(f"Balanced Accuracy: {row['Balanced_Accuracy']:.4f}")

results_df = pd.DataFrame(results)
results_df.to_csv(
    RESULT_DIR / "distance_comparison.csv",
    index=False,
)

print("\nDa luu: results/distance_comparison.csv")
