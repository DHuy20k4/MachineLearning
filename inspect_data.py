
from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/raw/Dry_Bean_Dataset.csv")

# Doc du lieu
df = pd.read_csv(DATA_PATH)

print("=" * 50)
print("1. KICH THUOC DU LIEU")
print("=" * 50)
print(f"So dong: {df.shape[0]}")
print(f"So cot: {df.shape[1]}")

print("\n" + "=" * 50)
print("2. KIEU DU LIEU")
print("=" * 50)
print(df.dtypes)

print("\n" + "=" * 50)
print("3. GIA TRI THIEU")
print("=" * 50)
print(df.isnull().sum())

print("\nTong gia tri thieu:", df.isnull().sum().sum())

print("\n" + "=" * 50)
print("4. SO DONG TRUNG LAP")
print("=" * 50)
print("So dong trung lap:", df.duplicated().sum())

print("\n" + "=" * 50)
print("5. PHAN BO CAC GIONG DAU")
print("=" * 50)
print(df["Class"].value_counts())

print("\nTy le phan tram (%):")
print((df["Class"].value_counts(normalize=True) * 100).round(2))

print("\n" + "=" * 50)
print("6. THONG KE CAC DAC TRUNG")
print("=" * 50)
print(df.describe().round(2).T)

print("\nDa hoan thanh kiem tra du lieu.")

