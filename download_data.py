
from pathlib import Path
from ucimlrepo import fetch_ucirepo

# Thu muc luu du lieu goc
DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

print("Dang tai bo du lieu Dry Bean...")

# Dry Bean co ma dataset UCI la 602
dry_bean = fetch_ucirepo(id=602)

# Ket hop dac trung va nhan lop
X = dry_bean.data.features
y = dry_bean.data.targets

import pandas as pd

df = X.copy()
df["Class"] = y.iloc[:, 0].values

output_path = DATA_DIR / "Dry_Bean_Dataset.csv"
df.to_csv(output_path, index=False)

print("\nTai du lieu thanh cong!")
print("Kich thuoc:", df.shape)
print("So dac trung:", X.shape[1])
print("So giong dau:", y.iloc[:, 0].nunique())
print("Cac giong dau:")
print(y.iloc[:, 0].value_counts())
print("\nDa luu tai:", output_path)
