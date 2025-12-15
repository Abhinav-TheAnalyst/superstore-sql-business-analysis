-- 02_sales_overview.sql
-- High-level KPIs and trend analysis.

-- Total sales and profit
SELECT
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales),0), 2) AS profit_margin_pct
FROM superstore;

-- Monthly trend (engine might use different date functions)
SELECT
    order_month,
    SUM(sales) AS monthly_sales,
    SUM(profit) AS monthly_profit
FROM superstore
GROUP BY order_month
ORDER BY order_month;
