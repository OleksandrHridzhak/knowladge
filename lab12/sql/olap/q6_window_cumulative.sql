-- Q6: WINDOW (Накопичення та ковзне середнє) — Помісячна кумулятивна передача енергії та 3-місячне ковзне середнє втрат
WITH monthly_stats AS (
    SELECT
        s.region_cluster,
        d.month,
        d.month_name,
        ROUND(SUM(f.energy_transmitted_mwh), 2) AS monthly_energy_mwh,
        ROUND(SUM(f.tech_losses_mwh), 2) AS monthly_losses_mwh
    FROM fact_grid_telemetry f
    JOIN dim_substation s ON f.substation_key = s.substation_key
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE s.region_cluster = 'Західний'
    GROUP BY s.region_cluster, d.month, d.month_name
)
SELECT
    region_cluster,
    month,
    month_name,
    monthly_energy_mwh,
    ROUND(SUM(monthly_energy_mwh) OVER (
        PARTITION BY region_cluster
        ORDER BY month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS cumulative_energy_mwh,
    monthly_losses_mwh,
    ROUND(AVG(monthly_losses_mwh) OVER (
        PARTITION BY region_cluster
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_3m_losses_mwh
FROM monthly_stats
ORDER BY month;
