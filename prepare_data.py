
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42

RAW_PATH = Path("data/raw/Dry_Bean_Dataset.csv")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Doc du lieu goc
df = pd.read_csv(RAW_PATH)

print("So dong ban dau:", len(df))

# 2. Loai bo cac dong trung lap hoan toan
duplicate_count = int(df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)

print("So dong trung lap da loai:", duplicate_count)
print("So dong sau xu ly:", len(df))

# 3. Tach dac trung va nhan lop
X = df.drop(columns=["Class"])
y = df["Class"]

# 4. Tach 15% lam tap test
X_train_val, X_test, y_train_val, y_test = train_test_split(
    X,
    y,
    test_size=0.15,
    random_state=RANDOM_STATE,
    stratify=y,
)

# 5. Tach 15% tong du lieu lam validation
# 0.15 / 0.85 = ti le validation trong phan con lai
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val,
    y_train_val,
    test_size=0.15 / 0.85,
    random_state=RANDOM_STATE,
    stratify=y_train_val,
)

# 6. Luu tung tap, kem nhan Class
train_df = X_train.copy()
train_df["Class"] = y_train

val_df = X_val.copy()
val_df["Class"] = y_val

test_df = X_test.copy()
test_df["Class"] = y_test

train_df.to_csv(OUTPUT_DIR / "train.csv", index=False)
val_df.to_csv(OUTPUT_DIR / "validation.csv", index=False)
test_df.to_csv(OUTPUT_DIR / "test.csv", index=False)

print("\nDa chia du lieu thanh cong!")
print(f"Train:      {len(train_df)} mau ({len(train_df) / len(df):.1%})")
print(f"Validation: {len(val_df)} mau ({len(val_df) / len(df):.1%})")
print(f"Test:       {len(test_df)} mau ({len(test_df) / len(df):.1%})")

print("\nPhan bo lop trong tap train:")
print(train_df["Class"].value_counts())

print("\nDa luu du lieu tai:", OUTPUT_DIR)
