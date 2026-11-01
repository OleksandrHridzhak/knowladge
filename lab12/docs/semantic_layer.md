# Специфікація семантичного шару та перевірка узгодженості (Результат 4)

## 1. Реєстр бізнес-метрик (`semantic/metrics.yml`)
| Код метрики | Назва | Формула SQL | Одиниця | Адитивність | Власник | Дата перегляду | Статус |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: | :---: |
| `total_energy_mwh` | Сумарний обсяг переданої електроенергії | `ROUND(SUM(f.energy_transmitted_mwh), 2)` | МВт·год | `additive` | Центральна диспетчерська служба НЕК Укренерго (Аналітичний відділ) | 2026-11-01 | **verified** |
| `loss_rate_pct` | Питомий коефіцієнт технологічних втрат | `ROUND(SUM(f.tech_losses_mwh) * 100.0 / NULLIF(SUM(f.energy_transmitted_mwh), 0), 3)` | % | `non-additive` | Служба режимів та балансів потужності (Група нормативних втрат) | 2026-11-01 | **verified** |
| `avg_load_factor_pct` | Середній коефіцієнт завантаження обладнання | `ROUND(AVG(f.load_factor_pct), 2)` | % | `non-additive` | Відділ експлуатації підстанцій та ліній 330-750 кВ | 2026-11-01 | **verified** |
| `protection_trip_frequency` | Частота спрацювань релейного захисту (РЗА) | `SUM(f.protection_trips_count)` | спрацювань | `additive` | Служба релейного захисту та протиаварійної автоматики (СРЗА) | 2026-11-01 | **verified** |
| `saidi_outage_min_per_unit` | Питома тривалість аварійного простою на одиницю обладнання | `ROUND(SUM(f.outage_duration_min) * 1.0 / NULLIF(COUNT(DISTINCT f.taxonomy_key), 0), 2)` | хв/об'єкт | `non-additive` | Інспекція надійності та технологічного нагляду ОЕС | 2026-11-01 | **verified** |
| `critical_risk_rate_pct` | Частка критичних режимів за індексом каскадного ризику | `ROUND(SUM(CASE WHEN f.risk_score >= 0.75 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2)` | % | `non-additive` | Група аналізу стійкості енергосистеми та критерію N-1 | 2026-11-01 | **verified** |

## 2. Автоматична генерація SQL за назвою метрики (`src/semantic_layer.py`)
### Приклад 1: Генерація запиту для `loss_rate_pct` та `total_energy_mwh` за `region_cluster`
```sql
SELECT
    s.region_cluster AS region_cluster,
    ROUND(SUM(f.energy_transmitted_mwh), 2) AS total_energy_mwh,
    ROUND(SUM(f.tech_losses_mwh) * 100.0 / NULLIF(SUM(f.energy_transmitted_mwh), 0), 3) AS loss_rate_pct
FROM fact_grid_telemetry f
JOIN dim_substation s ON f.substation_key = s.substation_key
GROUP BY s.region_cluster
ORDER BY region_cluster;
```
| region_cluster   |   total_energy_mwh |   loss_rate_pct |
|:-----------------|-------------------:|----------------:|
| Дніпровський     |           262528   |           2.542 |
| Західний         |           256322   |           2.471 |
| Південний        |            41608.6 |           2.602 |
| Центральний      |           437979   |           2.568 |

### Приклад 2: Генерація запиту для `saidi_outage_min_per_unit` та `protection_trip_frequency` за `class_level1_name`
```sql
SELECT
    t.class_level1_name AS class_level1_name,
    SUM(f.protection_trips_count) AS protection_trip_frequency,
    ROUND(SUM(f.outage_duration_min) * 1.0 / NULLIF(COUNT(DISTINCT f.taxonomy_key), 0), 2) AS saidi_outage_min_per_unit
FROM fact_grid_telemetry f
JOIN dim_taxonomy_equipment t ON f.taxonomy_key = t.taxonomy_key AND t.is_current = TRUE
GROUP BY t.class_level1_name
ORDER BY class_level1_name;
```
| class_level1_name                  |   protection_trip_frequency |   saidi_outage_min_per_unit |
|:-----------------------------------|----------------------------:|----------------------------:|
| Магістральні лінії електропередачі |                         354 |                      475.47 |
| Релейний захист та комутація       |                         355 |                      511.66 |
| Силове трансформаторне обладнання  |                         254 |                      578.03 |

## 3. Перевірка узгодженості результатів різними шляхами (Крок 3)
- **Питання 1 (`loss_rate_pct` за енергорайонами: Семантичний шар vs Еталонний OLAP ROLLUP):** максимальна розбіжність = `0.000000%` (Повний збіг).
- **Питання 2 (`saidi_outage_min_per_unit` за класами таксономії: Семантичний шар vs Двокроковий CTE по індивідах):** максимальна розбіжність = `0.000000 хв` (Повний збіг).
