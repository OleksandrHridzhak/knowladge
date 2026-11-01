-- ============================================================================
-- Лабораторна робота №12: OLAP-куб на основі таксономії
-- Студент: Гріджак Олександр (група ФЕІ-43, ЛНУ ім. Івана Франка)
-- Тематична область: Моделювання енергомереж (Сектор: Енергетика)
-- СУБД: DuckDB (Зіркова схема: 5 таблиць вимірів + 1 таблиця фактів)
-- ============================================================================

DROP TABLE IF EXISTS fact_grid_telemetry;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_taxonomy_equipment;
DROP TABLE IF EXISTS dim_substation;
DROP TABLE IF EXISTS dim_event_type;
DROP TABLE IF EXISTS dim_weather;

-- 1. Вимір часу (dim_date)
-- Ієрархія: year -> quarter -> month -> full_date -> hour
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER NOT NULL CHECK (year BETWEEN 2020 AND 2030),
    quarter VARCHAR(4) NOT NULL CHECK (quarter IN ('Q1', 'Q2', 'Q3', 'Q4')),
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    month_name VARCHAR(20) NOT NULL,
    day_of_month INTEGER NOT NULL CHECK (day_of_month BETWEEN 1 AND 31),
    day_of_week VARCHAR(16) NOT NULL,
    hour INTEGER NOT NULL CHECK (hour BETWEEN 0 AND 23),
    season VARCHAR(16) NOT NULL CHECK (season IN ('Зима', 'Весна', 'Літо', 'Осінь')),
    is_peak_hour BOOLEAN NOT NULL
);

-- 2. Вимір обладнання на основі таксономії (dim_taxonomy_equipment)
-- Ієрархія: class_level1_name -> subclass_level2_name -> equipment_name
-- Використовує глобальні IRI з онтології ЛР5/ЛР6 та політику SCD Type 2
CREATE TABLE dim_taxonomy_equipment (
    taxonomy_key INTEGER PRIMARY KEY,
    equipment_code VARCHAR(32) NOT NULL,
    equipment_name VARCHAR(120) NOT NULL,
    taxonomy_iri VARCHAR(180) NOT NULL CHECK (taxonomy_iri LIKE 'http://www.semanticweb.org/ontologies/2026/power-grid#%'),
    parent_iri VARCHAR(180) NOT NULL CHECK (parent_iri LIKE 'http://www.semanticweb.org/ontologies/2026/power-grid#%'),
    class_level1_name VARCHAR(80) NOT NULL,
    subclass_level2_name VARCHAR(80) NOT NULL,
    nominal_voltage_kv DOUBLE NOT NULL CHECK (nominal_voltage_kv > 0),
    rated_capacity_mw DOUBLE NOT NULL CHECK (rated_capacity_mw > 0),
    effective_from DATE NOT NULL,
    effective_to DATE NOT NULL,
    is_current BOOLEAN NOT NULL,
    CHECK (effective_from < effective_to)
);

-- 3. Вимір підстанцій та регіональних диспетчерських центрів (dim_substation)
-- Ієрархія: region_cluster -> oblast -> substation_name (SCD Type 1)
CREATE TABLE dim_substation (
    substation_key INTEGER PRIMARY KEY,
    substation_code VARCHAR(32) NOT NULL UNIQUE,
    substation_name VARCHAR(120) NOT NULL,
    region_cluster VARCHAR(40) NOT NULL,
    oblast VARCHAR(60) NOT NULL,
    voltage_class_kv INTEGER NOT NULL CHECK (voltage_class_kv IN (110, 330, 750)),
    n1_compliant BOOLEAN NOT NULL
);

-- 4. Вимір типів режимних та аварійних подій (dim_event_type)
-- Ієрархія: event_category -> event_subclass (з IRI класів подій)
CREATE TABLE dim_event_type (
    event_type_key INTEGER PRIMARY KEY,
    event_code VARCHAR(32) NOT NULL UNIQUE,
    event_category VARCHAR(60) NOT NULL,
    event_subclass VARCHAR(80) NOT NULL,
    event_iri VARCHAR(180) NOT NULL CHECK (event_iri LIKE 'http://www.semanticweb.org/ontologies/2026/power-grid#%'),
    severity_level INTEGER NOT NULL CHECK (severity_level BETWEEN 1 AND 5),
    protection_action VARCHAR(80) NOT NULL
);

-- 5. Вимір метеорологічних факторів ризику (dim_weather)
CREATE TABLE dim_weather (
    weather_key INTEGER PRIMARY KEY,
    condition_code VARCHAR(32) NOT NULL UNIQUE,
    condition_name VARCHAR(80) NOT NULL,
    wind_speed_group VARCHAR(40) NOT NULL,
    icing_risk_level VARCHAR(24) NOT NULL CHECK (icing_risk_level IN ('Низький', 'Середній', 'Високий', 'Критичний')),
    ambient_temp_c DOUBLE NOT NULL CHECK (ambient_temp_c BETWEEN -40.0 AND 50.0)
);

-- 6. Таблиця фактів (fact_grid_telemetry)
-- Зерно: один погодинний інтервал моніторингу одиниці обладнання на підстанції
CREATE TABLE fact_grid_telemetry (
    telemetry_id INTEGER PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    taxonomy_key INTEGER NOT NULL REFERENCES dim_taxonomy_equipment(taxonomy_key),
    substation_key INTEGER NOT NULL REFERENCES dim_substation(substation_key),
    event_type_key INTEGER NOT NULL REFERENCES dim_event_type(event_type_key),
    weather_key INTEGER NOT NULL REFERENCES dim_weather(weather_key),
    -- Адитивні міри (Additive)
    energy_transmitted_mwh DOUBLE NOT NULL CHECK (energy_transmitted_mwh >= 0.0),
    tech_losses_mwh DOUBLE NOT NULL CHECK (tech_losses_mwh >= 0.0),
    outage_duration_min DOUBLE NOT NULL CHECK (outage_duration_min >= 0.0 AND outage_duration_min <= 60.0),
    protection_trips_count INTEGER NOT NULL CHECK (protection_trips_count >= 0),
    -- Напівадитивні міри (Semi-additive)
    active_load_mw DOUBLE NOT NULL CHECK (active_load_mw >= 0.0),
    available_reserve_mw DOUBLE NOT NULL CHECK (available_reserve_mw >= 0.0),
    -- Неадитивні міри (Non-additive)
    load_factor_pct DOUBLE NOT NULL CHECK (load_factor_pct >= 0.0 AND load_factor_pct <= 160.0),
    voltage_level_kv DOUBLE NOT NULL CHECK (voltage_level_kv >= 0.0),
    risk_score DOUBLE NOT NULL CHECK (risk_score >= 0.0 AND risk_score <= 1.0),
    CHECK (tech_losses_mwh <= energy_transmitted_mwh)
);
