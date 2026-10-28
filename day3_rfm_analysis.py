
from pathlib import Path
import pandas as pd

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Load the Day 2 customer summary
input_file = project_folder / "data" / "customer_summary.csv"
df = pd.read_csv(input_file)

# Convert purchase date into datetime
df["Last_Purchase"] = pd.to_datetime(df["Last_Purchase"])

# Use the day after the latest purchase as the analysis date
snapshot_date = df["Last_Purchase"].max() + pd.Timedelta(days=1)

# Create the RFM dataset
rfm = pd.DataFrame({
    "CustomerID": df["CustomerID"],
    "Recency": (snapshot_date - df["Last_Purchase"]).dt.days,
    "Frequency": df["Total_Orders"],
    "Monetary": df["Total_Revenue"]
})

# Sort customers by total spending
rfm = rfm.sort_values("Monetary", ascending=False)

# Save the output
output_file = project_folder / "data" / "rfm_base.csv"
rfm.to_csv(output_file, index=False)

# Display results
print("Analysis Date:", snapshot_date.date())
print("\nRFM Dataset Preview:")
print(rfm.head(10).to_string(index=False))

print("\n--- Validation ---")
print("Total customers:", len(rfm))
print("Missing values:\n", rfm.isnull().sum())
print("Duplicate CustomerIDs:", rfm["CustomerID"].duplicated().sum())
print("Output saved to:", output_file)
