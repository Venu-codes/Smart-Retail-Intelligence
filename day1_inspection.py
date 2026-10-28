'''import pandas as pd

print("Pandas version:", pd.__version__)
print("Project setup successful!")
from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "Online Retail.xlsx"

df = pd.read_excel(file_path)

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())'''

from pathlib import Path
import pandas as pd

# Locate the Excel dataset
project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "Online Retail.xlsx"

# Check whether the file exists
if not file_path.exists():
    print("ERROR: Excel file not found:", file_path)
else:
    df = pd.read_excel(file_path)

    print("\n--- DATASET PREVIEW ---")
    print(df.head())

    print("\n--- DATASET SIZE ---")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\n--- COLUMN NAMES ---")
    print(df.columns.tolist())

    print("\n--- DATA TYPES ---")
    print(df.dtypes)

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

    print("\n--- DUPLICATE ROWS ---")
    print(df.duplicated().sum())

    print("\n--- BASIC STATISTICS ---")
    print(df.describe(include="all"))

print("\n--- NEGATIVE OR ZERO QUANTITY ---")
print((df["Quantity"] <= 0).sum())

print("\n--- ZERO OR NEGATIVE UNIT PRICE ---")
print((df["UnitPrice"] <= 0).sum())

print("\n--- CANCELLED INVOICES ---")
print(df["InvoiceNo"].astype(str).str.startswith("C").sum())

print("\n--- DATE RANGE ---")
print("Start:", df["InvoiceDate"].min())
print("End:", df["InvoiceDate"].max())

print("\n--- UNIQUE CUSTOMERS ---")
print(df["CustomerID"].nunique())

print("\n--- DATA QUALITY SUMMARY ---")

print("Total rows:", len(df))
print("Missing CustomerID:", df["CustomerID"].isnull().sum())
print("Missing Description:", df["Description"].isnull().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Invalid quantities:", (df["Quantity"] <= 0).sum())
print("Invalid prices:", (df["UnitPrice"] <= 0).sum())

print("\n--- SAMPLE NEGATIVE QUANTITY RECORDS ---")
print(df[df["Quantity"] < 0].head(5))

print("\n--- SAMPLE ZERO PRICE RECORDS ---")
print(df[df["UnitPrice"] <= 0].head(5))


# STEP 6: DATA CLEANING

# 1. Create a copy of the original dataset
clean_df = df.copy()

print("\n--- BEFORE CLEANING ---")
print("Original rows:", len(clean_df))

# 2. Remove exact duplicate rows
clean_df = clean_df.drop_duplicates()

# 3. Remove rows with missing CustomerID
clean_df = clean_df.dropna(subset=["CustomerID"])

# 4. Remove rows with missing Description
clean_df = clean_df.dropna(subset=["Description"])

# 5. Create a Revenue column
clean_df["Revenue"] = (
    clean_df["Quantity"] * clean_df["UnitPrice"]
)

# 6. Save cleaned data as a separate CSV file
output_path = (
    project_folder / "data" / "online_retail_cleaned.csv"
)

clean_df.to_csv(output_path, index=False)

# 7. Display cleaning results
print("\n--- AFTER CLEANING ---")
print("Cleaned rows:", len(clean_df))
print("Rows removed:", len(df) - len(clean_df))

print("\n--- MISSING VALUES AFTER CLEANING ---")
print(
    clean_df[["CustomerID", "Description"]]
    .isnull()
    .sum()
)

print("\n--- REVENUE SAMPLE ---")
print(
    clean_df[
        ["InvoiceNo", "Quantity", "UnitPrice", "Revenue"]
    ].head()
)

print("\nCleaned file saved at:", output_path)
print("File exists:", output_path.exists())


# STEP 7: VALIDATE CLEANED DATA

check_df = pd.read_csv(output_path)

print("\n--- CLEANED DATA VALIDATION ---")
print("File loaded successfully")
print("Rows:", len(check_df))
print("Columns:", len(check_df.columns))

print("\nMissing CustomerID:",
      check_df["CustomerID"].isnull().sum())

print("Missing Description:",
      check_df["Description"].isnull().sum())

print("Duplicate rows:",
      check_df.duplicated().sum())

print("\nRevenue column exists:",
      "Revenue" in check_df.columns)

print("\nFirst 5 cleaned records:")
print(check_df.head())

# STEP 8: DAY 1 SUMMARY

print("\n===== DAY 1 PROJECT SUMMARY =====")
print("Project: Smart Retail Intelligence")
print("Original rows:", len(df))
print("Cleaned rows:", len(check_df))
print("Rows removed:", len(df) - len(check_df))
print("Columns in cleaned dataset:", len(check_df.columns))
print("Missing CustomerID:", check_df["CustomerID"].isnull().sum())
print("Missing Description:", check_df["Description"].isnull().sum())
print("Duplicate rows:", check_df.duplicated().sum())
print("Revenue column created:", "Revenue" in check_df.columns)
print("Day 1 status: COMPLETED")
