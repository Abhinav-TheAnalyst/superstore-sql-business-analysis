-- 01_data_cleaning.sql
-- Quick checks and data validation queries to understand the cleaned dataset.

-- 1) Count rows and basic stats
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT order_month) AS months_present
FROM superstore;

-- 2) Missing values by column (engine-specific; example for Postgres)
-- SELECT column_name, COUNT(*) FILTER (WHERE column_name IS NULL) FROM superstore GROUP BY column_name;

-- 3) Basic sanity checks for numeric columns
SELECT
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    AVG(discount) AS avg_discount
FROM superstore;
