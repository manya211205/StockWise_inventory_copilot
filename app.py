
import streamlit as st
import pandas as pd
from inventory_logic import (
    generate_inventory_data,
    calculate_inventory,
    validate_inventory_upload,
)

st.set_page_config(
    page_title="StockWise | Inventory Copilot",
    page_icon="📦",
    layout="wide",
)

st.title("📦 StockWise")
st.subheader("Inventory Decision Copilot")
st.write(
    "Identify inventory risks, review replenishment "
    "recommendations, and estimate purchasing costs."
)

st.divider()

# Choose the inventory data source
st.header("Inventory Data")

data_source = st.radio(
    "Choose your data source",
    ["Demo dataset", "Upload your own CSV"],
    horizontal=True,
)

if data_source == "Upload your own CSV":
    uploaded_file = st.file_uploader(
        "Upload an inventory CSV file",
        type=["csv"],
        help=(
            "Required columns: SKU, Product, Category, Current_Stock, "
            "Avg_Daily_Sales, Lead_Time_Days, Incoming_Stock, Unit_Cost"
        ),
    )

    if uploaded_file is None:
        st.info("Upload a CSV file to analyse your inventory.")
        st.stop()

    try:
        uploaded_inventory = pd.read_csv(uploaded_file)
        is_valid, message = validate_inventory_upload(
            uploaded_inventory.copy()
        )

        if not is_valid:
            st.error(message)
            st.stop()

        inventory = calculate_inventory(uploaded_inventory)
        st.success("Inventory file validated successfully.")

    except Exception as error:
        st.error(f"Unable to process this file: {error}")
        st.stop()

else:
    inventory = calculate_inventory(generate_inventory_data())
    st.info("Currently using the built-in synthetic demo dataset.")

st.divider()

# Calculate dashboard metrics
total_products = len(inventory)

high_risk = int(
    (inventory["Risk_Level"] == "High Risk").sum()
)
medium_risk = int(
    (inventory["Risk_Level"] == "Medium Risk").sum()
)
low_risk = int(
    (inventory["Risk_Level"] == "Low Risk").sum()
)

reorder_items = inventory[
    inventory["Suggested_Reorder_Qty"] > 0
].copy()

total_reorder_units = int(
    reorder_items["Suggested_Reorder_Qty"].sum()
)

total_order_cost = float(
    reorder_items["Suggested_Order_Cost"].sum()
)

# Main dashboard
st.header("Inventory Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Products Analysed", total_products)
col2.metric("High-Risk Products", high_risk)
col3.metric("Products to Reorder", len(reorder_items))
col4.metric("Estimated Order Cost", f"₹{total_order_cost:,.0f}")

st.divider()

# Risk overview
st.header("Inventory Risk Overview")

risk_col1, risk_col2, risk_col3 = st.columns(3)

risk_col1.metric("🔴 High Risk", f"{high_risk} products")
risk_col2.metric("🟠 Medium Risk", f"{medium_risk} products")
risk_col3.metric("🟢 Low Risk", f"{low_risk} products")

risk_counts = (
    inventory["Risk_Level"]
    .value_counts()
    .reindex(
        ["High Risk", "Medium Risk", "Low Risk"],
        fill_value=0,
    )
)

st.bar_chart(risk_counts)

st.divider()

# Replenishment recommendations
st.header("Recommended Replenishment")

st.write(
    f"Recommended order quantity: **{total_reorder_units:,} units**"
)

if reorder_items.empty:
    st.success("No products currently require replenishment.")
else:
    recommendations = reorder_items[
        [
            "SKU",
            "Product",
            "Category",
            "Risk_Level",
            "Current_Stock",
            "Incoming_Stock",
            "Suggested_Reorder_Qty",
            "Unit_Cost",
            "Suggested_Order_Cost",
            "Recommendation_Reason",
        ]
    ].sort_values(
        by=["Risk_Level", "Suggested_Order_Cost"],
        ascending=[True, False],
    )

    recommendations = recommendations.rename(
        columns={
            "Risk_Level": "Risk Level",
            "Current_Stock": "Current Stock",
            "Incoming_Stock": "Incoming Stock",
            "Suggested_Reorder_Qty": "Reorder Quantity",
            "Unit_Cost": "Unit Cost (₹)",
            "Suggested_Order_Cost": "Estimated Order Cost (₹)",
            "Recommendation_Reason": "Recommendation",
        }
    )

    st.dataframe(
        recommendations,
        use_container_width=True,
        hide_index=True,
    )

st.divider()

# Explore inventory
st.header("Explore All Inventory")

risk_filter = st.multiselect(
    "Filter by risk level",
    options=["High Risk", "Medium Risk", "Low Risk"],
    default=["High Risk", "Medium Risk", "Low Risk"],
)

filtered_inventory = inventory[
    inventory["Risk_Level"].isin(risk_filter)
]

st.dataframe(
    filtered_inventory,
    use_container_width=True,
    hide_index=True,
)

# Download calculated results
csv_data = inventory.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download analysed inventory as CSV",
    data=csv_data,
    file_name="stockwise_inventory_analysis.csv",
    mime="text/csv",
)


# Prioritised Action List
st.divider()
st.header("🎯 Prioritised Action List")
st.write(
    "Focus on the products that need attention first. "
    "Actions are ranked using inventory risk and replenishment needs."
)

action_list = inventory.copy()

action_list["Action Priority"] = action_list["Risk_Level"].map({
    "High Risk": 1,
    "Medium Risk": 2,
    "Low Risk": 3,
}).fillna(4)

def get_next_action(row):
    if row["Risk_Level"] == "High Risk":
        if row["Suggested_Reorder_Qty"] > 0:
            return "Urgent: Review and place replenishment order"
        return "Urgent: Check supplier delivery and stock availability"

    if row["Risk_Level"] == "Medium Risk":
        if row["Suggested_Reorder_Qty"] > 0:
            return "Plan replenishment before stock becomes critical"
        return "Monitor stock and upcoming demand"

    if row["Suggested_Reorder_Qty"] > 0:
        return "Review suggested replenishment quantity"

    return "No immediate action required; continue monitoring"

action_list["Recommended Action"] = action_list.apply(
    get_next_action, axis=1
)

action_list = action_list.sort_values(
    by=[
        "Action Priority",
        "Projected_Days_of_Cover",
        "Suggested_Order_Cost",
    ],
    ascending=[True, True, False],
)

action_list["Action Priority"] = action_list["Action Priority"].map({
    1: "P1 - Urgent",
    2: "P2 - Plan",
    3: "P3 - Monitor",
    4: "Review",
})

priority_filter = st.multiselect(
    "Filter action list by priority",
    options=["P1 - Urgent", "P2 - Plan", "P3 - Monitor"],
    default=["P1 - Urgent", "P2 - Plan", "P3 - Monitor"],
)

visible_actions = action_list[
    action_list["Action Priority"].isin(priority_filter)
]

st.dataframe(
    visible_actions[
        [
            "SKU",
            "Product",
            "Risk_Level",
            "Projected_Days_of_Cover",
            "Lead_Time_Days",
            "Suggested_Reorder_Qty",
            "Suggested_Order_Cost",
            "Recommended Action",
            "Action Priority",
        ]
    ].rename(columns={
        "Risk_Level": "Risk Level",
        "Projected_Days_of_Cover": "Projected Days of Cover",
        "Lead_Time_Days": "Supplier Lead Time (Days)",
        "Suggested_Reorder_Qty": "Suggested Reorder Units",
        "Suggested_Order_Cost": "Estimated Order Cost (₹)",
    }),
    use_container_width=True,
    hide_index=True,
)


# Budget-Aware Replenishment
st.divider()
st.header("💰 Budget-Aware Replenishment")

st.write(
    "Set your purchasing budget to identify which recommended "
    "reorders can be prioritised within that limit."
)

budget = st.number_input(
    "Available purchasing budget (₹)",
    min_value=0,
    value=50000,
    step=5000,
)

budget_items = reorder_items.copy()

if budget_items.empty:
    st.success("No replenishment orders are currently recommended.")
else:
    # Prioritise higher-risk products, then lower days of cover
    budget_items = budget_items.sort_values(
        by=[
            "Risk_Priority",
            "Projected_Days_of_Cover",
            "Suggested_Order_Cost",
        ],
        ascending=[True, True, False],
    )

    selected_rows = []
    remaining_budget = float(budget)

    for _, row in budget_items.iterrows():
        order_cost = float(row["Suggested_Order_Cost"])

        if order_cost <= remaining_budget:
            selected_rows.append({
                "SKU": row["SKU"],
                "Product": row["Product"],
                "Risk Level": row["Risk_Level"],
                "Reorder Units": int(row["Suggested_Reorder_Qty"]),
                "Estimated Cost (₹)": order_cost,
                "Decision": "Prioritised within budget",
            })
            remaining_budget -= order_cost
        else:
            selected_rows.append({
                "SKU": row["SKU"],
                "Product": row["Product"],
                "Risk Level": row["Risk_Level"],
                "Reorder Units": int(row["Suggested_Reorder_Qty"]),
                "Estimated Cost (₹)": order_cost,
                "Decision": "Deferred - exceeds remaining budget",
            })

    budget_plan = pd.DataFrame(selected_rows)

    selected_orders = budget_plan[
        budget_plan["Decision"] == "Prioritised within budget"
    ]

    selected_cost = float(
        selected_orders["Estimated Cost (₹)"].sum()
    )

    budget_col1, budget_col2, budget_col3 = st.columns(3)

    budget_col1.metric(
        "Available Budget",
        f"₹{budget:,.0f}",
    )
    budget_col2.metric(
        "Planned Spend",
        f"₹{selected_cost:,.0f}",
    )
    budget_col3.metric(
        "Budget Remaining",
        f"₹{budget - selected_cost:,.0f}",
    )

    st.dataframe(
        budget_plan,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Planning assumption: each recommended product is treated as "
        "an all-or-nothing order. Higher-risk products are considered "
        "first. This is a simple prioritisation heuristic, not an "
        "optimised purchasing plan."
    )
st.caption(
    "Priority is based on the current rule-based risk classification, "
    "projected stock cover, and suggested replenishment. "
    "Validate actions against actual supplier and business conditions."
)
st.caption(
    "StockWise prototype | Uses a rule-based replenishment policy. "
    "Demo data is synthetic. Validate recommendations against "
    "real business data before operational use."
)
