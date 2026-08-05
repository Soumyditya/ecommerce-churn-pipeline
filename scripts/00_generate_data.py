import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_customers=1000, num_orders=5000):
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # 1. Customers
    customer_ids = [f'CUST_{i:04d}' for i in range(1, num_customers + 1)]
    join_dates = [datetime(2022, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(num_customers)]
    countries = np.random.choice(['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia'], num_customers, p=[0.4, 0.2, 0.1, 0.1, 0.1, 0.1])
    
    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'join_date': join_dates,
        'country': countries,
        'age': np.random.randint(18, 70, num_customers)
    })

    # 2. Products
    product_categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Toys']
    product_ids = [f'PROD_{i:03d}' for i in range(1, 51)]
    products_df = pd.DataFrame({
        'product_id': product_ids,
        'category': np.random.choice(product_categories, 50),
        'price': np.round(np.random.uniform(10.0, 500.0, 50), 2)
    })

    # 3. Orders
    order_ids = [f'ORD_{i:05d}' for i in range(1, num_orders + 1)]
    
    # Introduce some seasonality/trend in order dates
    order_dates = []
    for _ in range(num_orders):
        # More orders towards end of year (Q4)
        if random.random() < 0.4:
            month = random.randint(10, 12)
        else:
            month = random.randint(1, 9)
        day = random.randint(1, 28)
        order_dates.append(datetime(2023, month, day))
        
    # Simulate some customers buying more frequently (Pareto principle)
    weights = np.random.dirichlet(np.ones(num_customers), size=1)[0]
    order_customers = np.random.choice(customer_ids, num_orders, p=weights)
    
    order_products = np.random.choice(product_ids, num_orders)
    quantities = np.random.randint(1, 6, num_orders)
    
    orders_df = pd.DataFrame({
        'order_id': order_ids,
        'customer_id': order_customers,
        'product_id': order_products,
        'order_date': order_dates,
        'quantity': quantities
    })
    
    # Calculate total amount
    orders_df = orders_df.merge(products_df[['product_id', 'price']], on='product_id', how='left')
    orders_df['total_amount'] = orders_df['quantity'] * orders_df['price']
    
    # Sort orders by date
    orders_df = orders_df.sort_values('order_date').reset_index(drop=True)
    
    # Save to CSV
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw'), exist_ok=True)
    
    customers_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'customers.csv')
    products_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'products.csv')
    orders_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'orders.csv')
    
    customers_df.to_csv(customers_path, index=False)
    products_df.to_csv(products_path, index=False)
    orders_df.to_csv(orders_path, index=False)
    
    print(f"Synthetic data generated successfully:")
    print(f" - {len(customers_df)} customers")
    print(f" - {len(products_df)} products")
    print(f" - {len(orders_df)} orders")
    print(f"Saved to data/raw/")

if __name__ == "__main__":
    generate_synthetic_data()
