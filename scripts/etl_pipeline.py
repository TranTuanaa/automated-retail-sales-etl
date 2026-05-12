from scripts.extract_transform import extract_and_transform
from scripts.load_to_postgres import load_to_postgres
import time

def run_etl_pipeline():
    """Main ETL Pipeline - Chạy đầy đủ Extract → Transform → Load"""
    start_time = time.time()
    print("🚀 BẮT ĐẦU RETAIL ETL PIPELINE...\n")

    # 1. Extract & Transform
    df = extract_and_transform()

    # 2. Load vào PostgreSQL (Star Schema)
    load_to_postgres(df)

    end_time = time.time()
    duration = round(end_time - start_time, 2)
    
    print(f"\n🎉 PIPELINE HOÀN TẤT trong {duration} giây!")
    print("✅ Dữ liệu đã được load vào database `retail_dw`")

if __name__ == "__main__":
    run_etl_pipeline()