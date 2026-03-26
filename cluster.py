import sys
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


def main():
    if len(sys.argv) < 2:
        print("Usage: python cluster.py <preprocessed_dataset_path>")
        sys.exit(1)

    dataset_path = sys.argv[1]
    print(f"[CLUSTER] Loading data from {dataset_path}...")

    df = pd.read_csv(dataset_path, skiprows=1)

    # Use PCA columns if they exist
    pca_cols = [col for col in df.columns if str(col).startswith("PC")]

    if len(pca_cols) >= 2:
        # Use first 3 PCs if available, otherwise all existing PCA columns
        feature_cols = ["PC1", "PC2", "PC3"] if all(pc in pca_cols for pc in ["PC1", "PC2", "PC3"]) else pca_cols
        print(f"[CLUSTER] Using PCA columns: {feature_cols}")
    else:
        raise ValueError("PCA columns not found in dataset. Expected columns like PC1, PC2, PC3.")

    X = df[feature_cols].dropna()

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