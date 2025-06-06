import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# load data set

df = pd.read_csv(r'C:\Users\suche\Downloads\pro\superstore.csv',encoding='ISO-8859-1')
#--------------------------------------------------------------------------------------------------------------------
'''
1. Sales & Profit Performance
A. Identify our top and bottom performing products, categories, and sub-categories.

B. Break down sales and profit performance by state, region, and city.

C. Analyze the impact of discounting on profit margins. Are we over-discounting in ways that hurt profitability?'''

#--------------------------------------------------------------------------------------------------------------------------
# Set style for seaborn
sns.set(style = "whitegrid")

# ----------------------------
# A. Top and Bottom Products by Profit
# ----------------------------
top_product = df.groupby("Product Name")["Profit"].sum().sort_values(ascending= False).head(10)
bottom_products = df.groupby("Product Name")["Profit"].sum().sort_values().head(10)

# Category and Sub-Category
category_profit = df.groupby("Category")[["Sales", "Profit"]].sum().sort_values(by="Profit", ascending=False)
subcategory_profit = df.groupby("Sub-Category")[["Sales", "Profit"]].sum().sort_values(by="Profit", ascending=False)

# ----------------------------
# B. Sales & Profit by State, Region, City
# ----------------------------
# State-level
state_profit= df.groupby("State")[["Sales", "Profit"]].sum().sort_values(by="Profit", ascending=False)

# Region-level
region_profit = df.groupby("Region")[["Sales", "Profit"]].sum().sort_values(by="Profit", ascending=False)

# City-level (top/bottom 10 cities by profit)
top_cities = df.groupby("City")["Profit"].sum().sort_values(ascending=False).head(10)
bottom_cities = df.groupby("City")["Profit"].sum().sort_values().head(10)




# ----------------------------
# C. Discount vs Profit Correlation
# ----------------------------

discount_profit_corr = df[["Discount" ,"Profit"]].corr().loc["Discount" ,"Profit"]
print(discount_profit_corr)

# ----------------------------
# Visualization 1.
# ----------------------------

plt.figure(figsize=(20,28))

# 1. Top 10 Products
plt.subplot(5, 2, 1)
top_product.plot(kind='barh', color= "green")
plt.title("Top 10 Products by Profit")
plt.xlabel("Total Profit")

# 2. Bottom 10 Products
plt.subplot(5, 2, 2)
bottom_products.plot(kind='barh', color='red')
plt.title("Bottom 10 Products by Profit")
plt.xlabel("Total Profit")


# 3. Profit by Category
plt.subplot(5, 2, 3)
category_profit["Profit"].plot(kind='barh', color='red')
plt.title("Profit by Category")

# 4. Profit by Sub-Category
plt.subplot(5, 2, 4)
subcategory_profit["Profit"].plot(kind='bar', color='orange')
plt.title("Profit by Sub-Category")
plt.ylabel("Profit")

# 5. Profit by Region

plt.subplot(5, 2, 5)
region_profit["Profit"].plot(kind='bar', color='purple')
plt.title("Profit by Region")
plt.ylabel("Profit")

# 6. Profit by State (Top 10)

plt.subplot(5, 2, 6)
state_profit["Profit"].head(10).plot(kind='bar', color='teal')
plt.title("Top 10 States by Profit")
plt.ylabel("Profit")



# 7. Bottom 10 Cities by Profit
plt.subplot(5, 2, 7)
bottom_cities.plot(kind='barh', color='darkred')
plt.title("Bottom 10 Cities by Profit")
plt.xlabel("Total Profit")

# 8. top 10 Cities by Profit
plt.subplot(5, 2, 8)
top_cities .plot(kind='barh', color='black')
plt.title("Top 10 Cities by Profit")
plt.xlabel("Total Profit")

plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
'''
2. Customer Analysis
Profile our most valuable customer segments. Which groups contribute the most to sales and profit?

Explore any patterns in customer behavior that might inform targeted marketing.

Highlight key locations where we have high customer engagement or growth potential.'''
#---------------------------------------------------------------------------------------------------------------

# OBJECTIVE 1: Profile our most valuable customer segments
# Goal: Find which customer segments (Consumer, Corporate, Home Office) contribute most to Sales and Profit.

# --------------------------------------------------------------------------------------------------------------------
# OBJECTIVE 1: Most Valuable Customer Segments
# --------------------------------------------------------------------------------------------------------------------

segment_analysis = df.groupby("Segment")[["Sales","Profit"]].sum().sort_values(by="Sales", ascending=False)

# --------------------------------------------------------------------------------------------------------------------
# OBJECTIVE 2: Customer Behavior Patterns
# Goal: Frequent buyers/High spenders/Customers sensitive to discounts
# --------------------------------------------------------------------------------------------------------------------

# Group by Customer ID
customer_behavior = df.groupby("Customer ID").agg({
    "Sales": "sum",
    "Profit": "sum",
    "Order ID": "nunique",
    "Discount": "mean"}).rename(columns={"Order ID": "Num_Orders"})

# Frequent buyers = most orders
frequent_customers = customer_behavior.sort_values(by= "Num_Orders", ascending = False).head(10)

# # High spenders = most sales
high_spenders = customer_behavior.sort_values(by="Sales", ascending=False).head(10)

# High profit generators
profit_customers = customer_behavior.sort_values(by="Profit", ascending=False).head(10)


# Discount-reliant (high discount, low profit)
discount_loss = customer_behavior.sort_values(by="Discount", ascending=False).head(10)

# --------------------------------------------------------------------------------------------------------------------
# OBJECTIVE 3: High Engagement / Growth Potential Locations
# -----------------------------------------------------------------------------------

# Cities with most orders
city_engagement= df.groupby("City")["Order ID"].nunique().sort_values(ascending=False).head(10)

# States with most unique customers
state_customers = df.groupby("State")["Customer ID"].nunique().sort_values(ascending=False).head(10)

# --------------------------------------------------------------------------------------------------------------------
# VISUALIZATION 2
# --------------------------------------------------------------------------------------------------------------------
plt.figure(figsize=(22, 30))

# 1. Segment contribution
plt.subplot(4, 2, 1)
segment_analysis["Sales"].plot(kind="bar", color="skyblue")
plt.title("Sales Contribution by Segment")
plt.ylabel("Sales")


plt.subplot(4, 2, 2)
segment_analysis["Profit"].plot(kind="bar", color="salmon")
plt.title("Profit Contribution by Segment")
plt.ylabel("Profit")

# 2. High Spenders

plt.subplot(4, 2, 3)
high_spenders["Sales"].plot(kind="bar", color="green")
plt.title("Top 10 High-Spending Customers")
plt.ylabel("Sales")


# 3. Frequent Buyers

plt.subplot(4, 2, 4)
frequent_customers["Num_Orders"].plot(kind="bar", color="blue")
plt.title("Top 10 Frequent Buyers")
plt.ylabel("Number of Orders")

# 4. Most Profitable Customers
plt.subplot(4, 2, 5)
profit_customers["Profit"].plot(kind="bar", color="orange")
plt.title("Top 10 Profitable Customers")
plt.ylabel("Profit")

# 5. Customers with High Discounts
plt.subplot(4, 2, 6)
discount_loss["Discount"].plot(kind="bar", color="red")
plt.title("Top 10 Customers with Highest Discounts")
plt.ylabel("Average Discount")

# 6. Cities with Most Orders
plt.subplot(4, 2, 7)
city_engagement.plot(kind="bar", color="purple")
plt.title("Top 10 Cities by Order Volume")
plt.ylabel("Order Count")

# 7. States with Most Unique Customers
plt.subplot(4, 2, 8)
state_customers.plot(kind="bar" ,color="teal")
plt.title("Top 10 States by Unique Customers")
plt.ylabel("Unique Customers")

plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
'''
3. Operational Efficiency
Evaluate the efficiency and cost-effectiveness of different shipping modes.

Provide insights into order delivery times and any region-specific delays.

Assess average quantities ordered and suggest any trends related to stock optimization.'''
# ----------------------------------------------------------------------------------------------


# Convert date columns
df["Order Date"] = pd.to_datetime(df["Order Date"])

  
df["Ship Date"] = pd.to_datetime(df["Ship Date"])



# -----------------------------------------
# A. Shipping Mode Performance
# -----------------------------------------

shipping_summary = df.groupby("Ship Mode").agg({
    "Sales": "sum",
    "Profit": "sum",
    "Order ID": "nunique"}).rename(columns={"Order ID": "Total Orders"})


# Add cost-effectiveness metric
shipping_summary["Profit per Order"] = shipping_summary["Profit"]/shipping_summary["Total Orders"]
shipping_summary = shipping_summary.sort_values(by="Profit per Order", ascending=False)


# -----------------------------------------
# B. Order Delivery Timelines by Region
# -----------------------------------------

df["Delivery Time (Days)"]= (df["Ship Date"] - df["Order Date"])
region_delivery_time = df.groupby("Region")["Delivery Time (Days)"].mean()

# -----------------------------------------
# C. Quantity Trends for Stock Optimization
# -----------------------------------------

# Average quantity ordered per Sub-Category
quantity_by_subcat = df.groupby("Sub-Category")["Quantity"].mean().sort_values(ascending=False)


# Average quantity per Region
quantity_by_region = df.groupby("Region")["Quantity"].mean().sort_values(ascending=False)

# -----------------------------------------
# VISUALIZATION 3
# -----------------------------------------
plt.figure(figsize=(18, 22))  # Adjust size for clarity

# 1. Shipping Mode - Sales
plt.subplot(3, 2, 1)
shipping_summary["Sales"].plot(kind="bar", color="skyblue")
plt.title("Total Sales by Shipping Mode")
plt.ylabel("Sales")

# 2. Shipping Mode - Profit
plt.subplot(3, 2, 2)
shipping_summary["Profit"].plot(kind="bar", color="salmon")
plt.title("Total Profit by Shipping Mode")
plt.ylabel("Profit")

# 3. Shipping Mode - Profit per Order
plt.subplot(3, 2, 3)
shipping_summary["Profit per Order"].plot(kind="bar", color="green")
plt.title("Profit per Order by Shipping Mode")
plt.ylabel("Profit/Order")

# 4. Average Delivery Time by Region
plt.subplot(3, 2, 4)
region_delivery_time.plot(kind="bar", color="orange")
plt.title("Average Delivery Time by Region")
plt.ylabel("Days")

# 5. Average Quantity by Sub-Category
plt.subplot(3, 2, 5)
quantity_by_subcat.plot(kind="bar", color="purple")
plt.title("Avg Quantity Ordered by Sub-Category")
plt.ylabel("Average Quantity")

# 6. Average Quantity by Region
plt.subplot(3, 2, 6)
quantity_by_region.plot(kind="bar", color="teal")
plt.title("Avg Quantity Ordered by Region")
plt.ylabel("Average Quantity")

plt.tight_layout()
plt.show()


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------




# --------------------------------------------------------------------------------------------------
'''
4. Future Planning & Forecasting
Forecast monthly or quarterly sales trends based on historical data.

Identify any seasonal patterns or trends we can leverage for promotional planning.

Recommend changes in inventory management or marketing strategy based on projected demand.'''
# ---------------------------------------------------------------------------------------------------

# --------------------------------------------------------
# A. Monthly & Quarterly Sales Forecasting (Historical)
# --------------------------------------------------------

# Set Order Date as index
df_time = df.set_index("Order Date")

# Resample by month and quarter
monthly_sales = df_time["Sales"].resample("ME").sum()
quarterly_sales = df_time["Sales"].resample("QE").sum()


# Simple Moving Average (3-month) for forecasting trend
monthly_sma = monthly_sales.rolling(window=3).mean()

# --------------------------------------------------------
# B. Seasonal Pattern Detection
# --------------------------------------------------------

# Extract month and year
df["Month"] = df["Order Date"].dt.month
df["Year"]  = df["Order Date"].dt.year

# Avg monthly sales across years
seasonality = df.groupby("Month")["Sales"].mean()

# --------------------------------------------------------
# VISUALIZATION 4
# --------------------------------------------------------


plt.figure(figsize=(20, 20))

# 1. Monthly Sales Trend
plt.subplot(3, 1, 1)
monthly_sales.plot(label="Monthly Sales", color="skyblue")
monthly_sma.plot(label="3-Month Moving Avg", color="red")
plt.title("Monthly Sales with Forecast Trend")
plt.ylabel("Sales")
plt.legend()

# 2. Quarterly Sales Trend
plt.subplot(3, 1, 2)
quarterly_sales.plot(kind="line", marker="o", color="green")
plt.title("Quarterly Sales Trend")
plt.ylabel("Sales")

# 3. Average Sales by Month (Seasonality)
plt.subplot(3, 1, 3)
seasonality.plot(kind="bar", color="orange")
plt.title("Average Monthly Sales Across Years")
plt.ylabel("Avg Sales")
plt.xlabel("Month")

plt.tight_layout()
plt.show()


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
'''
5. Additional Strategic Observations
If you find any interesting or concerning patterns — such as consistently unprofitable categories, 
regional anomalies,or overlooked sales opportunities —please flag them. Your proactive insights are 
always welcome.'''
# ---------------------------------------------------------------------------------------------------
'''So what i found 
1.Unprofitable sub-categories
2.High discount & low profit segments
3.Profit margins by region/state'''
# ---------------------------------------------------------------------------------------------------

# ------------------------------
# 1. Unprofitable Sub-Categories
# ------------------------------
subcategory_profit = df.groupby("Sub-Category")[["Sales" ,"Profit"]].sum().sort_values(by ="Profit")
unprofitable_subcats = subcategory_profit[subcategory_profit["Profit"] < 0]

# ------------------------------
# 2. High Discount, Low Profit
# ------------------------------
discount_impact = df.groupby("Sub-Category")[["Discount", "Profit"]].mean()
high_discount_low_profit = discount_impact[(discount_impact["Discount"] > 0.2) & (discount_impact["Profit"] < 0)].sort_values(by="Discount", ascending=False)

# ------------------------------
# 3. Profit Margin by Region & State
# ------------------------------

region_anomaly = df.groupby("Region")[["Sales" ,"Profit"]].sum()
region_anomaly["Profit Margin (%)"] = (region_anomaly["Profit"] / region_anomaly["Sales"]) * 100


state_anomaly =df.groupby("State")[["Sales" ,"Profit"]].sum()
state_anomaly["Profit Margin (%)"]= (state_anomaly["Profit"]/state_anomaly["Sales"])* 100
low_margin_states= state_anomaly[state_anomaly["Profit Margin (%)"] <5].sort_values(by="Profit Margin (%)")

# ------------------------------
# VISUALIZATION 5
# ------------------------------

plt.figure(figsize=(22, 24))


# 1. Unprofitable Sub-Categories
plt.subplot(3, 2, 1)
unprofitable_subcats["Profit"].plot(kind='barh', color='crimson')
plt.title("Unprofitable Sub-Categories")
plt.xlabel("Total Profit")

# 2. High Discount, Low Profit Sub-Categories
plt.subplot(3, 2, 2)
sns.scatterplot(data=high_discount_low_profit, x="Discount", y="Profit", s=100, color='orange')
for i in high_discount_low_profit.index:
    plt.text(high_discount_low_profit.loc[i, "Discount"]+0.005, high_discount_low_profit.loc[i, "Profit"]+1, i)
plt.title("High Discount & Low Profit Sub-Categories")
plt.xlabel("Avg Discount")
plt.ylabel("Avg Profit")    

# 3. Profit Margin by Region
plt.subplot(3, 2, 3)
region_anomaly["Profit Margin (%)"].plot(kind='bar', color='skyblue')
plt.title("Profit Margin by Region")
plt.ylabel("Profit Margin (%)")


# 4. States with Lowest Profit Margins
plt.subplot(3, 2, 4)
low_margin_states["Profit Margin (%)"].plot(kind='barh', color='darkred')
plt.title("States with Low Profit Margin (<5%)")
plt.xlabel("Profit Margin (%)")

# 5. Profit vs Discount Heatmap
plt.subplot(3, 2, 5)
heatmap_data=  df.pivot_table(index = "Region", columns="Category", values="Profit", aggfunc="sum")
sns.heatmap(heatmap_data,annot=True, fmt=".0f", cmap="RdYlGn")
plt.title("Profit Heatmap by Region & Category")


# 6. Profit per Sub-Category (Overview)
plt.subplot(3, 2, 6)
subcategory_profit["Profit"].plot(kind= "bar", color = "gray")
plt.title("Profit by Sub-Category")
plt.ylabel("Profit")

plt.tight_layout()
plt.show()






































