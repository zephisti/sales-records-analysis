# To access and print the DataFrame values as a NumPy array
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataframe
df = pd.read_csv('sales_records.csv')

# --- Data Cleaning Steps ---
# 1. Strip whitespace from column names
df.columns = df.columns.str.strip()

# 2. Convert date columns to datetime objects
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# 3. Clean and convert currency columns to numeric
currency_cols = ['Unit Price', 'Unit Cost', 'Total Revenue', 'Total Cost', 'Total Profit']
for col in currency_cols:
    # Remove '$', ',', and strip leading/trailing whitespace then convert to float
    df[col] = df[col].astype(str).str.replace('[\$,]', '', regex=True).str.strip().astype(float)

# 4. Strip whitespace from other object (string) columns for consistency
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.strip()

# --- Original Script Output ---
print("--- Initial DataFrame Head (after cleaning) ---")
print(df.head())
print("\n--- DataFrame Shape ---")
print(df.shape)
print("\n--- DataFrame Description (numerical columns after cleaning) ---")
print(df.describe())
print("\n--- DataFrame Values (NumPy array) ---")
print(df.values)
print("\n--- DataFrame Info (to check data types) ---")
df.info()

# --- Now for some cool pandas operations! ---
print("\n\n--- Cool Pandas Operations ---")

# 1. What are the top 5 most profitable countries?
top_profitable_countries = df.groupby('Country')['Total Profit'].sum().sort_values(ascending=False).head(5)
print("\n1. Top 5 Most Profitable Countries:")
print(top_profitable_countries)

# 2. Which Item Type generates the most revenue on average?
avg_revenue_by_item = df.groupby('Item Type')['Total Revenue'].mean().sort_values(ascending=False)
print("\n2. Average Revenue by Item Type:")
print(avg_revenue_by_item)

# 3. How do online vs. offline sales channels compare in terms of total units sold and total revenue?
sales_channel_summary = df.groupby('Sales Channel').agg(
    Total_Units_Sold=('Units Sold', 'sum'),
    Total_Revenue_Generated=('Total Revenue', 'sum')
).sort_values(by='Total_Revenue_Generated', ascending=False)
print("\n3. Sales Channel Summary (Units Sold & Revenue):")
print(sales_channel_summary)

# 4. What is the monthly sales trend?
# Ensure 'Order Date' is the index for time series resampling
df_time_indexed = df.set_index('Order Date')
monthly_sales = df_time_indexed['Total Revenue'].resample('ME').sum() # 'ME' for month end frequency
print("\n4. Monthly Sales Revenue Trend (first 12 months):")
print(monthly_sales.head(12))
monthly_sales.plot(title='Monthly Sales Revenue')
plt.ylabel('Total Revenue')
plt.show()

# 5. Which regions have the highest average profit margin?
# Profit Margin = (Total Profit / Total Revenue) * 100
df['Profit Margin (%)'] = (df['Total Profit'] / df['Total Revenue']) * 100
avg_profit_margin_by_region = df.groupby('Region')['Profit Margin (%)'].mean().sort_values(ascending=False)
print("\n5. Average Profit Margin by Region (%):")
print(avg_profit_margin_by_region)

# 6. What's the average shipping time for orders?
df['Shipping Time (Days)'] = (df['Ship Date'] - df['Order Date']).dt.days
print("\n6. Average Shipping Time (Days):")
print(f"{df['Shipping Time (Days)'].mean():.2f} days")
print("\n   Longest Shipping Times (Top 5):")
print(df.sort_values(by='Shipping Time (Days)', ascending=False)[['Order ID', 'Country', 'Shipping Time (Days)']].head())

# 7. Pivot Table: Total revenue for each Item Type across different Sales Channels
pivot_revenue = pd.pivot_table(df, values='Total Revenue', index='Item Type', columns='Sales Channel', aggfunc='sum', fill_value=0)
print("\n7. Pivot Table: Total Revenue by Item Type and Sales Channel:")
print(pivot_revenue)

# 8. How many unique items are sold per region?
items_per_region = df.groupby('Region')['Item Type'].nunique().sort_values(ascending=False)
print("\n8. Number of Unique Item Types Sold per Region:")
print(items_per_region)

# 9. What is the distribution of 'Order Priority'?
order_priority_distribution = df['Order Priority'].value_counts(normalize=True) * 100
print("\n9. Order Priority Distribution (%):")
print(order_priority_distribution)

# 10. Which 'Item Type' has the highest 'Unit Cost' on average?
avg_unit_cost_item = df.groupby('Item Type')['Unit Cost'].mean().sort_values(ascending=False)
print("\n10. Average Unit Cost by Item Type:")
print(avg_unit_cost_item.head())

