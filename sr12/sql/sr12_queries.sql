-- ============================================================================
-- Самостійна робота №12: 5 SQL-запитів для перевірки зіркової схеми (Крок 4)
-- ============================================================================

-- Запит Q1 (Бізнес-питання 1): Який сумарний обсяг недовідпущеної електроенергії (ENS, МВт*год)
-- та штрафних компенсацій у розрізі енергетичних районів і класів напруги (ROLLUP)?
SELECT
    COALESCE(n.region_cluster, 'УСЯ ОЕС УКРАЇНИ') AS region_cluster,
    COALESCE(CAST(n.voltage_kv AS VARCHAR), 'Усі напруги') AS voltage_class,
    COUNT(*) AS incidents_cnt,
    ROUND(SUM(f.ens_unsupplied_mwh), 2) AS total_ens_mwh,
    ROUND(SUM(f.compensation_cost_uah) / 1000.0, 2) AS total_compensation_k_uah
FROM fact_outage_balance f
JOIN dim_grid_node n ON f.node_key = n.node_key
GROUP BY ROLLUP (n.region_cluster, n.voltage_kv)
ORDER BY GROUPING(n.region_cluster), n.region_cluster, GROUPING(n.voltage_kv), n.voltage_kv DESC;

-- Запит Q2 (Бізнес-питання 2): Як розподіляється сумарна тривалість відновлення живлення
-- та кількість знеструмлених точок обліку за класами таксономії обладнання і групами причин?
SELECT
    e.class_l1,
    e.subclass_l2,
    c.cause_group,
    COUNT(*) AS incidents_cnt,
    SUM(f.affected_consumers_cnt) AS total_consumers_affected,
    ROUND(SUM(f.restoration_duration_min), 1) AS total_restoration_min,
    ROUND(AVG(f.restoration_duration_min), 2) AS avg_restoration_min
FROM fact_outage_balance f
JOIN dim_equipment_taxonomy e ON f.equipment_key = e.equipment_key
JOIN dim_outage_cause c ON f.cause_key = c.cause_key
WHERE e.is_current = TRUE
GROUP BY e.class_l1, e.subclass_l2, c.cause_group
ORDER BY total_restoration_min DESC;

-- Запит Q3 (Бізнес-питання 3): Яке середнє вимкнене навантаження, обертовий резерв та відхилення
-- напруги спостерігаються для споживачів за категоріями надійності під час вечірнього максимуму взимку?
SELECT
    cc.reliability_tier,
    cc.sector_name,
    COUNT(*) AS winter_peak_incidents,
    ROUND(AVG(f.disconnected_load_mw), 2) AS avg_disconnected_mw,
    ROUND(AVG(f.spinning_reserve_mw), 2) AS avg_reserve_mw,
    ROUND(AVG(ABS(f.voltage_deviation_pct)), 2) AS avg_abs_voltage_dev_pct,
    ROUND(MIN(f.frequency_nadir_hz), 3) AS min_frequency_hz
FROM fact_outage_balance f
JOIN dim_time t ON f.time_key = t.time_key
JOIN dim_consumer_category cc ON f.consumer_key = cc.consumer_key
WHERE t.season = 'Зима'
  AND t.peak_period = 'Вечірній максимум'
GROUP BY cc.reliability_tier, cc.sector_name
ORDER BY avg_disconnected_mw DESC;

-- Запит Q4 (Бізнес-питання 4): Які топ-5 вузлових підстанцій мають найбільший недовідпуск електроенергії
-- та який їхній питомий індекс SAIDI (хв/споживача) з віконним ранжуванням DENSE_RANK?
WITH node_totals AS (
    SELECT
        n.region_cluster,
        n.substation_name,
        COUNT(*) AS incidents_cnt,
        ROUND(SUM(f.ens_unsupplied_mwh), 2) AS ens_mwh,
        ROUND(SUM(f.restoration_duration_min) * 1.0 / NULLIF(COUNT(*), 0), 2) AS avg_outage_min
    FROM fact_outage_balance f
    JOIN dim_grid_node n ON f.node_key = n.node_key
    GROUP BY n.region_cluster, n.substation_name
)
SELECT
    DENSE_RANK() OVER (ORDER BY ens_mwh DESC) AS severity_rank,
    region_cluster,
    substation_name,
    incidents_cnt,
    ens_mwh,
    avg_outage_min
FROM node_totals
QUALIFY severity_rank <= 5
ORDER BY severity_rank;

-- Запит Q5 (Бізнес-питання 5): Як змінилася середня тривалість відновлення та питомий недовідпуск
-- на один інцидент після модернізації обладнання за версіями SCD Тип 2?
SELECT
    e.natural_code,
    e.apparatus_model,
    e.is_current,
    e.rated_power_mva,
    COUNT(*) AS incidents_cnt,
    ROUND(AVG(f.restoration_duration_min), 2) AS avg_restoration_min,
    ROUND(SUM(f.ens_unsupplied_mwh) / NULLIF(COUNT(*), 0), 2) AS ens_per_incident_mwh
FROM fact_outage_balance f
JOIN dim_equipment_taxonomy e ON f.equipment_key = e.equipment_key
WHERE e.natural_code IN ('EQ-AT1-ZAKH', 'EQ-SEL421')
GROUP BY e.natural_code, e.apparatus_model, e.is_current, e.rated_power_mva
ORDER BY e.natural_code, e.is_current;
