import pandas as pd
import sqlite3
import os

def load_to_sql():
    processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    db_path = os.path.join(os.path.dirname(__file__), '..', 'ecommerce_data.db')
    
    # Load processed data
    print("Loading processed data...")
    customers = pd.read_csv(os.path.join(processed_dir, 'customers_with_predictions.csv'))
    orders = pd.read_csv(os.path.join(processed_dir, 'orders_cleaned.csv'))
    products = pd.read_csv(os.path.join(processed_dir, 'products_cleaned.csv'))
    
    # Connect to SQLite
    print("Connecting to SQLite database...")
    conn = sqlite3.connect(db_path)
    
    # Write to SQLite
    print("Writing tables to database...")
    customers.to_sql('customers', conn, if_exists='replace', index=False)
    orders.to_sql('orders', conn, if_exists='replace', index=False)
    products.to_sql('products', conn, if_exists='replace', index=False)
    
    # Create a view for the dashboard (Customer Churn View)
    cursor = conn.cursor()
    cursor.execute('DROP VIEW IF EXISTS dashboard_view')
    cursor.execute('''
        CREATE VIEW dashboard_view AS
        SELECT 
            c.customer_id,
            c.country,
            c.age,
            c.recency,
            c.frequency,
            c.monetary,
            c.is_churn,
            c.churn_probability,
            COUNT(o.order_id) as total_orders
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY 
            c.customer_id, c.country, c.age, c.recency, 
            c.frequency, c.monetary, c.is_churn, c.churn_probability
    ''')
    
    conn.commit()
    conn.close()
    print(f"Data successfully loaded to {db_path}")

if __name__ == "__main__":
    load_to_sql()
