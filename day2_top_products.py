
from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "online_retail_cleaned.csv"

df = pd.read_csv(file_path)

# Exclude cancellations, returns and invalid prices
sales_df = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0) &
    (~df["InvoiceNo"].astype(str).str.startswith("C"))
].copy()

# Calculate sales revenue
sales_df["Revenue"] = (
    sales_df["Quantity"] * sales_df["UnitPrice"]
)

# Aggregate product-level performance
top_products = (
    sales_df.groupby(["StockCode", "Description"], as_index=False)
    .agg(
        Total_Quantity_Sold=("Quantity", "sum"),
        Total_Revenue=("Revenue", "sum"),
        Total_Transactions=("InvoiceNo", "nunique")
    )
    .sort_values("Total_Quantity_Sold", ascending=False)
    .head(10)
)

print("\n--- TOP 10 PRODUCTS BY QUANTITY SOLD ---")
print(top_products.round(2).to_string(index=False))

output_path = project_folder / "data" / "top_products.csv"
top_products.to_csv(output_path, index=False)

print("\nSaved file:", output_path)
print("File exists:", output_path.exists())
