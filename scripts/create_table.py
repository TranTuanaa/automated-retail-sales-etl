from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Tạo chuỗi kết nối đến PostgreSQL
POSTGRES_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

# Tạo engine kết nối
engine = create_engine(POSTGRES_URL)

def create_tables():
    """Tạo 4 bảng Star Schema"""
    with engine.connect() as conn:
        print("🔨 Đang tạo các bảng Dimension...")

        # 1. dim_customer
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_customer (
                customer_id BIGINT PRIMARY KEY,
                country VARCHAR(100)
            );
        """))
        print("   ✅ dim_customer created")

        # 2. dim_product
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_product (
                stock_code VARCHAR(50) PRIMARY KEY,
                description TEXT
            );
        """))
        print("   ✅ dim_product created")

        # 3. dim_date
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_date (
                date_id SERIAL PRIMARY KEY,
                full_date DATE UNIQUE NOT NULL,
                year INT,
                month INT,
                day INT,
                weekday VARCHAR(20)
            );
        """))
        print("   ✅ dim_date created")

        # 4. fact_sales (bảng chính)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fact_sales (
                sale_id SERIAL PRIMARY KEY,
                invoice_no VARCHAR(50),
                stock_code VARCHAR(50),
                description TEXT,
                quantity INT,
                unit_price DECIMAL(10,2),
                total_amount DECIMAL(12,2),
                customer_id BIGINT,
                invoice_date TIMESTAMP,
                country VARCHAR(100),
                year INT,
                month INT,
                FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
                FOREIGN KEY (stock_code) REFERENCES dim_product(stock_code)
            );
        """))
        print("   ✅ fact_sales created")

        conn.commit()
        print("\n🎉 ĐÃ TẠO XONG TẤT CẢ 4 BẢNG STAR SCHEMA!")

if __name__ == "__main__":
    create_tables()