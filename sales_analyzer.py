
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. LOAD THE SALES DATASET
# ==========================================

df = pd.read_csv("sales_data.csv")

print("\n========== SALES DATA ANALYZER ==========")

# ==========================================
# 2. DISPLAY THE DATA
# ==========================================

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Dataset Shape ---")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n--- Column Information ---")
df.info()

# ==========================================
# 3. DATA CLEANING AND PREPARATION
# ==========================================

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Duplicate Rows ---")
print("Duplicates:", df.duplicated().sum())

# Remove duplicate rows
df = df.drop_duplicates()

# Convert Date column into datetime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert numeric columns
df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)
df["Unit_Price"] = pd.to_numeric(
    df["Unit_Price"], errors="coerce"
)

# Remove rows with missing essential values
df = df.dropna(
    subset=["Order_ID", "Date", "Product",
            "Quantity", "Unit_Price"]
)

# Remove invalid sales records
df = df[
    (df["Quantity"] > 0) &
    (df["Unit_Price"] >= 0)
].copy()

# ==========================================
# 4. CALCULATE REVENUE
# ==========================================

df["Revenue"] = df["Quantity"] * df["Unit_Price"]

print("\n--- Cleaned Dataset ---")
print(df.head())

# ==========================================
# 5. KEY SALES METRICS
# ==========================================

total_revenue = df["Revenue"].sum()
total_orders = df["Order_ID"].nunique()
total_units = df["Quantity"].sum()

order_revenue = df.groupby("Order_ID")["Revenue"].sum()
average_order_value = order_revenue.mean()

print("\n========== SALES SUMMARY ==========")
print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Total Units Sold: {total_units:,.0f}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")

# ==========================================
# 6. REVENUE BY PRODUCT
# ==========================================

product_revenue = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Revenue by Product ---")
print(product_revenue)

if not product_revenue.empty:
    print(
        "Highest Revenue Product:",
        product_revenue.idxmax()
    )

# ==========================================
# 7. UNITS SOLD BY PRODUCT
# ==========================================

units_by_product = (
    df.groupby("Product")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Units Sold by Product ---")
print(units_by_product)

if not units_by_product.empty:
    print(
        "Best-Selling Product by Quantity:",
        units_by_product.idxmax()
    )

# ==========================================
# 8. MONTHLY SALES ANALYSIS
# ==========================================

df["Month"] = df["Date"].dt.to_period("M")

monthly_revenue = (
    df.groupby("Month")["Revenue"].sum()
    .sort_index()
)

print("\n--- Monthly Revenue ---")
print(monthly_revenue)

if not monthly_revenue.empty:
    print("Best Sales Month:", monthly_revenue.idxmax())

# ==========================================
# 9. REVENUE BY CATEGORY
# ==========================================

if "Category" in df.columns:
    category_revenue = (
        df.groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n--- Revenue by Category ---")
    print(category_revenue)

# ==========================================
# 10. CREATE REVENUE BY PRODUCT CHART
# ==========================================

if not product_revenue.empty:
    plt.figure(figsize=(9, 5))

    product_revenue.sort_values().plot(
        kind="barh"
    )

    plt.title("Total Revenue by Product")
    plt.xlabel("Revenue (₹)")
    plt.ylabel("Product")
    plt.tight_layout()

    plt.savefig("revenue_by_product.png")
    plt.show()

# ==========================================
# 11. CREATE MONTHLY SALES CHART
# ==========================================

if not monthly_revenue.empty:
    plt.figure(figsize=(9, 5))

    monthly_revenue.plot(
        kind="line", marker="o"
    )

    plt.title("Monthly Sales Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue (₹)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("monthly_sales.png")
    plt.show()

# ==========================================
# 12. EXPORT CLEANED DATA
# ==========================================

df.to_csv("cleaned_sales_data.csv", index=False)

print("\nCleaned dataset saved as cleaned_sales_data.csv")
print("Charts saved as PNG files.")
print("\n========== ANALYSIS COMPLETED ==========")
