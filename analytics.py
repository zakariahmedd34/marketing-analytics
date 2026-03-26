import sys
import subprocess
import pandas as pd

from exception import CustomException


def main():
    if len(sys.argv) < 2:
        print("Usage: python analytics.py <preprocessed_dataset_path>")
        sys.exit(1)

    try:
        dataset_path = sys.argv[1]
        print(f"[ANALYTICS] Loading data from {dataset_path}...")

        df = pd.read_csv(dataset_path)

        required_cols = [
            "Income_Level",
            "Total_Spending",
            "Age_Group",
            "Total_Purchases",
            "Spending_Level",
            "Response",
            "Engagement",
        ]

        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(
                f"Missing required columns for analytics: {', '.join(missing_cols)}"
            )
        # Insight 1
        # Which Income_Level has the highest average Total_Spending?
        print("[ANALYTICS] Generating Insight 1...")

        spending_by_income = (
            df.groupby("Income_Level")["Total_Spending"]
            .mean()
            .sort_values(ascending=False)
        )

        top_income_group = spending_by_income.idxmax()
        top_income_value = spending_by_income.max()

        lowest_income_group = spending_by_income.idxmin()
        lowest_income_value = spending_by_income.min()

        insight1 = (
            f"Insight 1:\n"
            f"Customers in the {top_income_group} income group have the highest average total spending "
            f"({top_income_value:.2f}), while customers in the {lowest_income_group} income group have the lowest "
            f"average total spending ({lowest_income_value:.2f}). "
            f"This suggests that income level is strongly associated with customer spending behavior."
        )
        # Insight 2
        # Which Age_Group has the highest average Total_Purchases?
        print("[ANALYTICS] Generating Insight 2...")

        purchases_by_age = (
            df.groupby("Age_Group")["Total_Purchases"]
            .mean()
            .sort_values(ascending=False)
        )

        top_age_group = purchases_by_age.idxmax()
        top_age_value = purchases_by_age.max()

        lowest_age_group = purchases_by_age.idxmin()
        lowest_age_value = purchases_by_age.min()

        insight2 = (
            f"Insight 2:\n"
            f"The {top_age_group} age group has the highest average total number of purchases "
            f"({top_age_value:.2f}), while the {lowest_age_group} age group has the lowest "
            f"average total number of purchases ({lowest_age_value:.2f}). "
            f"This suggests that customer age is related to purchase activity."
        )
        # Insight 3
        # Which Spending_Level has the highest average Response and Engagement?
        print("[ANALYTICS] Generating Insight 3...")

        response_engagement_by_spending = (
            df.groupby("Spending_Level")[["Response", "Engagement"]]
            .mean()
            .sort_values(by="Response", ascending=False)
        )

        top_response_group = response_engagement_by_spending["Response"].idxmax()
        top_response_value = response_engagement_by_spending["Response"].max()

        top_engagement_group = response_engagement_by_spending["Engagement"].idxmax()
        top_engagement_value = response_engagement_by_spending["Engagement"].max()

        if top_response_group == top_engagement_group:
            insight3 = (
                f"Insight 3:\n"
                f"Customers in the {top_response_group} spending group have the highest average response rate "
                f"({top_response_value:.4f}) and the highest average engagement ({top_engagement_value:.4f}). "
                f"This indicates that stronger spending behavior is associated with greater responsiveness and "
                f"engagement in marketing campaigns."
            )
        else:
            insight3 = (
                f"Insight 3:\n"
                f"Customers in the {top_response_group} spending group have the highest average response rate "
                f"({top_response_value:.4f}), while customers in the {top_engagement_group} spending group show "
                f"the highest average engagement ({top_engagement_value:.4f}). "
                f"This indicates that spending behavior is associated with both responsiveness and engagement in "
                f"marketing campaigns."
            )
        # Save insight files
        print("[ANALYTICS] Saving insight text files...")

        with open("insight1.txt", "w", encoding="utf-8") as f:
            f.write(insight1)

        with open("insight2.txt", "w", encoding="utf-8") as f:
            f.write(insight2)

        with open("insight3.txt", "w", encoding="utf-8") as f:
            f.write(insight3)

        print("[ANALYTICS] Saved insight1.txt, insight2.txt, and insight3.txt")

        print("\n" + insight1 + "\n")
        print(insight2 + "\n")
        print(insight3 + "\n")

        # Hand off to visualize.py
        print("[ANALYTICS] Handing off to visualize.py...")
        subprocess.run(["python3", "visualize.py", dataset_path], check=True)

    except Exception as e:
        raise CustomException(str(e), sys)


if __name__ == "__main__":
    main()