import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def extract_and_transform():
    """Extract từ Excel và Transform dữ liệu"""
    print("📥 Bắt đầu Extract dữ liệu từ Excel...")

    # Đường dẫn đến file Excel
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Online Retail.xlsx")
    
    # Extract
    df = pd.read_excel(data_path)
    print(f"   ✅ Đọc xong {len(df):,} records từ Excel")

    # Transform
    print("🔄 Đang Transform dữ liệu...")

    # 1. Xóa dòng thiếu CustomerID
    df = df.dropna(subset=['CustomerID'])

    # 2. Xóa duplicate
    df = df.drop_duplicates()

    # 3. Lọc Quantity & UnitPrice > 0
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

    # 4. Tính TotalAmount
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

    # 5. Chuyển InvoiceDate thành datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # 6. Thêm Year và Month
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month

    # 7. Đổi tên cột cho khớp với bảng fact_sales
    df = df.rename(columns={
        'InvoiceNo': 'invoice_no',
        'StockCode': 'stock_code',
        'Description': 'description',
        'Quantity': 'quantity',
        'UnitPrice': 'unit_price',
        'CustomerID': 'customer_id',
        'Country': 'country',
        'InvoiceDate': 'invoice_date',
        'TotalAmount': 'total_amount',   
        'Year': 'year',                 
        'Month': 'month'                 
    })

    print(f"   ✅ Transform xong! Còn lại {len(df):,} records sạch sẽ")
    
    return df

if __name__ == "__main__":
    df = extract_and_transform()
    print("\n✅ Extract & Transform HOÀN TẤT!")
    print(df.head())