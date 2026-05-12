import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def extract_and_transform():
    """Extract từ Excel + Transform dữ liệu"""
    print("📥 Bắt đầu Extract dữ liệu từ Excel...")

    # === Đọc đường dẫn từ .env (dễ thay đổi sau này) ===
    data_folder = os.getenv('DATA_FOLDER', 'data')
    file_name = os.getenv('SOURCE_FILE', 'Online Retail.xlsx')
    
    # Tạo đường dẫn đầy đủ
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, data_folder, file_name)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Không tìm thấy file: {data_path}")

    # Extract
    print(f"   Đang đọc file: {file_name}")
    df = pd.read_excel(data_path)
    print(f"   ✅ Đọc xong {len(df):,} records")

    # ==================== TRANSFORM ====================
    print("🔄 Đang Transform và làm sạch dữ liệu...")

    # 1. Xóa dòng thiếu CustomerID
    df = df.dropna(subset=['CustomerID'])

    # 2. Xóa duplicate
    df = df.drop_duplicates()

    # 3. Lọc dữ liệu hợp lệ
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

    # 4. Tính TotalAmount
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

    # 5. Chuyển kiểu dữ liệu
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['CustomerID'] = df['CustomerID'].astype('int64')

    # 6. Thêm cột Year, Month
    df['year'] = df['InvoiceDate'].dt.year
    df['month'] = df['InvoiceDate'].dt.month

    # 7. Rename cột (chuẩn snake_case)
    df = df.rename(columns={
        'InvoiceNo': 'invoice_no',
        'StockCode': 'stock_code',
        'Description': 'description',
        'Quantity': 'quantity',
        'UnitPrice': 'unit_price',
        'CustomerID': 'customer_id',
        'Country': 'country',
        'InvoiceDate': 'invoice_date',
        'TotalAmount': 'total_amount'
    })

    print(f"   ✅ Transform hoàn tất! Còn lại {len(df):,} records")
    print(f"   Tổng doanh thu: ${df['total_amount'].sum():,.2f}")

    return df


if __name__ == "__main__":
    df = extract_and_transform()
    print("\n🎉 Extract & Transform HOÀN TẤT!")
    print(df.head())