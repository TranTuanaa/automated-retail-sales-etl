from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from datetime import datetime

# Load biến môi trường
load_dotenv()

# Cải thiện: Kiểm tra các biến môi trường quan trọng trước
required_env = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 
                'POSTGRES_PORT', 'POSTGRES_DB']
for var in required_env:
    if not os.getenv(var):
        raise ValueError(f"Missing environment variable: {var}")

# Tạo chuỗi kết nối
POSTGRES_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(POSTGRES_URL, echo=False)  # echo=False để gọn log hơn

def create_tables():
    """Tạo các bảng Star Schema với cải tiến"""
    try:
        with engine.connect() as conn:
            print("🔨 Đang tạo các bảng Dimension và Fact...")

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

            # 3. dim_date - Cải thiện thêm nhiều cột hữu ích
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS dim_date (
                    date_id SERIAL PRIMARY KEY,
                    full_date DATE UNIQUE NOT NULL,
                    year INT NOT NULL,
                    month INT NOT NULL,
                    day INT NOT NULL,
                    weekday VARCHAR(20),
                    quarter INT,
                    is_weekend BOOLEAN
                );
            """))
            print("   ✅ dim_date created (with extra columns)")

            # 4. fact_sales - Chuẩn hóa Star Schema (chỉ giữ FK)
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS fact_sales (
                    sale_id SERIAL PRIMARY KEY,
                    invoice_no VARCHAR(50),
                    stock_code VARCHAR(50),
                    quantity INT,
                    unit_price DECIMAL(10,2),
                    total_amount DECIMAL(12,2),
                    customer_id BIGINT,
                    date_id INT,
                    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id) ON DELETE SET NULL,
                    FOREIGN KEY (stock_code) REFERENCES dim_product(stock_code) ON DELETE SET NULL,
                    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
                );
            """))
            print("   ✅ fact_sales created (Star Schema optimized)")

            conn.commit()
            print("\n🎉 ĐÃ TẠO HOÀN THÀNH TẤT CẢ CÁC BẢNG!")
            print(f"   Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"❌ Lỗi khi tạo bảng: {e}")
        raise

if __name__ == "__main__":
    create_tables()