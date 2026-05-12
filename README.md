# Retail Sales ETL Pipeline with Apache Airflow

Project này tự động hóa quy trình ETL cho bộ dữ liệu bán lẻ. Pipeline đọc file `Online Retail.xlsx`, làm sạch dữ liệu bằng Pandas, rồi load vào PostgreSQL theo mô hình star schema. Airflow được dùng để điều phối và lên lịch chạy.

### Tech Stack
- Python
- Pandas
- Apache Airflow
- PostgreSQL
- Docker Compose
- SQLAlchemy

### Cách chạy
1. Chạy Docker:
   ```bash
   docker compose up -d
   ```
2. Truy cập Airflow UI tại `http://localhost:8080`
3. Đăng nhập bằng `airflow / airflow`
4. Trigger DAG `retail_etl_pipeline`

### Cấu trúc thư mục
- `dags/` chứa DAG Airflow
- `scripts/` chứa code ETL
- `data/` chứa file Excel đầu vào

### Tác giả
Trần Anh Tuấn - Sinh viên Toán Ứng dụng (TDTU)
