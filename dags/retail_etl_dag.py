from airflow import DAG  # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import sys
import os

# FIX ĐƯỜNG DẪN cho Airflow chạy trong Docker
sys.path.insert(0, '/opt/airflow')

from scripts.etl_pipeline import run_etl_pipeline

default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'retries': 3,                    # Tăng retry lên 3
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

    # Task chính
    run_etl = PythonOperator(
        task_id='run_retail_etl_pipeline',
        python_callable=run_etl_pipeline,
        provide_context=True,       # Hỗ trợ lấy context nếu sau này cần
    )

    # Có thể thêm task create_tables sau này
    run_etl # type: ignore