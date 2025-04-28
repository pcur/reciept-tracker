from config.env import load_config
load_config()

import streamlit as st
import pandas as pd
import plotly.express as px
from services.db_service import get_all_receipts
debug = 0
st.header("📊 Dashboard")

# Fetch all receipts from JSON files
receipts = get_all_receipts()

if not receipts:
    st.info("No receipts found yet.")
    st.stop()

# Convert receipts to a DataFrame for easier analysis
data = pd.DataFrame(receipts)

# After loading data
data = pd.DataFrame(receipts)

# Ensure numeric and date formats
data["total_amount"] = pd.to_numeric(data["total_amount"], errors="coerce")
data["purchase_date"] = pd.to_datetime(data["purchase_date"], format="%m/%d/%y", errors="coerce")

# Drop missing/invalid
data = data.dropna(subset=["total_amount", "category"])

# Standardize categories
data["category"] = data["category"].str.strip().str.title()

# -- Insert a debug printout
if debug == 1:
    st.write("Receipts DataFrame:", data)

# Now plot
st.subheader("Spending by Category")
category_spending = data.groupby("category")["total_amount"].sum().reset_index()

# Debug printout
if debug == 1:
    st.write("Data for Pie Chart:", category_spending)

fig_pie = px.pie(category_spending, values="total_amount", names="category", title="Spending by Category")
st.plotly_chart(fig_pie)

# Spending per day
st.subheader("Spending Per Day")
daily_spending = data.groupby(data["purchase_date"].dt.date)["total_amount"].sum().reset_index()
daily_spending.columns = ["Date", "Total Amount"]
fig_line = px.line(daily_spending, x="Date", y="Total Amount", title="Spending Per Day")
st.plotly_chart(fig_line)

