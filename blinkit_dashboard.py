
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("Blinkit.xlsx")

# Title
st.title("🛒 Blinkit Sales Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
fat_filter = st.sidebar.multiselect("Select Fat Content:", options=df["Item Fat Content"].unique(), default=df["Item Fat Content"].unique())
location_filter = st.sidebar.multiselect("Select Outlet Location:", options=df["Outlet Location Type"].unique(), default=df["Outlet Location Type"].unique())

# Apply filters
df_filtered = df[
    (df["Item Fat Content"].isin(fat_filter)) &
    (df["Outlet Location Type"].isin(location_filter))
]

# KPIs
total_sales = int(df_filtered["Sales"].sum())
avg_rating = round(df_filtered["Rating"].mean(), 2)
total_items = df_filtered["Item Identifier"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("⭐ Average Rating", avg_rating)
col3.metric("📦 Unique Items", total_items)

st.markdown("---")

# Sales by Item Type
st.subheader("📊 Sales by Item Type")
sales_by_type = df_filtered.groupby("Item Type")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False)
fig1 = px.bar(sales_by_type, x="Item Type", y="Sales", color="Sales", title="Sales by Item Type")
st.plotly_chart(fig1, use_container_width=True)

# Sales by Outlet Type
st.subheader("🏪 Sales by Outlet Type")
sales_by_outlet = df_filtered.groupby("Outlet Type")["Sales"].sum().reset_index()
fig2 = px.pie(sales_by_outlet, names="Outlet Type", values="Sales", title="Sales by Outlet Type")
st.plotly_chart(fig2, use_container_width=True)

# Item Visibility vs. Sales
st.subheader("🔍 Item Visibility vs Sales")
fig3 = px.scatter(df_filtered, x="Item Visibility", y="Sales", color="Item Type", size="Item Weight", hover_data=["Item Identifier"])
st.plotly_chart(fig3, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Built with 💡 by a Data Analyst using Python + Streamlit")
