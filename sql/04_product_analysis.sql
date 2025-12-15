-- 04_product_analysis.sql
-- Understand which categories, sub-categories and products drive sales and profit.

-- Category level
SELECT category,
       SUM(sales) AS sales,
       SUM(profit) AS profit,
       ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales),0), 2) AS profit_margin_pct
FROM superstore
GROUP BY category
ORDER BY profit DESC;

-- Top products by profit
SELECT product_name, category, sub_category, SUM(sales) AS sales, SUM(profit) AS profit
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY profit DESC
LIMIT 20;
