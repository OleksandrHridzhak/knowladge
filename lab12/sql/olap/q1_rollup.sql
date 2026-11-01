-- Q1: ROLLUP — Ієрархічна агрегація переданої енергії та втрат за енергорайонами і класами напруги
SELECT
    COALESCE(s.region_cluster, 'УСІ ЕНЕРГОРАЙОНИ (РАЗОМ)') AS region_cluster,
    COALESCE(CAST(s.voltage_class_kv AS VARCHAR), 'Усі класи напруги') AS voltage_class,
    COUNT(*) AS observations_cnt,
    ROUND(SUM(f.energy_transmitted_mwh), 2) AS total_energy_mwh,
    ROUND(SUM(f.tech_losses_mwh), 2) AS total_losses_mwh,
    ROUND(SUM(f.tech_losses_mwh) * 100.0 / NULLIF(SUM(f.energy_transmitted_mwh), 0), 3) AS loss_rate_pct
FROM fact_grid_telemetry f
JOIN dim_substation s ON f.substation_key = s.substation_key
GROUP BY ROLLUP (s.region_cluster, s.voltage_class_kv)
ORDER BY GROUPING(s.region_cluster), s.region_cluster, GROUPING(s.voltage_class_kv), s.voltage_class_kv DESC;
