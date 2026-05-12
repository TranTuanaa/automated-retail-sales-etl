from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Tạo chuỗi kết nối đến PostgreSQL
POSTGRES_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(POSTGRES_URL)

def load_to_postgres(df):
    with engine.connect() as conn:
        # Xóa dữ liệu cũ trước khi load mới (TRUNCATE)
        print("🧹 Đang xóa dữ liệu cũ...")
        conn.execute(text("TRUNCATE TABLE dim_customer RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_product RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_date RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE fact_sales RESTART IDENTITY CASCADE;"))
        conn.commit()

    # 1. Load dim_customer (chỉ lấy unique để tránh duplicate)
    dim_customer = df[['customer_id', 'country']].drop_duplicates(subset=['customer_id'])
    dim_customer.to_sql('dim_customer', engine, if_exists='append', index=False)
    print(f"   ✅ Loaded {len(dim_customer):,} records vào dim_customer")

    # 2. Load dim_product (unique theo stock_code)
    dim_product = df[['stock_code', 'description']].drop_duplicates(subset=['stock_code'])
    dim_product.to_sql('dim_product', engine, if_exists='append', index=False)
    print(f"   ✅ Loaded {len(dim_product):,} records vào dim_product")

    # 3. Load dim_date (tạo từ invoice_date)
    print("   📅 Đang tạo và load dim_date...")
    dim_date = pd.DataFrame({
        'full_date': pd.to_datetime(df['invoice_date'].dt.date)
    }).drop_duplicates(subset=['full_date'])
    
    dim_date['year'] = dim_date['full_date'].dt.year
    dim_date['month'] = dim_date['full_date'].dt.month
    dim_date['day'] = dim_date['full_date'].dt.day
    dim_date['weekday'] = dim_date['full_date'].dt.day_name()
    
    dim_date.to_sql('dim_date', engine, if_exists='append', index=False)
    print(f"   ✅ Loaded {len(dim_date):,} records vào dim_date")

    # 3. Load fact_sales (bảng chính)
    fact_columns = [
        'invoice_no', 'stock_code', 'description', 'quantity',
        'unit_price', 'total_amount', 'customer_id', 'invoice_date',
        'country', 'year', 'month'
    ]
    fact_sales = df[fact_columns]
    fact_sales.to_sql('fact_sales', engine, if_exists='append', index=False)
    print(f"   ✅ Loaded {len(fact_sales):,} records vào fact_sales")

    print("\n🎉 LOAD TO POSTGRESQL HOÀN TẤT!")

if __name__ == "__main__":
    # Test chạy end-to-end
    from extract_transform import extract_and_transform
    df = extract_and_transform()
    load_to_postgres(df)