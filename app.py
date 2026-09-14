import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime as dt

st.set_page_config(
    page_title="Retail Sales & Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("🛍️ Customer Purchase Behavior & Retail Analytics Dashboard")
st.markdown("Interactive analytics dashboard tracking sales trends, customer lifetime value, and RFM segment cohorts.")

@st.cache_data
def load_and_process_data():
    # Load dataset
    df = pd.read_excel("Online Retail.xlsx")

    # Data Cleaning
    df = df.dropna(subset=['CustomerID'])
    df = df.drop_duplicates()
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

    # Feature Engineering
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # RFM Analysis
    snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalAmount': 'sum'
    }).rename(columns={
        'InvoiceDate': 'Recency',
        'InvoiceNo': 'Frequency',
        'TotalAmount': 'Monetary'
    })

    # Scoring
    r_labels = [4, 3, 2, 1]
    rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=r_labels).astype(int)

    f_labels = [1, 2, 3, 4]
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=f_labels).astype(int)
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], q=4, labels=f_labels).astype(int)

    def assign_segment(row):
        r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
        if r >= 3 and f >= 3 and m >= 3:
            return 'Champions / High Value'
        elif f >= 3:
            return 'Loyal'
        elif r >= 3 and f < 3:
            return 'Potential'
        elif r <= 2 and (f >= 2 or m >= 3):
            return 'At Risk'
        else:
            return 'One-Time / Inactive'

    rfm['Customer_Segment'] = rfm.apply(assign_segment, axis=1)

    # Merge Segment back into master dataframe
    df = df.merge(rfm[['Customer_Segment']], on='CustomerID', how='left')
    return df

with st.spinner("Processing retail data & RFM segmentation... Please wait 20-30 seconds"):
    df = load_and_process_data()

# Sidebar Filters
st.sidebar.header("Filter Controls")
selected_country = st.sidebar.multiselect(
    "Select Country",
    options=df['Country'].unique(),
    default=['United Kingdom'] if 'United Kingdom' in df['Country'].unique() else df['Country'].unique()[:1]
)

selected_segment = st.sidebar.multiselect(
    "Select Customer Segment",
    options=df['Customer_Segment'].dropna().unique(),
    default=df['Customer_Segment'].dropna().unique()
)

# Filter Data
filtered_df = df[
    (df['Country'].isin(selected_country)) & 
    (df['Customer_Segment'].isin(selected_segment))
]

# Top KPI Metric Cards
total_revenue = filtered_df['TotalAmount'].sum()
total_orders = filtered_df['InvoiceNo'].nunique()
total_customers = filtered_df['CustomerID'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Unique Customers", f"{total_customers:,}")
col4.metric("Avg Order Value (AOV)", f"₹{avg_order_value:,.2f}")

st.markdown("---")

# Charts Row 1: Segments & Revenue
c1, c2 = st.columns(2)

with c1:
    st.subheader("Customer Distribution by Segment")
    seg_counts = filtered_df.groupby('Customer_Segment')['CustomerID'].nunique().reset_index()
    fig_pie = px.pie(
        seg_counts, 
        values='CustomerID', 
        names='Customer_Segment', 
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("Revenue Contribution by Segment")
    seg_rev = filtered_df.groupby('Customer_Segment')['TotalAmount'].sum().reset_index()
    fig_bar = px.bar(
        seg_rev, 
        x='Customer_Segment', 
        y='TotalAmount', 
        color='Customer_Segment',
        labels={'TotalAmount': 'Revenue (₹)'},
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Charts Row 2: Monthly Trends & Top Products
c3, c4 = st.columns(2)

with c3:
    st.subheader("Monthly Sales Trend")
    filtered_df['YearMonth'] = filtered_df['InvoiceDate'].dt.to_period('M').astype(str)
    monthly_sales = filtered_df.groupby('YearMonth')['TotalAmount'].sum().reset_index()
    fig_line = px.line(
        monthly_sales, 
        x='YearMonth', 
        y='TotalAmount', 
        markers=True,
        labels={'TotalAmount': 'Sales (₹)', 'YearMonth': 'Month'}
    )
    fig_line.update_traces(line_color='#2ecc71', line_width=3)
    st.plotly_chart(fig_line, use_container_width=True)

with c4:
    st.subheader("Top 10 Selling Products by Revenue")
    top_items = filtered_df.groupby('Description')['TotalAmount'].sum().reset_index()
    top_items = top_items.sort_values(by='TotalAmount', ascending=False).head(10)
    fig_items = px.bar(
        top_items, 
        y='Description', 
        x='TotalAmount', 
        orientation='h',
        labels={'TotalAmount': 'Revenue (₹)'},
        color_discrete_sequence=['#3498db']
    )
    fig_items.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_items, use_container_width=True)
