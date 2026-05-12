from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(POSTGRES_URL)


def load_to_postgres(df):

    print("Bat dau load du lieu vao PostgreSQL...")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE dim_customer RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE dim_product RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE dim_date RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE fact_sales RESTART IDENTITY CASCADE"))

    print("Full refresh - Load toan bo du lieu")

    if df.empty:
        print("Khong co du lieu de load")
        return

    print("Loading dim_customer...")

    dim_customer = (
        df[['customer_id', 'country']].drop_duplicates(subset=['customer_id'])
    )

    dim_customer.to_sql('dim_customer', engine, if_exists='append', index=False, method='multi')

    print(f"Loaded {len(dim_customer):,} records vao dim_customer")
    print("Loading dim_product...")

    dim_product = (
        df[['stock_code', 'description']].drop_duplicates(subset=['stock_code'])
    )

    dim_product.to_sql('dim_product', engine, if_exists='append', index=False, method='multi')

    print(f"Loaded {len(dim_product):,} records vao dim_product")
    print("Loading dim_date...")

    dim_date = pd.DataFrame({
        'full_date': pd.to_datetime(df['invoice_date'].dt.date)
    }).drop_duplicates(subset=['full_date'])

    dim_date['year'] = dim_date['full_date'].dt.year
    dim_date['month'] = dim_date['full_date'].dt.month
    dim_date['day'] = dim_date['full_date'].dt.day
    dim_date['weekday'] = dim_date['full_date'].dt.day_name()
    dim_date['quarter'] = dim_date['full_date'].dt.quarter
    dim_date['is_weekend'] = dim_date['full_date'].dt.weekday >= 5

    dim_date.to_sql('dim_date', engine, if_exists='append', index=False, method='multi')

    print(f"Loaded {len(dim_date):,} records vao dim_date")
    print("Loading fact_sales...")

    date_lookup = pd.read_sql("SELECT date_id, full_date FROM dim_date", engine)
    date_lookup['full_date'] = pd.to_datetime(date_lookup['full_date'])

    fact_sales = df.copy()
    fact_sales['full_date'] = pd.to_datetime(fact_sales['invoice_date'].dt.date)
    fact_sales = fact_sales.merge(date_lookup, on='full_date', how='left')

    if fact_sales['date_id'].isna().any():
        raise ValueError("Khong map duoc date_id cho mot so invoice_date")

    fact_sales['date_id'] = fact_sales['date_id'].astype('int64')

    fact_columns = [
        'invoice_no',
        'stock_code',
        'quantity',
        'unit_price',
        'total_amount',
        'customer_id',
        'date_id'
    ]

    fact_sales = fact_sales[fact_columns]
    fact_sales.to_sql(
        'fact_sales',
        engine,
        if_exists='append',
        index=False,
        method='multi'
    )

    print(f"Loaded {len(fact_sales):,} records vao fact_sales")
    print("\nLOAD TO POSTGRESQL HOAN TAT!")


if __name__ == "__main__":
    from extract_transform import extract_and_transform
    df = extract_and_transform()
    load_to_postgres(df)
