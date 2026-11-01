-- Q4: DICE — Вибірка підкуба для магістралей 750/330 кВ Західного і Центрального регіонів при аваріях та ожеледі
SELECT
    s.region_cluster,
    t.subclass_level2_name,
    e.event_subclass,
    w.icing_risk_level,
    COUNT(*) AS incident_count,
    ROUND(SUM(f.tech_losses_mwh), 2) AS losses_mwh,
    ROUND(SUM(f.outage_duration_min), 2) AS outage_min,
    ROUND(AVG(f.risk_score), 3) AS avg_risk
FROM fact_grid_telemetry f
JOIN dim_substation s ON f.substation_key = s.substation_key
JOIN dim_taxonomy_equipment t ON f.taxonomy_key = t.taxonomy_key
JOIN dim_event_type e ON f.event_type_key = e.event_type_key
JOIN dim_weather w ON f.weather_key = w.weather_key
WHERE s.region_cluster IN ('Західний', 'Центральний')
  AND s.voltage_class_kv IN (750, 330)
  AND e.event_category = 'Аварійний режим'
  AND w.icing_risk_level IN ('Високий', 'Критичний')
GROUP BY s.region_cluster, t.subclass_level2_name, e.event_subclass, w.icing_risk_level
ORDER BY avg_risk DESC, losses_mwh DESC;
