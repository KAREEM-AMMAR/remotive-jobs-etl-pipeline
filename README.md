# 🚀 Production-Grade Automated ETL Data Pipeline

An end-to-end, containerized Data Engineering ETL pipeline that extracts remote job data from external REST APIs, ingests raw records into a PostgreSQL staging environment, cleans and normalizes the datasets, and loads them into a production-grade Data Warehouse. Fully automated and orchestrated using Apache Airflow within a Docker container environment.

---

## 🏛️ System Architecture

The pipeline consists of four containerized services managed seamlessly via `docker-compose`:

    +-----------------------------------------------------------------------+
    |                            Docker Host                                |
    |                                                                       |
    |  +--------------------+             +------------------------------+  |
    |  |    Remotive API    | (External)  |         pgAdmin GUI          |  |
    |  +---------+----------+             +--------------+---------------+  |
    |            |                                       |                  |
    |            v                                       v                  |
    |  +---------+----------+   bridge    +--------------+---------------+  |
    |  |  Airflow Webserver | <---------> |      PostgreSQL Database     |  |
    |  |   & Scheduler      |  network    |       (Data Warehouse)       |  |
    |  +--------------------+             +------------------------------+  |
    +-----------------------------------------------------------------------+

1. **Airflow Webserver & Scheduler:** Handles pipeline scheduling, task orchestration, DAG execution monitoring, and dependency management.
2. **PostgreSQL Database:** serves as the primary Data Warehouse hosting both the `staging_jobs` (raw ingestion) and `transformed_jobs` (cleaned production data) schemas.
3. **pgAdmin 4:** Web-based interface for managing, inspecting, and querying PostgreSQL database tables.

---

## 🛠️ Tech Stack & Key Features

* **Orchestration:** Apache Airflow (Python-based DAGs)
* **Infrastructure & Containerization:** Docker, Docker Compose
* **Data Storage / Warehouse:** PostgreSQL 15, pgAdmin 4
* **Language & Libraries:** Python 3.10, Pandas, Psycopg2, Requests
* **Design Patterns:**
  * **Two-Stage Ingestion Strategy:** Staging Schema for raw API payloads + Production Schema for clean analytics.
  * **Idempotency & Conflict Handling:** Prevents duplicate job record insertion using `ON CONFLICT DO NOTHING`.
  * **Environment Isolation:** Zero local dependency issues via bridged Docker networking (`airflow-net`).

---

## 📂 Repository Structure

    remotive-jobs-etl-pipeline/
    ├── dags/
    │   ├── extract_jobs.py       # API Data Extraction & Staging Load logic
    │   ├── transform_jobs.py     # Data Cleaning & Production Load logic
    │   └── jobs_dag.py           # Airflow DAG definition & Task Dependency
    ├── docker-compose.yml        # Docker infrastructure multi-container setup
    ├── .gitignore                # Git exclusions (logs, pycache)
    └── README.md                 # Complete Project Documentation

---

## ⚡ Quick Start & Deployment

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* Git installed on your system.

### Running the Pipeline

1. **Clone this repository:**
   git clone https://github.com/KAREEM-AMMAR/remotive-jobs-etl-pipeline.git
   cd remotive-jobs-etl-pipeline

2. **Start the containerized services:**
   docker-compose up -d

3. **Initialize Airflow Database & Admin User:**
   docker exec -it airflow_webserver airflow db migrate
   docker exec -it airflow_webserver airflow users create --username airflow --password airflow --firstname Admin --lastname User --role Admin --email admin@example.com

4. **Access Airflow UI:**
   Open `http://localhost:8080` in your browser (Credentials: `airflow` / `airflow`) and enable the `production_jobs_etl_pipeline` DAG!