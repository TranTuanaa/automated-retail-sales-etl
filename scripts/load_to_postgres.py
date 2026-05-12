from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(POSTGRES_URL)

def get_latest_date():

    query = """
    SELECT MAX(invoice_date)
    FROM fact_sales;
    """

    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            latest_date = result.scalar()

        return latest_date

    except Exception as e:
        print(f"❌ Lỗi khi lấy latest date: {e}")
        return None


def load_to_postgres(df):

    print("📤 Bắt đầu load dữ liệu vào PostgreSQL...")

    latest_date = get_latest_date()

    if latest_date:
        print(f"📅 Latest invoice_date trong DB: {latest_date}")
        df = df[df['invoice_date'] > latest_date]
        print(f"🆕 Records mới cần load: {len(df):,}")

    else:
        print("🟢 First run - Load toàn bộ dữ liệu")

    if df.empty:
        print("⚠️ Không có dữ liệu mới để load")
        return

    print("👤 Loading dim_customer...")

    dim_customer = (
        df[['customer_id', 'country']].drop_duplicates(subset=['customer_id'])
    )

    dim_customer.to_sql('dim_customer',engine,if_exists='append',index=False,method='multi')

    print(f"✅ Loaded {len(dim_customer):,} records vào dim_customer")
    print("📦 Loading dim_product...")

    dim_product = (
        df[['stock_code', 'description']].drop_duplicates(subset=['stock_code'])
    )

    dim_product.to_sql('dim_product',engine,if_exists='append',index=False,method='multi')

    print(f"✅ Loaded {len(dim_product):,} records vào dim_product")
    print("📅 Loading dim_date...")

    dim_date = pd.DataFrame({
    'full_date': pd.to_datetime(df['invoice_date'].dt.date)}).drop_duplicates(subset=['full_date'])

    dim_date['year'] = dim_date['full_date'].dt.year
    dim_date['month'] = dim_date['full_date'].dt.month
    dim_date['day'] = dim_date['full_date'].dt.day
    dim_date['weekday'] = dim_date['full_date'].dt.day_name()

    # Thêm cột date_id nếu cần (hoặc để DB tự generate)
    dim_date.to_sql('dim_date', engine, if_exists='append', index=False, method='multi')

    print(f"✅ Loaded {len(dim_date):,} records vào dim_date")
    print("💰 Loading fact_sales...")

    fact_columns = [
        'invoice_no',
        'stock_code',
        'description',
        'quantity',
        'unit_price',
        'total_amount',
        'customer_id',
        'invoice_date',
        'country',
        'year',
        'month'
    ]

    fact_sales = df[fact_columns]
    fact_sales.to_sql(
        'fact_sales',
        engine,
        if_exists='append',
        index=False,
        method='multi'
    )

    print(f"✅ Loaded {len(fact_sales):,} records vào fact_sales")
    print("\n🎉 LOAD TO POSTGRESQL HOÀN TẤT!")

if __name__ == "__main__":
    from extract_transform import extract_and_transform
    df = extract_and_transform()
    load_to_postgres(df)