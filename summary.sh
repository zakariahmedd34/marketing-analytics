#!/bin/bash

CONTAINER_NAME=marketing_analytics_container
HOST_RESULTS_DIR=./results

mkdir -p "$HOST_RESULTS_DIR"

docker cp $CONTAINER_NAME:/app/pipeline/data_raw.csv $HOST_RESULTS_DIR/ 2>/dev/null
docker cp $CONTAINER_NAME:/app/pipeline/data_preprocessed.csv $HOST_RESULTS_DIR/ 2>/dev/null
docker cp $CONTAINER_NAME:/app/pipeline/data_clustered.csv $HOST_RESULTS_DIR/ 2>/dev/null
docker cp $CONTAINER_NAME:/app/pipeline/insight1.txt $HOST_RESULTS_DIR/ 2>/dev/null
docker cp $CONTAINER_NAME:/app/pipeline/insight2.txt $HOST_RESULTS_DIR/ 2>/dev/null
docker cp $CONTAINER_NAME:/app/pipeline/insight3.txt $HOST_RESULTS_DIR/ 2>/dev/null
docker cp $CONTAINER_NAME:/app/pipeline/summary_plot.png $HOST_RESULTS_DIR/ 2>/dev/null
docker cp $CONTAINER_NAME:/app/pipeline/clusters.txt $HOST_RESULTS_DIR/ 2>/dev/null

docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

echo "Outputs copied to results/ and container removed."