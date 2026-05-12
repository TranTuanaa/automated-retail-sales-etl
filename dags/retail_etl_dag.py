from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import sys

# FIX ĐƯỜNG DẪN CHO AIRFLOW DOCKER
sys.path.insert(0, '/opt/airflow')

from scripts.etl_pipeline import run_etl_pipeline

default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='retail_etl_pipeline',
    default_args=default_args,
    description='Automated Retail Sales ETL Pipeline (Star Schema + PostgreSQL)',
    schedule='0 2 * * *',      # Chạy lúc 2h sáng hàng ngày
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['retail', 'etl', 'postgres'],
) as dag:

    run_etl = PythonOperator(
        task_id='run_retail_etl_pipeline',
        python_callable=run_etl_pipeline,
    )

    run_etl # type: ignore