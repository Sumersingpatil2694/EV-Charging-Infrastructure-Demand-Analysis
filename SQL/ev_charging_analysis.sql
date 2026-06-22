-- ============================================================
-- EV Charging Station Demand Analysis — SQL Analytics
-- Project  : Europe EV Charging Infrastructure Analysis
-- Database : ev_charging_analysis
-- Author   : Sumersing Patil
-- ============================================================
-- CONTENTS:
--   0. Database & Table Setup
--   Q1. Top Priority Cities for Investment
--   Q2. Month-over-Month EV Growth by Country
--   Q3. Infrastructure Status Profile
--   Q4. Charging Desert Cities
--   Q5. Coverage Gap by City Tier
--   Q6. Year-over-Year EV Growth Trend
-- ============================================================


-- ============================================================
-- 0. DATABASE & TABLE SETUP
-- ============================================================

CREATE DATABASE IF NOT EXISTS ev_charging_analysis;
USE ev_charging_analysis;

CREATE TABLE IF NOT EXISTS ev_data (
    id                   INT AUTO_INCREMENT PRIMARY KEY,
    country              VARCHAR(200),
    state                VARCHAR(200),
    city                 VARCHAR(200),
    year                 INT,
    month                INT,
    population           FLOAT,
    population_density   FLOAT,
    ev_registrations     FLOAT,
    bev_registrations    FLOAT,
    phev_registrations   FLOAT,
    charging_stations    FLOAT,
    charging_points      FLOAT,
    latitude             FLOAT,
    longitude            FLOAT,
    ev_per_station       FLOAT,
    station_density      FLOAT,
    monthly_growth_pct   FLOAT,
    yoy_growth_pct       FLOAT,
    coverage_gap         FLOAT,
    demand_score         FLOAT,
    priority_score       FLOAT,
    infra_status         VARCHAR(100),
    city_tier            VARCHAR(100),
    ev_market_share_pct  FLOAT,
    bev_share_pct        FLOAT,
    ev_stock_city        FLOAT,
    adoption_stage       VARCHAR(100)
);


-- ============================================================
-- Q1. TOP PRIORITY CITIES FOR CHARGING INVESTMENT
-- ============================================================
-- Business Question:
--   Which cities need charging infrastructure the most?
-- Logic:
--   Rank cities by average priority_score (higher = more urgent).
--   Also show coverage_gap and EV registrations for context.
-- ============================================================

SELECT
    country,
    city,
    ROUND(AVG(priority_score),    2)  AS avg_priority_score,
    ROUND(AVG(coverage_gap),      2)  AS avg_coverage_gap,
    ROUND(AVG(ev_registrations),  1)  AS avg_ev_registrations,
    ROUND(AVG(charging_stations), 1)  AS avg_charging_stations,
    MAX(infra_status)                 AS latest_infra_status
FROM ev_data
GROUP BY country, city
ORDER BY avg_priority_score DESC
LIMIT 15;

-- Saved as view:
CREATE OR REPLACE VIEW v_top_priority_cities AS
SELECT
    country,
    city,
    ROUND(AVG(priority_score),    2)  AS avg_priority_score,
    ROUND(AVG(coverage_gap),      2)  AS avg_coverage_gap,
    ROUND(AVG(ev_registrations),  1)  AS avg_ev_registrations,
    ROUND(AVG(charging_stations), 1)  AS avg_charging_stations,
    MAX(infra_status)                 AS latest_infra_status
FROM ev_data
GROUP BY country, city
ORDER BY avg_priority_score DESC
LIMIT 20;


-- ============================================================
-- Q2. MONTH-OVER-MONTH EV GROWTH BY COUNTRY
-- ============================================================
-- Business Question:
--   Which countries are seeing the fastest EV adoption growth?
-- Logic:
--   Use a CTE to aggregate monthly totals per country,
--   then apply LAG() window function to compute MoM growth %.
-- ============================================================

WITH monthly AS (
    SELECT
        country,
        year,
        month,
        CONCAT(year, '-', LPAD(month, 2, '0')) AS month_str,
        SUM(ev_registrations)        AS total_ev,
        SUM(charging_stations)       AS total_stations
    FROM ev_data
    GROUP BY country, year, month
)
SELECT
    country,
    month_str,
    total_ev,
    total_stations,
    LAG(total_ev) OVER (
        PARTITION BY country ORDER BY year, month
    )                                AS prev_month_ev,
    ROUND(
        100.0 * (
            total_ev
            - LAG(total_ev) OVER (PARTITION BY country ORDER BY year, month)
        )
        / NULLIF(
            LAG(total_ev) OVER (PARTITION BY country ORDER BY year, month),
            0
        ),
    2)                               AS mom_ev_growth_pct
FROM monthly
ORDER BY country, year, month;

-- Saved as view:
CREATE OR REPLACE VIEW v_monthly_mom_growth AS
WITH monthly AS (
    SELECT
        country,
        year,
        month,
        CONCAT(year, '-', LPAD(month, 2, '0')) AS month_str,
        SUM(ev_registrations)  AS total_ev,
        SUM(charging_stations) AS total_stations
    FROM ev_data
    GROUP BY country, year, month
)
SELECT
    country,
    month_str,
    total_ev,
    total_stations,
    LAG(total_ev) OVER (PARTITION BY country ORDER BY year, month) AS prev_month_ev,
    ROUND(
        100.0 * (total_ev - LAG(total_ev) OVER (PARTITION BY country ORDER BY year, month))
        / NULLIF(LAG(total_ev) OVER (PARTITION BY country ORDER BY year, month), 0),
    2) AS mom_ev_growth_pct
FROM monthly
ORDER BY country, year, month;


-- ============================================================
-- Q3. INFRASTRUCTURE STATUS PROFILE
-- ============================================================
-- Business Question:
--   How is charging infrastructure health distributed
--   across the dataset, and which status has the highest gap?
-- Logic:
--   Group by infra_status, aggregate key metrics.
--   Higher avg_ev_per_station = more EVs sharing fewer chargers.
-- ============================================================

SELECT
    infra_status,
    COUNT(*)                          AS total_records,
    COUNT(DISTINCT city)              AS city_count,
    ROUND(AVG(priority_score),  2)   AS avg_priority_score,
    ROUND(AVG(coverage_gap),    2)   AS avg_coverage_gap,
    ROUND(AVG(ev_per_station),  2)   AS avg_ev_per_station,
    ROUND(AVG(ev_registrations), 1)  AS avg_ev_registrations
FROM ev_data
GROUP BY infra_status
ORDER BY avg_priority_score DESC;

-- Saved as view:
CREATE OR REPLACE VIEW v_infra_status_profile AS
SELECT
    infra_status,
    COUNT(*)                          AS total_records,
    COUNT(DISTINCT city)              AS city_count,
    ROUND(AVG(priority_score),  2)   AS avg_priority_score,
    ROUND(AVG(coverage_gap),    2)   AS avg_coverage_gap,
    ROUND(AVG(ev_per_station),  2)   AS avg_ev_per_station,
    ROUND(AVG(ev_registrations), 1)  AS avg_ev_registrations
FROM ev_data
GROUP BY infra_status
ORDER BY avg_priority_score DESC;


-- ============================================================
-- Q4. CHARGING DESERT CITIES
-- ============================================================
-- Business Question:
--   Which cities have the most critical charging shortage —
--   high EVs on road, almost no charging stations?
-- Logic:
--   Filter only Critical Gap / Needs Attention cities.
--   Order by coverage_gap descending = worst-served first.
-- ============================================================

SELECT
    country,
    city,
    ROUND(AVG(ev_registrations),  1)  AS avg_ev_registrations,
    ROUND(AVG(charging_stations), 1)  AS avg_charging_stations,
    ROUND(AVG(coverage_gap),      2)  AS avg_coverage_gap,
    ROUND(AVG(ev_per_station),    2)  AS avg_ev_per_station,
    MAX(infra_status)                 AS infra_status
FROM ev_data
WHERE infra_status IN ('Critical Gap', 'Needs Attention')
GROUP BY country, city
ORDER BY avg_coverage_gap DESC
LIMIT 20;

-- Saved as view:
CREATE OR REPLACE VIEW v_charging_deserts AS
SELECT
    country,
    city,
    ROUND(AVG(ev_registrations),  1)  AS avg_ev_registrations,
    ROUND(AVG(charging_stations), 1)  AS avg_charging_stations,
    ROUND(AVG(coverage_gap),      2)  AS avg_coverage_gap,
    ROUND(AVG(ev_per_station),    2)  AS avg_ev_per_station,
    MAX(infra_status)                 AS infra_status
FROM ev_data
WHERE infra_status IN ('Critical Gap', 'Needs Attention')
GROUP BY country, city
ORDER BY avg_coverage_gap DESC
LIMIT 20;


-- ============================================================
-- Q5. COVERAGE GAP ANALYSIS BY CITY TIER
-- ============================================================
-- Business Question:
--   Are smaller cities more underserved than metro cities?
--   Where is the investment gap the largest by city size?
-- Logic:
--   Group by city_tier (Tier 1 Metro → Tier 4 Small).
--   Compare avg coverage_gap and avg priority_score per tier.
-- ============================================================

SELECT
    city_tier,
    COUNT(DISTINCT city)              AS city_count,
    ROUND(AVG(ev_registrations),  1)  AS avg_ev_registrations,
    ROUND(AVG(charging_stations), 1)  AS avg_charging_stations,
    ROUND(AVG(coverage_gap),      2)  AS avg_coverage_gap,
    ROUND(AVG(ev_per_station),    2)  AS avg_ev_per_station,
    ROUND(AVG(priority_score),    2)  AS avg_priority_score
FROM ev_data
GROUP BY city_tier
ORDER BY avg_priority_score DESC;

-- Saved as view:
CREATE OR REPLACE VIEW v_city_tier_gap AS
SELECT
    city_tier,
    COUNT(DISTINCT city)              AS city_count,
    ROUND(AVG(ev_registrations),  1)  AS avg_ev_registrations,
    ROUND(AVG(charging_stations), 1)  AS avg_charging_stations,
    ROUND(AVG(coverage_gap),      2)  AS avg_coverage_gap,
    ROUND(AVG(ev_per_station),    2)  AS avg_ev_per_station,
    ROUND(AVG(priority_score),    2)  AS avg_priority_score
FROM ev_data
GROUP BY city_tier
ORDER BY avg_priority_score DESC;


-- ============================================================
-- Q6. YEAR-OVER-YEAR EV GROWTH TREND
-- ============================================================
-- Business Question:
--   How has EV adoption grown annually per country?
--   Are charging stations keeping pace with EV growth?
-- Logic:
--   CTE aggregates yearly totals per country.
--   LAG() computes YoY growth % for both EV reg and stations.
--   Useful for identifying countries that need proactive planning.
-- ============================================================

WITH yearly AS (
    SELECT
        country,
        year,
        SUM(ev_registrations)   AS total_ev,
        SUM(charging_stations)  AS total_stations
    FROM ev_data
    GROUP BY country, year
)
SELECT
    country,
    year,
    total_ev,
    total_stations,
    LAG(total_ev) OVER (
        PARTITION BY country ORDER BY year
    )                            AS prev_year_ev,
    ROUND(
        100.0 * (
            total_ev
            - LAG(total_ev) OVER (PARTITION BY country ORDER BY year)
        )
        / NULLIF(
            LAG(total_ev) OVER (PARTITION BY country ORDER BY year),
            0
        ),
    2)                           AS yoy_ev_growth_pct,
    LAG(total_stations) OVER (
        PARTITION BY country ORDER BY year
    )                            AS prev_year_stations,
    ROUND(
        100.0 * (
            total_stations
            - LAG(total_stations) OVER (PARTITION BY country ORDER BY year)
        )
        / NULLIF(
            LAG(total_stations) OVER (PARTITION BY country ORDER BY year),
            0
        ),
    2)                           AS yoy_station_growth_pct
FROM yearly
ORDER BY country, year;

-- Saved as view:
CREATE OR REPLACE VIEW v_yoy_ev_growth AS
WITH yearly AS (
    SELECT
        country, year,
        SUM(ev_registrations)  AS total_ev,
        SUM(charging_stations) AS total_stations
    FROM ev_data
    GROUP BY country, year
)
SELECT
    country, year, total_ev, total_stations,
    LAG(total_ev)       OVER (PARTITION BY country ORDER BY year) AS prev_year_ev,
    ROUND(100.0 * (total_ev - LAG(total_ev) OVER (PARTITION BY country ORDER BY year))
          / NULLIF(LAG(total_ev) OVER (PARTITION BY country ORDER BY year), 0), 2) AS yoy_ev_growth_pct,
    LAG(total_stations) OVER (PARTITION BY country ORDER BY year) AS prev_year_stations,
    ROUND(100.0 * (total_stations - LAG(total_stations) OVER (PARTITION BY country ORDER BY year))
          / NULLIF(LAG(total_stations) OVER (PARTITION BY country ORDER BY year), 0), 2) AS yoy_station_growth_pct
FROM yearly
ORDER BY country, year;


-- ============================================================
-- QUICK REFERENCE — All 6 Views
-- ============================================================
-- SELECT * FROM v_top_priority_cities;
-- SELECT * FROM v_monthly_mom_growth;
-- SELECT * FROM v_infra_status_profile;
-- SELECT * FROM v_charging_deserts;
-- SELECT * FROM v_city_tier_gap;
-- SELECT * FROM v_yoy_ev_growth;
-- ============================================================
