
from pathlib import Path
import pandas as pd

cm = pd.read_csv(
    Path("results") / "confusion_matrix.csv",
    index_col=0,
)

# Các hàng là nhãn thật, các cột là nhãn dự đoán.
# Bỏ các trường hợp dự đoán đúng trên đường chéo.
errors = []

for i in range(len(cm.index)):
    for j in range(i + 1, len(cm.columns)):
        class_a = cm.index[i]
        class_b = cm.columns[j]

        # A bị đoán thành B
        a_to_b = int(cm.loc[class_a, class_b])

        # B bị đoán thành A
        b_to_a = int(cm.loc[class_b, class_a])

        errors.append({
            "Class A": class_a,
            "Class B": class_b,
            "A predicted as B": a_to_b,
            "B predicted as A": b_to_a,
            "Total confusion": a_to_b + b_to_a,
        })

result = pd.DataFrame(errors)
result = result.sort_values(
    "Total confusion",
    ascending=False,
)

print("===== CAC CAP GIONG DAU DE BI NHAM NHAT =====")
print(result.head(10).to_string(index=False))

result.to_csv(
    Path("results") / "confused_class_pairs.csv",
    index=False,
)

print("\nDa luu: results/confused_class_pairs.csv")

