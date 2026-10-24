from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import ETL functions from extract and transform scripts
from extract_jobs import run_extraction
from transform_jobs import run_transformation

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG structure
with DAG(
    'production_jobs_etl_pipeline',
    default_args=default_args,
    description='A production-grade ETL pipeline for job data using Airflow and PostgreSQL',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Extract data from API and load into staging
    extract_task = PythonOperator(
        task_id='extract_raw_jobs_task',
        python_callable=run_extraction,
    )

    # Task 2: Transform staging data and load into transformed table
    transform_task = PythonOperator(
        task_id='transform_clean_jobs_task',
        python_callable=run_transformation,
    )

    # Define task dependency (Extract runs first, then Transform)
    extract_task >> transform_task