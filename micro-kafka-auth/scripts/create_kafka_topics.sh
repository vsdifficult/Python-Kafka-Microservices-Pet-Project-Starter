#!/bin/bash

# Ожидаем, пока Kafka станет доступна
echo "Waiting for Kafka to be ready..."
cub kafka-ready -b kafka:9092 1 20

# Создаем необходимые топики
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic user-events
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic post-events
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic feed-updates

echo "Kafka topics created successfully."