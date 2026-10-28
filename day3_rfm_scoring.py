
from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent

input_file = project_folder / "data" / "rfm_base.csv"
df = pd.read_csv(input_file)

# Assign scores from 1 to 5
# Lower Recency is better, so reverse its score
df["R_Score"] = pd.qcut(
    df["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

df["F_Score"] = pd.qcut(
    df["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

df["M_Score"] = pd.qcut(
    df["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Combined RFM score
df["RFM_Score"] = (
    df["R_Score"].astype(str)
    + df["F_Score"].astype(str)
    + df["M_Score"].astype(str)
)

output_file = project_folder / "data" / "rfm_scored.csv"
df.to_csv(output_file, index=False)

print("RFM Scoring Preview:")
print(
    df[[
        "CustomerID", "Recency", "Frequency", "Monetary",
        "R_Score", "F_Score", "M_Score", "RFM_Score"
    ]].head(10).to_string(index=False)
)

print("\nTotal customers scored:", len(df))
print("Missing values:\n", df.isnull().sum())
print("\nSaved to:", output_file)
