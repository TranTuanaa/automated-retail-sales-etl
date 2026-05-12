# Retail Sales ETL Pipeline with Apache Airflow

**Project 2** – Automated Retail ETL Pipeline

Mình nâng cấp từ Project 1 (script Python thủ công) lên pipeline ETL tự động chạy bằng Apache Airflow.

### Tech Stack
- Python + Pandas
- Apache Airflow (DAG)
- PostgreSQL
- Docker & Docker Compose
- SQLAlchemy

### Những gì đã làm
- Xây dựng ETL end-to-end (Extract → Transform → Load)
- Thiết kế Star Schema (fact_sales + dim_customer, dim_product, dim_date)
- Tạo DAG Airflow chạy theo lịch tự động
- Sử dụng Docker để chạy môi trường

### Cách chạy
1. Khởi động Docker:
   ```bash
   docker compose up -d
   ```
2. Truy cập Airflow UI: http://localhost:8080
 - (Username/Password: airflow / airflow)
 - Vào Dags → tìm retail_etl_pipeline → bật toggle và Trigger

### Cấu trúc thư mục
 - dags/ → chứa DAG Airflow
 - scripts/ → code ETL
 - data/ → file Excel nguồn

### Author: 
 - Trần Anh Tuấn
 - Sinh viên Toán Ứng Dụng - (TDTU)