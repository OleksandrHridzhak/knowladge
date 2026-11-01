-- Q5: PIVOT — Квартальна матриця переданої електроенергії (МВт*год) за енергетичними районами
SELECT
    region_cluster,
    ROUND(COALESCE(Q1, 0.0), 2) AS Q1_mwh,
    ROUND(COALESCE(Q2, 0.0), 2) AS Q2_mwh,
    ROUND(COALESCE(Q3, 0.0), 2) AS Q3_mwh,
    ROUND(COALESCE(Q4, 0.0), 2) AS Q4_mwh,
    ROUND(COALESCE(Q1, 0.0) + COALESCE(Q2, 0.0) + COALESCE(Q3, 0.0) + COALESCE(Q4, 0.0), 2) AS annual_total_mwh
FROM (
    SELECT
        s.region_cluster,
        d.quarter,
        f.energy_transmitted_mwh
    FROM fact_grid_telemetry f
    JOIN dim_substation s ON f.substation_key = s.substation_key
    JOIN dim_date d ON f.date_key = d.date_key
)
PIVOT (
    SUM(energy_transmitted_mwh)
    FOR quarter IN ('Q1' AS Q1, 'Q2' AS Q2, 'Q3' AS Q3, 'Q4' AS Q4)
)
ORDER BY annual_total_mwh DESC;
