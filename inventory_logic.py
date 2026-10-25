
import pandas as pd
import numpy as np


def generate_inventory_data():
    """Create the reproducible 30-product demo dataset."""

    np.random.seed(42)

    products = [
        "Shampoo", "Conditioner", "Face Wash", "Moisturizer",
        "Sunscreen", "Lip Balm", "Body Lotion", "Hand Cream",
        "Toothpaste", "Toothbrush", "Laundry Detergent", "Dish Soap",
        "Floor Cleaner", "Hair Oil", "Serum", "Face Mask",
        "Body Wash", "Deodorant", "Razor", "Cotton Pads",
        "Tissues", "Sanitary Pads", "Baby Wipes", "Baby Lotion",
        "Protein Bar", "Oats", "Coffee", "Green Tea",
        "Water Bottle", "Snack Pack"
    ]

    categories = [
        "Personal Care", "Personal Care", "Personal Care",
        "Personal Care", "Personal Care", "Personal Care",
        "Personal Care", "Personal Care", "Oral Care", "Oral Care",
        "Home Care", "Home Care", "Home Care", "Personal Care",
        "Personal Care", "Personal Care", "Personal Care",
        "Personal Care", "Personal Care", "Personal Care",
        "Home Care", "Personal Care", "Baby Care", "Baby Care",
        "Food", "Food", "Beverages", "Beverages",
        "Accessories", "Food"
    ]

    df = pd.DataFrame({
        "SKU": [f"SKU{i:03d}" for i in range(1, 31)],
        "Product": products,
        "Category": categories,
        "Current_Stock": np.random.randint(5, 150, 30),
        "Avg_Daily_Sales": np.round(
            np.random.uniform(1, 15, 30), 1
        ),
        "Lead_Time_Days": np.random.randint(1, 8, 30),
        "Incoming_Stock": np.random.choice(
            [0, 0, 0, 20, 40, 60], 30
        ),
        "Unit_Cost": np.random.randint(50, 1000, 30)
    })

    return df


def calculate_inventory(df):
    """Calculate inventory risk and replenishment recommendations."""

    df = df.copy()

    df["Days_of_Cover"] = (
        df["Current_Stock"] / df["Avg_Daily_Sales"]
    ).round(1)

    df["Lead_Time_Demand"] = (
        df["Avg_Daily_Sales"] * df["Lead_Time_Days"]
    ).round(1)

    df["Projected_Available_Stock"] = (
        df["Current_Stock"] + df["Incoming_Stock"]
    )

    df["Stock_After_Lead_Time"] = (
        df["Projected_Available_Stock"] - df["Lead_Time_Demand"]
    ).round(1)

    df["Projected_Days_of_Cover"] = (
        df["Projected_Available_Stock"] / df["Avg_Daily_Sales"]
    ).round(1)

    def classify_risk(row):
        if row["Projected_Days_of_Cover"] < row["Lead_Time_Days"]:
            return "High Risk"
        elif row["Projected_Days_of_Cover"] < row["Lead_Time_Days"] + 3:
            return "Medium Risk"
        return "Low Risk"

    df["Risk_Level"] = df.apply(classify_risk, axis=1)

    risk_priority = {
        "High Risk": 1,
        "Medium Risk": 2,
        "Low Risk": 3
    }

    df["Risk_Priority"] = df["Risk_Level"].map(risk_priority)

    safety_stock_days = 2

    df["Safety_Stock"] = np.ceil(
        df["Avg_Daily_Sales"] * safety_stock_days
    ).astype(int)

    df["Target_Stock"] = np.ceil(
        df["Lead_Time_Demand"] + df["Safety_Stock"]
    ).astype(int)

    df["Stock_Position"] = (
        df["Current_Stock"] + df["Incoming_Stock"]
    )

    df["Suggested_Reorder_Qty"] = np.maximum(
        0, df["Target_Stock"] - df["Stock_Position"]
    ).astype(int)

    df["Suggested_Order_Cost"] = (
        df["Suggested_Reorder_Qty"] * df["Unit_Cost"]
    )

    df["Recommendation_Reason"] = np.where(
        df["Suggested_Reorder_Qty"] > 0,
        "Replenishment recommended",
        "No reorder needed under current policy"
    )

    return df
