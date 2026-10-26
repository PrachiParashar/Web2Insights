
from extractor import extract_stock_data

if __name__ == "__main__":
    print("Starting scheduled stock-data extraction...")
    extract_stock_data("AAPL")
    print("Stock-data extraction completed successfully!")
