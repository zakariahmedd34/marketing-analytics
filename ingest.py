import sys
import pandas as pd
import subprocess
from exception import CustomException

def main():
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <dataset_path>")
        sys.exit(1)

    dataset_path = sys.argv[1]

    print("[INGEST] Loading dataset...")

    try:
        if dataset_path.endswith(".xlsx"):
            df = pd.read_excel(dataset_path)
        else:
            df = pd.read_csv(dataset_path)

        raw_path = "data_raw.csv"
        df.to_csv(raw_path, index=False)

        print(f"[INGEST] Saved raw data to {raw_path}")

        subprocess.run(["python", "preprocess.py", "data_raw.csv"])

    except Exception as e:
        raise CustomException(str(e), sys)

if __name__ == "__main__":
    main()