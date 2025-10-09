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
