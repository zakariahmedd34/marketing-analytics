import sys
import pandas as pd
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
        processed_path = "data_preprocessed.csv"
        df.to_csv(processed_path, index=False)
        print(f"[PREPROCESS] Saved preprocessed data to {processed_path}")
        print("[PREPROCESS] Handing off to analytics.py...")
        # subprocess.run(["python", "analytics.py", processed_path])
    except Exception as e:
        raise CustomException(str(e), sys)

if __name__ == "__main__":
    main()