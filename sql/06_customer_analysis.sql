-- 06_customer_analysis.sql
-- Identify high value customers and churn risk signals.

-- Top customers by profit
SELECT customer_id, customer_name, SUM(sales) AS sales, SUM(profit) AS profit
FROM superstore
GROUP BY customer_id, customer_name
ORDER BY profit DESC
LIMIT 25;

-- Customers with lots of orders but low profit
SELECT customer_id, customer_name, COUNT(order_id) AS orders, SUM(sales) AS sales, SUM(profit) AS profit
FROM superstore
GROUP BY customer_id, customer_name
HAVING COUNT(order_id) > 10
ORDER BY profit ASC
LIMIT 25;
