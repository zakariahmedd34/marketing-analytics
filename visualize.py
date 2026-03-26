import sys
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <preprocessed_dataset_path>")
        sys.exit(1)

    dataset_path = sys.argv[1]
    print(f"[VISUALIZE] Loading data from {dataset_path}...")

    df = pd.read_csv(dataset_path)

    required_cols = [
        "Income",
        "Age",
        "Total_Spending",
        "Total_Purchases",
        "Average_Spend",
        "Engagement",
        "Spending_Ratio"
    ]

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns for visualization: {', '.join(missing_cols)}")

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    # Histogram
    sns.histplot(df["Total_Spending"], bins=30, kde=True, ax=axes[0])
    axes[0].set_title("Distribution of Total Spending")
    axes[0].set_xlabel("Total Spending")
    axes[0].set_ylabel("Count")

    # Correlation Heatmap
    corr_cols = [
        "Income",
        "Age",
        "Total_Spending",
        "Total_Purchases",
        "Average_Spend",
        "Engagement",
        "Spending_Ratio"
    ]
    corr_matrix = df[corr_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=axes[1])
    axes[1].set_title("Correlation Heatmap")

    # Scatterplot
    sns.scatterplot(data=df, x="Income", y="Total_Spending", ax=axes[2])
    axes[2].set_title("Income vs Total Spending")
    axes[2].set_xlabel("Income")
    axes[2].set_ylabel("Total Spending")

    plt.tight_layout()
    plt.savefig("summary_plot.png", dpi=300)
    plt.close()

    print("[VISUALIZE] Saved summary_plot.png")
    print("[VISUALIZE] Handing off to cluster.py...")

    subprocess.run(["python", "cluster.py", dataset_path], check=True)


if __name__ == "__main__":
    main()