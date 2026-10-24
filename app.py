
import streamlit as st

st.set_page_config(
    page_title="StockWise | Inventory Copilot",
    page_icon="📦",
    layout="wide"
)

st.title("📦 StockWise")
st.subheader("Inventory Decision Copilot")
st.write(
    "Identify inventory risks, review replenishment "
    "recommendations, and estimate purchasing costs."
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Products Analysed", "30")
col2.metric("High-Risk Products", "3")
col3.metric("Products to Reorder", "5")
col4.metric("Estimated Order Cost", "₹80,753")

st.divider()

st.header("Inventory Risk Overview")

risk_col1, risk_col2, risk_col3 = st.columns(3)

risk_col1.metric("🔴 High Risk", "3 products")
risk_col2.metric("🟠 Medium Risk", "4 products")
risk_col3.metric("🟢 Low Risk", "23 products")

st.info(
    "This is the initial interface using synthetic-data "
    "results. The app will be extended with live calculations "
    "and uploaded inventory data."
)

st.header("Recommended Replenishment")

demo_recommendations = [
    {
        "Product": "Lip Balm",
        "Risk": "High Risk",
        "Reorder Quantity": 75,
        "Estimated Cost (₹)": 21750
    },
    {
        "Product": "Face Wash",
        "Risk": "High Risk",
        "Reorder Quantity": 55,
        "Estimated Cost (₹)": 34320
    },
    {
        "Product": "Face Mask",
        "Risk": "High Risk",
        "Reorder Quantity": 40,
        "Estimated Cost (₹)": 8800
    },
    {
        "Product": "Oats",
        "Risk": "Medium Risk",
        "Reorder Quantity": 23,
        "Estimated Cost (₹)": 14421
    },
    {
        "Product": "Coffee",
        "Risk": "Medium Risk",
        "Reorder Quantity": 2,
        "Estimated Cost (₹)": 1462
    }
]

st.dataframe(
    demo_recommendations,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Prototype demo | Recommendations use a preliminary "
    "rule-based policy and synthetic inventory data."
)
