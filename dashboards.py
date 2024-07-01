import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the page layout
st.set_page_config(layout="wide", page_title="Supermarket Sales Dashboard")

# Load the data
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Extract month and year
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Month", df["Month"].unique())

# Filter data for the selected month
df_filtered = df[df["Month"] == month]

# Define the new color palette
color_palette = px.colors.qualitative.Set2

# Titles and Layout
st.title("📊 Supermarket Sales Dashboard")
st.subheader(f"Analysis for {month}")

# Create columns for layout
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Plot 1: Revenue by day
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Daily Revenue",
                  color_discrete_sequence=color_palette)
col1.plotly_chart(fig_date, use_container_width=True)

# Plot 2: Revenue by product type
fig_prod = px.bar(df_filtered, x="Total", y="Product line", 
                  color="City", title="Revenue by Product Type",
                  orientation="h", color_discrete_sequence=color_palette)
col2.plotly_chart(fig_prod, use_container_width=True)

# Plot 3: Revenue by branch
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total",
                   title="Revenue by Branch", color_discrete_sequence=color_palette)
col3.plotly_chart(fig_city, use_container_width=True)

# Plot 4: Revenue by payment type
fig_kind = px.pie(df_filtered, values="Total", names="Payment",
                   title="Revenue by Payment Type", color_discrete_sequence=color_palette)
col4.plotly_chart(fig_kind, use_container_width=True)

# Plot 5: Branch ratings
city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(city_rating, x="City", y="Rating",
                   title="Branch Ratings", color_discrete_sequence=color_palette)
col5.plotly_chart(fig_rating, use_container_width=True)
