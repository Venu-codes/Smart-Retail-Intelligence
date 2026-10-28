
from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "online_retail_cleaned.csv"

df = pd.read_csv(file_path)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["InvoiceNo"] = df["InvoiceNo"].astype(str)

# Keep valid positive sales; exclude cancellations and returns
sales_df = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0) &
    (~df["InvoiceNo"].str.startswith("C"))
].copy()

sales_df["Revenue"] = (
    sales_df["Quantity"] * sales_df["UnitPrice"]
)

# Aggregate transactions by customer
customer_summary = (
    sales_df.groupby("CustomerID", as_index=False)
    .agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Orders=("InvoiceNo", "nunique"),
        Total_Quantity=("Quantity", "sum"),
        First_Purchase=("InvoiceDate", "min"),
        Last_Purchase=("InvoiceDate", "max")
    )
)

# Average order value
customer_summary["Average_Order_Value"] = (
    customer_summary["Total_Revenue"] /
    customer_summary["Total_Orders"]
)

# Rank customers by revenue
customer_summary = customer_summary.sort_values(
    "Total_Revenue", ascending=False
)

print("\n--- CUSTOMER SUMMARY ---")
print("Unique customers:", len(customer_summary))

print("\n--- TOP 10 CUSTOMERS BY REVENUE ---")
print(customer_summary.head(10).round(2).to_string(index=False))

output_path = project_folder / "data" / "customer_summary.csv"
customer_summary.to_csv(output_path, index=False)

print("\nSaved file:", output_path)
print("File exists:", output_path.exists())


# STEP 5: VERIFY DAY 2 OUTPUT FILES

print("\n--- DAY 2 OUTPUT FILE CHECK ---")

files_to_check = [
    "online_retail_cleaned.csv",
    "monthly_revenue.csv",
    "top_products.csv",
    "customer_summary.csv"
]

for filename in files_to_check:
    output_file = project_folder / "data" / filename

    print(
        filename,
        "| Exists:", output_file.exists(),
        "| Size:", output_file.stat().st_size if output_file.exists() else 0
    )

print("\n--- CUSTOMER SUMMARY VALIDATION ---")
print("Unique customers:", customer_summary["CustomerID"].nunique())
print("Duplicate customer IDs:", customer_summary["CustomerID"].duplicated().sum())
print("Missing CustomerIDs:", customer_summary["CustomerID"].isnull().sum())
