# 🚗 Smart City Real-Time Streaming System

A **real-time streaming architecture** that simulates and processes live data from a **Smart City** environment using **Apache Kafka**, **Apache Spark Structured Streaming**, and **AWS S3**.

This project demonstrates how IoT data — such as **vehicle telemetry**, **GPS tracking**, **traffic cameras**, **weather conditions**, and **emergency incidents** — can be ingested, processed, and stored in the cloud for analytics.

---

## 📚 Table of Contents

- [📖 Overview](#-overview)
- [🏗️ System Architecture](#️-system-architecture)
- [🧠 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ How It Works](#️-how-it-works)
- [💾 Data Schemas](#-data-schemas)
- [🔧 Configuration](#-configuration)
- [🧰 Dependencies](#-dependencies)
- [🧩 Troubleshooting](#-troubleshooting)
- [🚀 Future Improvements](#-future-improvements)
- [👤 Author](#-author)

---

## 📖 Overview

The **Smart City Streaming System** simulates vehicles traveling from **London** to **Birmingham**, generating continuous real-time data for:

- 🚘 Vehicle telemetry  
- 🛰️ GPS tracking  
- 🚦 Traffic camera data  
- 🌦️ Weather conditions  
- 🚑 Emergency incidents  

These data streams are sent to **Kafka topics**, consumed by **Spark Structured Streaming**, and stored in **AWS S3** in **Parquet** format for analytics.

---

## 🏗️ System Architecture

```plaintext
+-------------------+
|  Data Simulator   |
| (Python Producer) |
+--------+----------+
         |
         v
  +---------------+
  |   Kafka       |
  |   Topics       |
  +---------------+
         |
         v
  +---------------+
  |   Spark       |
  |   Streaming    |
  +---------------+
         |
         v
  +---------------+
  |    AWS S3     |
  |  (Data Lake)  |
  +---------------+
```
---
## 🧠 Tech Stack

Component	Technology
Data Simulation	Python (confluent_kafka)
Messaging	Apache Kafka (Dockerized)
Stream Processing	Apache Spark 3.5.0
Storage	AWS S3
Containerization	Docker & Docker Compose
Cloud Credentials	Hadoop AWS Connector

## 📁 Project Structure

```
smart-city-streaming/
├── jobs/
│   ├── producer.py          # Kafka data generator
│   ├── spark-city.py        # Spark Streaming job
│   ├── main.py              # Spark entry script
│   ├── config.py            # AWS credentials and configuration
├── docker-compose.yml       # Cluster setup (Kafka + Spark)
└── README.md                # Project documentation

```
## ⚙️ How It Works
## 🧱 Step 1 — Start the Cluster

Start Kafka and Spark containers:

docker-compose up -d


This will run:

Zookeeper

Kafka Broker

Spark Master

Spark Worker Nodes

## 🚗 Step 2 — Start Data Producer
Run the Python simulator:
```
python jobs/producer.py
```
This will simulate real-time vehicle data traveling from London to Birmingham and push messages into Kafka topics.

## 🔥 Step 3 — Start Spark Structured Streaming

Run your Spark job inside the master container:
```
docker exec -it spark-master spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.901 \
  --master spark://spark-master:7077 \
  jobs/spark-city.py
```
Spark will:
Consume JSON data from Kafka
Apply predefined schemas
Write the structured data to AWS S3 in Parquet format

## ☁️ Step 4 — Verify Data in AWS S3

Check your AWS S3 bucket for new folders:
s3a://smartcity-spark-streaming-data-01/data/
├── vehicle_data/
├── gps_data/
├── traffic_data/
├── weather_data/
└── emergency_data/

## 🔧 Configuration

Edit config.py to add your AWS credentials:

configuration = {
  "AWS_ACCESS_KEY": "your_aws_access_key",
  "AWS_SECRET_KEY": "your_aws_secret_key"
}


Kafka topics and bootstrap servers are set as environment variables:

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
VEHICLE_TOPIC=vehicle_data
GPS_TOPIC=gps_data
TRAFFIC_TOPIC=traffic_data
WEATHER_TOPIC=weather_data
EMERGENCY_TOPIC=emergency_data

## 🧰 Dependencies
Install Python dependencies locally:
pip install confluent-kafka boto3
Spark and Kafka dependencies are handled within Docker images.
