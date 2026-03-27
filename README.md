# Marketing Analytics Pipeline

This project implements a full customer analytics machine learning pipeline using Python and Docker. It processes a marketing dataset to generate structural insights, visual summaries, and customer segmentations through K-Means clustering.

## Team Members

- Zakaria Ahmed
- Salma Ghonim
- Yasmin Radwan

## Project Structure

```text
marketing-analytics/
├── Dockerfile
├── requirements.txt
├── ingest.py
├── preprocess.py
├── analytics.py
├── visualize.py
├── cluster.py
├── summary.sh
├── README.md
├── .gitignore
├── data/
│   ├── marketing_campaign.xlsx
│   ├── data_preprocessed.csv
│   └── *.ipynb (Analysis notebooks)
└── results/
    └── (Outputs generated here after running the pipeline)
```

<<<<<<< HEAD
## Pipeline Execution Flow
The pipeline follows a sequential execution model:
1. `ingest.py` → Loads raw data and passes it to preprocessing.
2. `preprocess.py` → Cleans the data, performs feature engineering, handles missing values, and saves `data_preprocessed.csv`.
3. `analytics.py` → Extracts 3 key business insights based on spending, age, and engagement grouping, then saves text files.
4. `visualize.py` → Generates correlational and distributional visualizations and saves `summary_plot.png`.
5. `cluster.py` → Executes PCA clustering (K-Means), saves silhouette scores and clustered data.
=======
## Requirements
>>>>>>> 870066d (Final pipeline fixes, summary.sh corrections, and execution flow update)

Each Python script explicitly calls the next stage, meaning running the entrypoint triggers the entire downstream pipeline.

## How to Run Locally

First, install the necessary requirements:

```bash
pip install -r requirements.txt
```

To run the complete pipeline from scratch, starting with ingestion:

```bash
python ingest.py data/marketing_campaign.xlsx
```

Alternatively, to start from the preprocessed data (skipping ingestion and preprocessing):

```bash
python analytics.py data/data_preprocessed.csv
```

Outputs will be generated in your current working directory.

## How to Run using Docker

A `Dockerfile` is provided so you can run the pipeline inside an isolated container.

### 1. Build the Docker Image
```bash
docker build -t marketing-analytics .
```

### 2. Run the Container
Start an interactive shell session inside the container:
```bash
docker run -it --name marketing_analytics_container marketing-analytics
```

### 3. Run the Pipeline inside Docker
Once inside the running container, trigger the full pipeline starting with ingestion:
```bash
python ingest.py data/marketing_campaign.xlsx
```
*(Optionally, type `exit` to return to your host machine.)*

### 4. Export Results
From your host machine, run `summary.sh` to extract the generated insight files, plots, and clustered datasets into the locally synced `./results/` folder, which will then subsequently clean up the Docker container for you:
```bash
./summary.sh
```

## Expected Outputs in `results/`

- `data_preprocessed.csv` → The post-cleaning dataset.
- `data_clustered.csv` → The dataset appended with K-Means cluster labels.
- `insight1.txt` → Structural insights correlating income & spending.
- `insight2.txt` → Structural insights correlating age & purchases.
- `insight3.txt` → Structural insights correlating responses & engagement.
- `summary_plot.png` → The visualizations produced.
- `clusters.txt` → Contains silhouette metrics and cluster sample counts.

## Docker Hub Image
https://hub.docker.com/repository/docker/yasminradwan/marketing-analytics/general
