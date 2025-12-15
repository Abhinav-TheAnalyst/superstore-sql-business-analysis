-- 07_final_insights.sql
-- Final set of queries to produce recruiter-friendly charts and tables.

-- Combine product and region signals: profitable product categories by region
SELECT region, category, SUM(sales) AS sales, SUM(profit) AS profit
FROM superstore
GROUP BY region, category
ORDER BY region, profit DESC;

-- Quick summary table for dashboards
SELECT
    region,
    SUM(sales) AS sales,
    SUM(profit) AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales),0), 2) AS margin_pct,
    COUNT(DISTINCT customer_id) AS customers
FROM superstore
GROUP BY region
ORDER BY sales DESC;
