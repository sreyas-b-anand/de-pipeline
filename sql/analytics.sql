-- 1. Which city has the most orders?
SELECT
    l.city,
    COUNT(*) AS order_count
FROM fact_orders f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.city
ORDER BY order_count DESC;


-- 2. Which restaurants have the most orders?
SELECT
    r.restaurant_name,
    COUNT(*) AS order_count
FROM fact_orders f
JOIN dim_restaurant r
    ON f.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name
ORDER BY order_count DESC;


-- 3. What is the average order value across all orders?
SELECT
    AVG(total) AS average_order_value
FROM fact_orders;


-- 4. What percentage of all orders were delivered?
SELECT
    COUNT(*) FILTER (WHERE is_delivered = TRUE) * 100.0
    / COUNT(*) AS delivered_percentage
FROM fact_orders;


-- 5. What is the average order value for each city?
SELECT
    l.city,
    AVG(f.total) AS average_order_value
FROM fact_orders f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.city
ORDER BY average_order_value DESC;


-- 6. Which restaurant has the highest average order value?
SELECT
    r.restaurant_name,
    AVG(f.total) AS average_order_value
FROM fact_orders f
JOIN dim_restaurant r
    ON f.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name
ORDER BY average_order_value DESC
LIMIT 1;


-- 7. What is the average delivery distance?
SELECT
    AVG(distance_km) AS average_delivery_distance
FROM fact_orders;


-- 8. Does delivery distance affect average order value?
SELECT
    CASE
        WHEN distance_km < 2 THEN '< 2 km'
        WHEN distance_km <= 5 THEN '2-5 km'
        WHEN distance_km <= 10 THEN '5-10 km'
        ELSE '> 10 km'
    END AS distance_range,
    AVG(total) AS average_order_value
FROM fact_orders
GROUP BY distance_range
ORDER BY average_order_value DESC;


-- 9. What is the average order value for delivered vs non-delivered orders?
SELECT
    is_delivered,
    AVG(total) AS average_order_value
FROM fact_orders
GROUP BY is_delivered;


-- 10. What are the top 10 restaurants based on total revenue?
SELECT
    r.restaurant_name,
    SUM(f.total) AS total_revenue
FROM fact_orders f
JOIN dim_restaurant r
    ON f.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name
ORDER BY total_revenue DESC
LIMIT 10;


-- 11. Which restaurants have an average order value higher than the overall average?
SELECT
    r.restaurant_name,
    AVG(f.total) AS average_order_value
FROM fact_orders f
JOIN dim_restaurant r
    ON f.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name
HAVING AVG(f.total) > (
    SELECT AVG(total)
    FROM fact_orders
)
ORDER BY average_order_value DESC;


-- 12. How many orders were placed each month?
SELECT
    d.year,
    d.month,
    COUNT(*) AS order_count
FROM fact_orders f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 13. What is the monthly revenue?
SELECT
    d.year,
    d.month,
    SUM(f.total) AS revenue
FROM fact_orders f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 14. Which city generates the most revenue?
SELECT
    l.city,
    SUM(f.total) AS total_revenue
FROM fact_orders f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.city
ORDER BY total_revenue DESC;


-- 15. Which restaurants have the highest delivery success rate?
SELECT
    r.restaurant_name,
    COUNT(*) FILTER (WHERE f.is_delivered = TRUE) * 100.0
    / COUNT(*) AS delivery_success_rate
FROM fact_orders f
JOIN dim_restaurant r
    ON f.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name
ORDER BY delivery_success_rate DESC;


-- 16. Which customers placed the most orders?
SELECT
    c.customer_id,
    COUNT(*) AS order_count
FROM fact_orders f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY order_count DESC
LIMIT 10;


-- 17. What is the average rating for each restaurant?
SELECT
    r.restaurant_name,
    AVG(f.rating) AS average_rating
FROM fact_orders f
JOIN dim_restaurant r
    ON f.restaurant_id = r.restaurant_id
WHERE f.rating IS NOT NULL
GROUP BY r.restaurant_name
ORDER BY average_rating DESC;


-- 18. What is the average rider wait time by city?
SELECT
    l.city,
    AVG(f.rider_wait_time) AS average_rider_wait_time
FROM fact_orders f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.city
ORDER BY average_rider_wait_time DESC;


-- 19. What is the average KPT duration by restaurant?
SELECT
    r.restaurant_name,
    AVG(f.kpt_duration) AS average_kpt_duration
FROM fact_orders f
JOIN dim_restaurant r
    ON f.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name
ORDER BY average_kpt_duration DESC;


-- 20. What percentage of orders were rejected, returned, or timed out?
SELECT
    order_status,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage
FROM fact_orders
GROUP BY order_status
ORDER BY percentage DESC;