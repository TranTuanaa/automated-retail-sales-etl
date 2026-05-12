from airflow import DAG  # type: ignore
from airflow.providers.standard.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import sys
import os

# FIX ĐƯỜNG DẪN cho Airflow chạy trong Docker
sys.path.insert(0, '/opt/airflow')

from scripts.etl_pipeline import run_etl_pipeline
from scripts.create_table import create_tables

default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'retries': 3,                    
    'retry_delay': timedelta(minutes=2),
    'email_on_failure': False,
}

with DAG(
    dag_id='retail_etl_pipeline',
    default_args=default_args,
    description='Automated Retail Sales ETL Pipeline (Star Schema + PostgreSQL)',
    schedule='0 2 * * *',           # Chạy lúc 2h sáng hàng ngày
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['retail', 'etl', 'postgres', 'star_schema'],
    max_active_runs=1,              # Chỉ cho phép 1 lần chạy cùng lúc
) as dag:
    create_tables_task = PythonOperator(
        task_id='create_tables',
        python_callable=create_tables,
    )

    # Task chính
    run_etl = PythonOperator(
        task_id='run_retail_etl_pipeline',
        python_callable=run_etl_pipeline,
    )

    create_tables_task >> run_etl # type: ignore
