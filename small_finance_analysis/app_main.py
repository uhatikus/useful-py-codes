import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog


output_directory = "output"
os.makedirs(output_directory, exist_ok=True)


def load_data():
    orders_path = filedialog.askopenfilename(
        title="Select Orders Excel File", filetypes=[("Excel Files", "*.xlsx")]
    )
    currency_rates_path = filedialog.askopenfilename(
        title="Select Currency Rates Excel File", filetypes=[("Excel Files", "*.xlsx")]
    )
    affiliate_rates_path = filedialog.askopenfilename(
        title="Select Affiliate Rates Excel File", filetypes=[("Excel Files", "*.xlsx")]
    )

    if orders_path and currency_rates_path and affiliate_rates_path:
        process_data(orders_path, currency_rates_path, affiliate_rates_path)
    else:
        status_label.config(text="Please select all input files.")


def process_data(orders_path, currency_rates_path, affiliate_rates_path):
    # Load data and perform processing
    orders_df = pd.read_excel(orders_path)
    currency_rates_df = pd.read_excel(currency_rates_path)
    affiliate_rates_df = pd.read_excel(affiliate_rates_path)

    # Handle duplicates, typos, and missing values if necessary

    # Step 2: Convert “Order Amount” into EUR applying provided currency rates
    currency_rates_df["date"] = pd.to_datetime(currency_rates_df["date"])
    merged_df = pd.merge(
        orders_df, currency_rates_df, left_on="Order Date", right_on="date", how="left"
    )

    # Handle missing currency rates
    merged_df["USD"].ffill(inplace=True)
    merged_df["GBP"].ffill(inplace=True)

    # Convert “Order Amount” into EUR
    merged_df["Order Amount (EUR)"] = merged_df["Order Amount"] / merged_df["USD"]

    # Step 3: Calculate fees for each order using appropriate affiliate rates
    def calculate_fees(row):
        affiliate_id = row["Affiliate ID"]

        # Filter affiliate rates for the given affiliate ID
        affiliate_rate = affiliate_rates_df[
            (affiliate_rates_df["Affiliate ID"] == affiliate_id)
            & (affiliate_rates_df["Start Date"] <= row["Order Date"])
        ]

        # Check if there are applicable rates, otherwise use default values
        if not affiliate_rate.empty:
            affiliate_rate = affiliate_rate.sort_values(
                "Start Date", ascending=False
            ).iloc[0]
        else:
            # Use default values or raise an error based on your requirements
            affiliate_rate = {
                "Processing Rate": 0,
                "Refund Fee": 0,
                "Chargeback Fee": 0,
            }

        processing_fee = row["Order Amount (EUR)"] * affiliate_rate["Processing Rate"]
        refund_fee = (
            affiliate_rate["Refund Fee"] if row["Order Status"] == "Refunded" else 0
        )
        chargeback_fee = (
            affiliate_rate["Chargeback Fee"]
            if row["Order Status"] == "Chargeback"
            else 0
        )

        return pd.Series(
            {
                "Processing Fee": processing_fee,
                "Refund Fee": refund_fee,
                "Chargeback Fee": chargeback_fee,
            }
        )

    fees_df = merged_df.apply(calculate_fees, axis=1)
    merged_df = pd.concat([merged_df, fees_df], axis=1)

    # Step 4: Generate a weekly aggregation for each affiliate and save an excel report
    for affiliate_id, affiliate_name in zip(
        affiliate_rates_df["Affiliate ID"], affiliate_rates_df["Affiliate Name"]
    ):
        affiliate_orders = merged_df[
            merged_df["Affiliate ID"] == affiliate_id
        ].copy()  # Create a copy to avoid SettingWithCopyWarning
        affiliate_orders["Week"] = affiliate_orders["Order Date"].dt.to_period("W-Sun")

        weekly_aggregation = (
            affiliate_orders.groupby("Week")
            .agg(
                {
                    "Order Number": "count",
                    "Order Amount (EUR)": "sum",
                    "Processing Fee": "sum",
                    "Refund Fee": "sum",
                    "Chargeback Fee": "sum",
                }
            )
            .reset_index()
        )

        weekly_aggregation.to_excel(f"output/{affiliate_name}.xlsx", index=False)

        # Display success message
        status_label.config(text="Data processing complete!")


# GUI setup
root = tk.Tk()
root.title("Data Processing Application")

load_button = tk.Button(root, text="Start", command=load_data)
load_button.pack(pady=20)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
