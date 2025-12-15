-- 03_region_analysis.sql
-- Region and state level analysis to identify where profit is coming from.

SELECT
    region,
    state,
    SUM(sales) AS sales,
    SUM(profit) AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales),0), 2) AS profit_margin_pct
FROM superstore
GROUP BY region, state
ORDER BY profit DESC
LIMIT 50;

-- Top losing states (most negative profit)
SELECT state, SUM(sales) AS sales, SUM(profit) AS profit
FROM superstore
GROUP BY state
ORDER BY profit ASC
LIMIT 10;
