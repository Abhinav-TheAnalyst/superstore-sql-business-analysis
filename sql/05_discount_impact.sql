-- 05_discount_impact.sql
-- Explore how discounting relates to profit and sales.

-- Group by rounded discount levels (useful when discounts are floats)
SELECT
    ROUND(discount::numeric, 2) AS discount_val,
    COUNT(*) AS order_count,
    SUM(sales) AS sales,
    SUM(profit) AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales),0), 2) AS profit_margin_pct
FROM superstore
GROUP BY discount_val
ORDER BY discount_val;

-- Compare average profit margin for orders with high discount vs low discount
SELECT
    CASE WHEN discount >= 0.2 THEN 'high_discount' ELSE 'low_discount' END AS bucket,
    AVG(profit) AS avg_profit,
    AVG(sales) AS avg_sales
FROM superstore
GROUP BY bucket;
