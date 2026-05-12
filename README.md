# Automated Retail Sales ETL

A simple data engineering project that automates a retail ETL pipeline using Python, Airflow, PostgreSQL, and Docker.

## What this project does

This pipeline:

- reads retail data from `Online Retail.xlsx`
- cleans and transforms the data with Pandas
- creates a simple star schema in PostgreSQL
- loads the data into dimension tables and a fact table
- runs through an Airflow DAG

## Tools used

- Python
- Pandas
- Apache Airflow
- PostgreSQL
- Docker Compose
- SQLAlchemy

## Data model

The warehouse includes:

- `dim_customer`
- `dim_product`
- `dim_date`
- `fact_sales`

## Project structure

```text
automated-retail-sales-etl/
├── dags/
├── scripts/
├── data/
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

## How to run
1. Start the services
```
docker compose up -d
```
2. Open Airflow UI at:
```
http://localhost:8080
```
 - Login: airflow / airflow
3. Trigger the DAG: retail_etl_pipeline
## Notes
 - The pipeline currently uses a full refresh approach
 - The source data is a local Excel file
 - This project was built for practicing ETL, Airflow, and basic warehouse design
## Author
 - Trần Anh Tuấn Sinh viên Toán Ứng dụng (TDTU)