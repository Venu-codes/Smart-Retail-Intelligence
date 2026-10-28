
from pathlib import Path
import pandas as pd

# Load cleaned dataset
project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "online_retail_cleaned.csv"

df = pd.read_csv(file_path)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Separate normal sales from cancellation/return rows
sales_df = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0) &
    (~df["InvoiceNo"].astype(str).str.startswith("C"))
].copy()

# Create monthly analysis columns
sales_df["YearMonth"] = sales_df["InvoiceDate"].dt.to_period("M").astype(str)
sales_df["Revenue"] = sales_df["Quantity"] * sales_df["UnitPrice"]

# Aggregate monthly revenue
monthly_revenue = (
    sales_df.groupby("YearMonth", as_index=False)
    .agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Transactions=("InvoiceNo", "nunique"),
        Unique_Customers=("CustomerID", "nunique")
    )
    .sort_values("YearMonth")
)

print("\n--- MONTHLY REVENUE ANALYSIS ---")
print(monthly_revenue.round(2).to_string(index=False))

# Save result for future SQL and Power BI analysis
output_path = project_folder / "data" / "monthly_revenue.csv"
monthly_revenue.to_csv(output_path, index=False)

print("\nSaved file:", output_path)
print("File exists:", output_path.exists())
