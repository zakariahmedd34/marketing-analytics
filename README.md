# Marketing Analytics Pipeline

This project implements a full customer analytics pipeline using Python and Docker. It processes a marketing dataset to generate textual insights, visual summaries, and customer segmentation through K-Means clustering.

## Team Members

- Zakaria Ahmed
- Salma Ghonim
- Yasmin Radwan

## Project Structure

```text
marketing-analytics/
├── Dockerfile
├── ingest.py
├── preprocess.py
├── analytics.py
├── visualize.py
├── cluster.py
├── summary.sh
├── README.md
├── data/
│   └── data_preprocessed.csv
└── results/

## Requirements

The project uses the following Python libraries:

pandas
numpy
matplotlib
seaborn
scikit-learn
scipy
openpyxl
Docker Setup
Build Docker Image
docker build -t marketing-analytics .
Run Container
docker run -it --name marketing_analytics_container marketing-analytics
Run Pipeline

## Inside the container:

python analytics.py data/data_preprocessed.csv
Export Results to Host

## After exiting the container:
./summary.sh
## Execution Flow
ingest.py → preprocess.py → analytics.py → visualize.py → cluster.py


Each Python script calls the next stage and passes the latest dataset path as argument.

## Outputs

The pipeline generates the following outputs:

data_preprocessed.csv → processed dataset
data_clustered.csv → dataset with assigned cluster labels
insight1.txt → insight about income and spending
insight2.txt → insight about age and purchases
insight3.txt → insight about response and engagement
summary_plot.png → visualization summary
clusters.txt → number of samples per cluster

## Example Insights
Higher income customers spend significantly more than lower income customers.
Senior customers tend to make more purchases than younger customers.
High-spending customers show higher marketing response and engagement.


GitHub Repository


Docker Hub
https://hub.docker.com/repository/docker/yasminradwan/marketing-analytics/general

Notes
The pipeline was tested locally with:
python3 analytics.py data/data_preprocessed.csv
Clustering uses PCA columns (PC1, PC2, PC3) when available.
Result files are copied from the Docker container to the host using summary.sh.
