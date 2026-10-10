
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import f1_score
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

results = []

for k in range(1, 32):
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(
            n_neighbors=k,
            weights="distance",
            metric="minkowski",
            p=2,
            n_jobs=-1,
        )),
    ])

    model.fit(X_train, y_train)
    predictions = model.predict(X_val)

    macro_f1 = f1_score(
        y_val,
        predictions,
        average="macro",
    )

    results.append({
        "K": k,
        "Macro_F1": macro_f1,
    })

    print(f"K={k:2d} | Macro-F1={macro_f1:.4f}")

results_df = pd.DataFrame(results)
results_df.to_csv(RESULT_DIR / "k_tuning_results.csv", index=False)

best_row = results_df.loc[results_df["Macro_F1"].idxmax()]
best_k = int(best_row["K"])

plt.figure(figsize=(10, 6))
plt.plot(
    results_df["K"],
    results_df["Macro_F1"],
    marker="o",
)
plt.xticks(range(1, 32, 2))
plt.xlabel("Number of Neighbors (K)")
plt.ylabel("Macro-F1")
plt.title("KNN Hyperparameter Tuning on Validation Set")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RESULT_DIR / "k_tuning.png", dpi=150)
plt.show()

print("\n===== K TOT NHAT TREN VALIDATION =====")
print(f"K tot nhat: {best_k}")
print(f"Macro-F1:   {best_row['Macro_F1']:.4f}")
print("Da luu: results/k_tuning_results.csv")
print("Da luu: results/k_tuning.png")
