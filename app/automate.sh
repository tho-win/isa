#!/usr/bin/env bash

while true; 
do
    echo "=========================BEGIN SPARK JOB============================="
    docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/recommendation.py
    echo "=========================FINISH SPARK JOB============================="
    echo "sleeping..."
    sleep 120
done