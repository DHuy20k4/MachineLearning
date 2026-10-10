
from pathlib import Path

import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)

DATA_DIR = Path("data/processed")
RESULT_DIR = Path("results")
MODEL_DIR = Path("models")

RESULT_DIR.mkdir(parents=True, exist_ok=True)

train_df = pd.read_csv(DATA_DIR / "train.csv")
val_df = pd.read_csv(DATA_DIR / "validation.csv")
test_df = pd.read_csv(DATA_DIR / "test.csv")

# Chọn K tốt nhất từ validation.
# Fit lại trên train + validation sau khi đã hoàn tất lựa chọn.
train_val_df = pd.concat(
    [train_df, val_df],
    ignore_index=True,
)

X_train_val = train_val_df.drop(columns=["Class"])
y_train_val = train_val_df["Class"]

X_test = test_df.drop(columns=["Class"])
y_test = test_df["Class"]

# Dùng đúng cấu hình đã chọn:
# StandardScaler + KNN, K=18, Euclidean, distance weighting.
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

model = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(
        n_neighbors=18,
        weights="distance",
        metric="minkowski",
        p=2,
        n_jobs=-1,
    )),
])

model.fit(X_train_val, y_train_val)
predictions = model.predict(X_test)

print("===== KET QUA DANH GIA CUOI CUNG =====")
print(f"Accuracy:          {accuracy_score(y_test, predictions):.4f}")
print(f"Macro-F1:          {f1_score(y_test, predictions, average='macro'):.4f}")
print(f"Balanced Accuracy: {balanced_accuracy_score(y_test, predictions):.4f}")

print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(y_test, predictions, digits=4))

labels = sorted(y_test.unique())
cm = confusion_matrix(y_test, predictions, labels=labels)

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels,
)
cm_df.to_csv(RESULT_DIR / "confusion_matrix.csv")

plt.figure(figsize=(10, 8))
sns.heatmap(
    cm_df,
    annot=True,
    fmt="d",
    cmap="Blues",
)
plt.title("Confusion Matrix - Dry Bean KNN")
plt.xlabel("Predicted Class")
plt.ylabel("True Class")
plt.tight_layout()
plt.savefig(RESULT_DIR / "confusion_matrix.png", dpi=150)
plt.show()

# Lưu mô hình cuối để dùng khi xây dựng API.
joblib.dump(model, MODEL_DIR / "dry_bean_knn.joblib")

print("\nDa luu:")
print("- results/confusion_matrix.csv")
print("- results/confusion_matrix.png")
print("- models/dry_bean_knn.joblib")
