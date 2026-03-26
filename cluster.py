import sys
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cluster.py <preprocessed_dataset_path>")
        sys.exit(1)

    dataset_path = sys.argv[1]
    print(f"[CLUSTER] Loading data from {dataset_path}...")

    df = pd.read_csv(dataset_path)

    # Try to detect PCA columns flexibly
    pca_cols = [
        col for col in df.columns
        if str(col).strip().lower().startswith("pc")
    ]

    if len(pca_cols) >= 2:
        # Prefer first 3 PCA columns if available
        preferred = [col for col in ["PC1", "PC2", "PC3"] if col in df.columns]
        feature_cols = preferred if len(preferred) >= 2 else pca_cols[:3]
        print(f"[CLUSTER] Using PCA columns: {feature_cols}")
    else:
        # Fallback to meaningful numeric customer features
        candidate_cols = [
            "Income",
            "Age",
            "Total_Spending",
            "Total_Purchases",
            "Average_Spend",
            "Engagement",
            "Spending_Ratio",
            "Recency",
            "Family_Size",
        ]

        feature_cols = [col for col in candidate_cols if col in df.columns]

        if len(feature_cols) < 2:
            raise ValueError(
                "Not enough valid columns found for clustering. "
                "Need at least 2 numeric columns."
            )

        print(f"[CLUSTER] PCA columns not found. Using fallback features: {feature_cols}")

    X = df[feature_cols].copy()

    # Keep only numeric columns and drop missing rows
    X = X.select_dtypes(include="number").dropna()

    if X.shape[1] < 2:
        raise ValueError("Need at least 2 numeric columns for clustering after filtering.")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    best_k = 2
    best_score = -1

    for k in range(2, 7):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)

        if score > best_score:
            best_score = score
            best_k = k

    final_model = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    final_labels = final_model.fit_predict(X_scaled)

    df.loc[X.index, "Cluster"] = final_labels
    df["Cluster"] = df["Cluster"].astype("Int64")
    df.to_csv("data_clustered.csv", index=False)

    counts = df["Cluster"].value_counts().sort_index()

    with open("clusters.txt", "w", encoding="utf-8") as f:
        f.write(f"Chosen k: {best_k}\n")
        f.write(f"Silhouette score: {best_score:.4f}\n\n")
        for cluster_id, count in counts.items():
            f.write(f"Cluster {cluster_id}: {count} samples\n")

    print("[CLUSTER] Saved data_clustered.csv and clusters.txt")


if __name__ == "__main__":
    main()