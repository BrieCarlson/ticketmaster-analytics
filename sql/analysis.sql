-- ============================================
-- Ticketmaster Analytics
-- SQL Analysis
-- ============================================


-- 1. Total number of events
SELECT COUNT(*) AS total_events
FROM events;


-- 2. Events by state
SELECT
    v.state,
    COUNT(*) AS event_count
FROM events e
JOIN venues v
    ON e.venue_id = v.venue_id
GROUP BY v.state
ORDER BY event_count DESC;


-- 3. Events by city
SELECT
    v.city,
    v.state,
    COUNT(*) AS event_count
FROM events e
JOIN venues v
    ON e.venue_id = v.venue_id
GROUP BY v.city, v.state
ORDER BY event_count DESC;


-- 4. Events by segment
SELECT
    segment,
    COUNT(*) AS event_count
FROM events
GROUP BY segment
ORDER BY event_count DESC;


-- 5. Top genres
SELECT
    genre,
    COUNT(*) AS event_count
FROM events
WHERE genre IS NOT NULL
GROUP BY genre
ORDER BY event_count DESC
LIMIT 15;


-- 6. Top venues
SELECT
    v.venue_name,
    v.city,
    v.state,
    COUNT(*) AS event_count
FROM events e
JOIN venues v
    ON e.venue_id = v.venue_id
GROUP BY v.venue_id, v.venue_name, v.city, v.state
ORDER BY event_count DESC
LIMIT 15;


-- 7. Events by month
SELECT
    DATE_TRUNC('month', event_date)::date AS month,
    COUNT(*) AS event_count
FROM events
GROUP BY month
ORDER BY month;


-- 8. Events by event status
SELECT
    event_status,
    COUNT(*) AS event_count
FROM events
GROUP BY event_status
ORDER BY event_count DESC;


-- 9. Genre distribution by state
SELECT
    v.state,
    e.genre,
    COUNT(*) AS event_count
FROM events e
JOIN venues v
    ON e.venue_id = v.venue_id
WHERE e.genre IS NOT NULL
GROUP BY v.state, e.genre
ORDER BY v.state, event_count DESC;


-- 10. Cities with the greatest variety of genres
SELECT
    v.city,
    v.state,
    COUNT(DISTINCT e.genre) AS unique_genres,
    COUNT(*) AS event_count
FROM events e
JOIN venues v
    ON e.venue_id = v.venue_id
WHERE e.genre IS NOT NULL
GROUP BY v.city, v.state
ORDER BY unique_genres DESC, event_count DESC;


-- 11. Events by year and month
SELECT
    EXTRACT(YEAR FROM event_date) AS year,
    EXTRACT(MONTH FROM event_date) AS month,
    COUNT(*) AS event_count
FROM events
GROUP BY year, month
ORDER BY year, month;


-- 12. Data completeness
SELECT
    COUNT(*) AS total_events,
    COUNT(event_time) AS events_with_time,
    COUNT(timezone) AS events_with_timezone,
    COUNT(promoter) AS events_with_promoter,
    COUNT(price_min) AS events_with_price,
    COUNT(attraction_id) AS events_with_attraction
FROM events;