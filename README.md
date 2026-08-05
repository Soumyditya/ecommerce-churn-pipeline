# E-Commerce Customer Insights & Churn Prediction Pipeline

## Overview
This project is an end-to-end Data Analytics and Data Science pipeline simulating a real-world E-Commerce environment. The goal of this project is to process raw transactional data, engineer business-critical features (like RFM metrics), predict customer churn using Machine Learning, and store the results in a relational database for Business Intelligence reporting.

## Tech Stack
- **Python**: Data generation, Pandas (Data Cleaning & Feature Engineering), Scikit-Learn (Machine Learning)
- **SQL**: SQLite for relational database management, Views, Window Functions, CTEs
- **BI Tools**: Ready for integration with Power BI or Tableau

## Project Architecture
1. **Data Generation (`00_generate_data.py`)**: Generates a synthetic dataset of 1,000 customers, 50 products, and 5,000 orders.
2. **Data Cleaning & EDA (`01_data_cleaning.py`)**: Cleans the raw CSV files and engineers RFM (Recency, Frequency, Monetary) metrics to segment customers based on their buying behavior.
3. **Predictive Modeling (`02_eda_and_modeling.py`)**: Trains a Random Forest Classifier to predict the probability of a customer churning (defined as no purchases in the last 180 days).
4. **Database Integration (`03_load_to_sql.py`)**: Loads all processed data into a local SQLite database (`ecommerce_data.db`) and creates a comprehensive `dashboard_view` for BI tools.
5. **SQL Analytics (`sql/queries.sql`)**: Contains complex SQL queries demonstrating data aggregation, revenue trends, and high-value customer identification.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
