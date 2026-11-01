-- Q3: SLICE — Зріз куба для зимових пікових годин за підстанціями
SELECT
    s.substation_name,
    s.region_cluster,
    s.voltage_class_kv,
    COUNT(*) AS peak_hours_observed,
    ROUND(AVG(f.active_load_mw), 2) AS avg_active_load_mw,
    ROUND(AVG(f.available_reserve_mw), 2) AS avg_reserve_mw,
    ROUND(MAX(f.load_factor_pct), 2) AS max_load_factor_pct
FROM fact_grid_telemetry f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_substation s ON f.substation_key = s.substation_key
WHERE d.season = 'Зима'
  AND d.is_peak_hour = TRUE
GROUP BY s.substation_name, s.region_cluster, s.voltage_class_kv
ORDER BY avg_active_load_mw DESC;
