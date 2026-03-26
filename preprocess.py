import sys
import subprocess
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from exception import CustomException

def main():
    if len(sys.argv) < 2:
        print("Usage: python preprocess.py <dataset_path>")
        sys.exit(1)

    try:
        dataset_path = sys.argv[1]
        print(f"[PREPROCESS] Loading data from {dataset_path}...")

        # Load the raw data passed from ingest.py
        df = pd.read_csv(dataset_path)
    
        # 1. Data Cleaning: handle missing values, remove duplicates.

        print("[PREPROCESS] Cleaning data...")
        # Handle missing values 
        df = df.dropna(subset=['Income'])

        # fix noise in Age column
        df = df[df['Year_Birth'] >= 1940]
        # fix noise in Marital_Status column
        df['Marital_Status'] = df['Marital_Status'].replace({'Alone': 'Single'})
        df = df[~df['Marital_Status'].isin(['Absurd', 'YOLO'])]
        df = df.drop(columns=['Z_CostContact', 'Z_Revenue'])

        # outliers in Income diagnosis
        Q1 = df['Income'].quantile(0.25)
        Q3 = df['Income'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df['Income'] = df['Income'].clip(lower_bound, upper_bound)

        # 2- Feature engineering
        print("[PREPROCESS] Engineering features...")

        df['Total_Spending'] = df[[
            'MntWines', 'MntFruits', 'MntMeatProducts',
            'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
        ]].sum(axis=1)

    
        df['Total_Purchases'] = (
            df['NumWebPurchases'] +
            df['NumCatalogPurchases'] +
            df['NumStorePurchases']
        )
        
        df['Average_Spend'] = df['Total_Spending'] / (df['Total_Purchases'] + 1)

        
        df['Family_Size'] = df['Kidhome'] + df['Teenhome'] + 1

    
        current_year = pd.Timestamp.now().year
        df['Age'] = current_year - df['Year_Birth']

    
        df['Engagement'] = df['Total_Purchases'] / (df['Recency'] + 1)

        
        df['Spending_Ratio'] = df['Total_Spending'] / (df['Income'] + 1)

        # drop unnecessary columns
        cols_to_drop = ['ID', 'Year_Birth']
        df = df.drop(columns=cols_to_drop) 

        # Save the processed results
        cleaned_path = "data_cleaned.csv"
        df.to_csv(cleaned_path, index=False)
        print(f"[PREPROCESS] Saved cleaned data to {cleaned_path}")
        print("[PREPROCESS] Task 1 complete. Starting Task 2...")
        # print("[PREPROCESS] Handing off to analytics.py...")
        # subprocess.run(["python", "analytics.py", cleaned_path])
        print("[PREPROCESS] Starting Task 2...")

        # Start Task 2 from Task 1 output
        df_task2 = pd.read_csv(cleaned_path)

        # 1) Remove duplicates
        print("[PREPROCESS] Removing duplicates...")
        before_rows = len(df_task2)
        df_task2 = df_task2.drop_duplicates().reset_index(drop=True)
        after_rows = len(df_task2)
        print(f"[PREPROCESS] Removed {before_rows - after_rows} duplicate rows.")

        # 2) Inspect and transform Dt_Customer
        print("[PREPROCESS] Transforming Dt_Customer...")
        df_task2["Dt_Customer"] = pd.to_datetime(
            df_task2["Dt_Customer"], errors="coerce"
        )

        if df_task2["Dt_Customer"].isnull().sum() > 0:
            raise ValueError("Dt_Customer contains invalid dates after conversion.")

        reference_date = df_task2["Dt_Customer"].max()
        df_task2["Customer_Days"] = (reference_date - df_task2["Dt_Customer"]).dt.days
        df_task2["Customer_Year"] = df_task2["Dt_Customer"].dt.year
        df_task2["Customer_Month"] = df_task2["Dt_Customer"].dt.month

        # Drop original date column after extracting useful numeric features
        df_task2 = df_task2.drop(columns=["Dt_Customer"])

        # Keep a copy BEFORE encoding/scaling for discretization
        df_for_discretization = df_task2.copy()

        # 3) Encoding categorical columns
        print("[PREPROCESS] Encoding categorical columns...")
        categorical_cols = df_task2.select_dtypes(include=["object"]).columns.tolist()
        df_encoded = pd.get_dummies(
            df_task2, columns=categorical_cols, drop_first=False
        )

        # Convert any boolean dummy columns to integers
        bool_cols = df_encoded.select_dtypes(include=["bool"]).columns.tolist()
        if bool_cols:
            df_encoded[bool_cols] = df_encoded[bool_cols].astype(int)

        # 4) Scaling
        print("[PREPROCESS] Scaling features...")
        scaler = StandardScaler()
        scaled_array = scaler.fit_transform(df_encoded)
        df_scaled = pd.DataFrame(scaled_array, columns=df_encoded.columns)

        # 5) PCA
        print("[PREPROCESS] Applying PCA...")
        pca_full = PCA()
        pca_full.fit(df_scaled)

        explained_variance = pca_full.explained_variance_ratio_
        cumulative_variance = np.cumsum(explained_variance)

        # Minimum number of components to explain at least 90% variance
        n_components_90 = int(np.argmax(cumulative_variance >= 0.90) + 1)

        pca = PCA(n_components=n_components_90)
        pca_result = pca.fit_transform(df_scaled)

        pca_columns = [f"PC{i+1}" for i in range(n_components_90)]
        df_pca = pd.DataFrame(pca_result, columns=pca_columns)

        # 6) Discretization on original meaningful values
        print("[PREPROCESS] Applying discretization...")
        df_for_discretization["Age_Group"] = pd.qcut(
            df_for_discretization["Age"],
            q=3,
            labels=["Young", "Middle_Age", "Senior"],
            duplicates="drop",
        )

        df_for_discretization["Income_Level"] = pd.qcut(
            df_for_discretization["Income"],
            q=3,
            labels=["Low", "Medium", "High"],
            duplicates="drop",
        )

        df_for_discretization["Spending_Level"] = pd.qcut(
            df_for_discretization["Total_Spending"],
            q=3,
            labels=["Low", "Medium", "High"],
            duplicates="drop",
        )

        discretized_cols = df_for_discretization[
            ["Age_Group", "Income_Level", "Spending_Level"]
        ].reset_index(drop=True)

        # 7) Combine encoded data + PCA + discretized columns
        df_preprocessed = pd.concat(
            [
                df_encoded.reset_index(drop=True),
                df_pca.reset_index(drop=True),
                discretized_cols,
            ],
            axis=1,
        )

        # Final check for missing values
        total_missing = int(df_preprocessed.isnull().sum().sum())
        if total_missing > 0:
            raise ValueError(
                f"Final preprocessed dataset contains {total_missing} missing values."
            )

        # Save final Task 2 output
        processed_path = "data_preprocessed.csv"
        df_preprocessed.to_csv(processed_path, index=False)
        print(f"[PREPROCESS] Saved final preprocessed data to {processed_path}")

        # Hand off to analytics.py
        print("[PREPROCESS] Handing off to analytics.py...")
        subprocess.run(["python", "analytics.py", processed_path], check=True)
    except Exception as e:
        raise CustomException(str(e), sys)

if __name__ == "__main__":
    main()