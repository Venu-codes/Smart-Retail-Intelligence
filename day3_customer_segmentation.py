
from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent

input_file = project_folder / "data" / "rfm_scored.csv"
df = pd.read_csv(input_file)

def segment_customer(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "High-Value Customer"
    elif f >= 4 and r >= 3:
        return "Loyal Customer"
    elif r >= 4 and f >= 2:
        return "Potential Loyalist"
    elif r <= 2 and f >= 2:
        return "At-Risk Customer"
    else:
        return "Other Customers"

df["Customer_Segment"] = df.apply(segment_customer, axis=1)

output_file = project_folder / "data" / "rfm_customer_segments.csv"
df.to_csv(output_file, index=False)

print("Customer Segment Summary:")
print(df["Customer_Segment"].value_counts().to_string())

print("\nCustomer Examples:")
print(
    df[[
        "CustomerID", "Recency", "Frequency",
        "Monetary", "RFM_Score", "Customer_Segment"
    ]].head(10).to_string(index=False)
)

print("\nTotal customers:", len(df))
print("Missing segment values:", df["Customer_Segment"].isnull().sum())
print("Saved to:", output_file)
