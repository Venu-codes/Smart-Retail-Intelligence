
from pathlib import Path
import pandas as pd

# Locate the project and cleaned dataset
project_folder = Path(__file__).resolve().parent.parent

file_path = (
    project_folder / "data" / "online_retail_cleaned.csv"
)

# Load the cleaned dataset
df = pd.read_csv(file_path)

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Identify cancelled invoices
df["InvoiceNo"] = df["InvoiceNo"].astype(str)

df["IsCancelled"] = df["InvoiceNo"].str.startswith("C")

# Identify return/negative quantity records
df["IsReturn"] = df["Quantity"] < 0

# Summarize transaction records
print("\n--- DATASET SUMMARY ---")
print("Total rows:", len(df))

print("\n--- CANCELLED INVOICE ANALYSIS ---")
print("Cancelled rows:", df["IsCancelled"].sum())
print(
    "Unique cancelled invoices:",
    df.loc[df["IsCancelled"], "InvoiceNo"].nunique()
)

print("\n--- RETURN ANALYSIS ---")
print("Rows with negative quantity:", df["IsReturn"].sum())

print(
    "Unique invoices with negative quantity:",
    df.loc[df["IsReturn"], "InvoiceNo"].nunique()
)

print("\n--- REVENUE IMPACT ---")
print(
    "Revenue from negative-quantity rows:",
    round(df.loc[df["IsReturn"], "Revenue"].sum(), 2)
)

print(
    "Revenue from positive-quantity rows:",
    round(df.loc[df["Quantity"] > 0, "Revenue"].sum(), 2)
)

print("\n--- SAMPLE RETURN RECORDS ---")
print(
    df.loc[
        df["IsReturn"],
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "Revenue"]
    ].head(10)
)
