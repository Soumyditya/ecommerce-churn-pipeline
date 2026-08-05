import pandas as pd
import os

def clean_data():
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    
    # Load data
    print("Loading raw data...")
    customers = pd.read_csv(os.path.join(raw_dir, 'customers.csv'))
    orders = pd.read_csv(os.path.join(raw_dir, 'orders.csv'))
    products = pd.read_csv(os.path.join(raw_dir, 'products.csv'))
    
    # Cleaning Customers
    customers.drop_duplicates(inplace=True)
    
    # Cleaning Orders
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    
    # Create RFM Features (Recency, Frequency, Monetary)
    print("Calculating RFM metrics for customers...")
    
    # Assume analysis date is the day after the last order
    analysis_date = orders['order_date'].max() + pd.Timedelta(days=1)
    
    rfm = orders.groupby('customer_id').agg({
        'order_date': lambda x: (analysis_date - x.max()).days, # Recency
        'order_id': 'count', # Frequency
        'total_amount': 'sum' # Monetary
    }).rename(columns={
        'order_date': 'recency',
        'order_id': 'frequency',
        'total_amount': 'monetary'
    }).reset_index()
    
    # Merge RFM back to customers
    customers_processed = pd.merge(customers, rfm, on='customer_id', how='left')
    
    # Fill NaN for customers with no orders (if any)
    customers_processed['recency'] = customers_processed['recency'].fillna(999)
    customers_processed['frequency'] = customers_processed['frequency'].fillna(0)
    customers_processed['monetary'] = customers_processed['monetary'].fillna(0)
    
    # Save processed data
    customers_processed.to_csv(os.path.join(processed_dir, 'customers_processed.csv'), index=False)
    orders.to_csv(os.path.join(processed_dir, 'orders_cleaned.csv'), index=False)
    products.to_csv(os.path.join(processed_dir, 'products_cleaned.csv'), index=False)
    
    print("Data cleaning and feature engineering complete. Files saved to data/processed/")

if __name__ == "__main__":
    clean_data()
