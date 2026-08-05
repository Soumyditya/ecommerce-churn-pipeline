-- 1. Monthly Revenue Trend
SELECT 
    strftime('%Y-%m', order_date) AS order_month,
    SUM(total_amount) AS monthly_revenue,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM orders
GROUP BY order_month
ORDER BY order_month;

-- 2. Top 5 Products by Revenue
SELECT 
    p.category,
    p.product_id,
    SUM(o.total_amount) as total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category, p.product_id
ORDER BY total_revenue DESC
LIMIT 5;

-- 3. Customer Churn Risk by Country
SELECT 
    country,
    COUNT(customer_id) as total_customers,
    SUM(is_churn) as churned_customers,
    CAST(SUM(is_churn) AS FLOAT) / COUNT(customer_id) * 100 as churn_rate_percentage
FROM customers
GROUP BY country
ORDER BY churn_rate_percentage DESC;

-- 4. High Value Customers at Risk of Churn
-- CTE to find customers in top 20% of monetary value
WITH RankedCustomers AS (
    SELECT 
        customer_id,
        monetary,
        churn_probability,
        NTILE(5) OVER(ORDER BY monetary DESC) as value_quintile
    FROM customers
)
SELECT 
    customer_id,
    monetary,
    churn_probability
FROM RankedCustomers
WHERE value_quintile = 1 AND churn_probability > 0.6
ORDER BY churn_probability DESC;
