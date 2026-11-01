-- Q2: CUBE — Перехресний аналіз простоїв та спрацювань РЗА за класами таксономії та категоріями подій
SELECT
    COALESCE(t.class_level1_name, 'УСІ КЛАСИ ОБЛАДНАННЯ') AS equipment_class,
    COALESCE(e.event_category, 'УСІ КАТЕГОРІЇ ПОДІЙ') AS event_category,
    COUNT(*) AS events_cnt,
    SUM(f.protection_trips_count) AS total_trips,
    ROUND(SUM(f.outage_duration_min), 2) AS total_outage_min,
    ROUND(AVG(f.risk_score), 3) AS avg_risk_score
FROM fact_grid_telemetry f
JOIN dim_taxonomy_equipment t ON f.taxonomy_key = t.taxonomy_key
JOIN dim_event_type e ON f.event_type_key = e.event_type_key
WHERE t.is_current = TRUE
GROUP BY CUBE (t.class_level1_name, e.event_category)
ORDER BY GROUPING(t.class_level1_name), t.class_level1_name, GROUPING(e.event_category), e.event_category;
