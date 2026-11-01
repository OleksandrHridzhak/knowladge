-- Q7: WINDOW (Ранжування DENSE_RANK) — Топ-3 найбільш навантажених одиниць обладнання у кожному класі таксономії
WITH equipment_stats AS (
    SELECT
        t.class_level1_name,
        t.subclass_level2_name,
        t.equipment_name,
        ROUND(AVG(f.load_factor_pct), 2) AS avg_load_pct,
        ROUND(MAX(f.load_factor_pct), 2) AS peak_load_pct,
        SUM(f.protection_trips_count) AS total_trips
    FROM fact_grid_telemetry f
    JOIN dim_taxonomy_equipment t ON f.taxonomy_key = t.taxonomy_key
    WHERE t.is_current = TRUE
    GROUP BY t.class_level1_name, t.subclass_level2_name, t.equipment_name
),
ranked AS (
    SELECT
        *,
        DENSE_RANK() OVER (
            PARTITION BY class_level1_name
            ORDER BY avg_load_pct DESC, total_trips DESC
        ) AS rank_in_class
    FROM equipment_stats
)
SELECT
    class_level1_name,
    rank_in_class,
    subclass_level2_name,
    equipment_name,
    avg_load_pct,
    peak_load_pct,
    total_trips
FROM ranked
WHERE rank_in_class <= 3
ORDER BY class_level1_name, rank_in_class;
