-- ============================================================================
-- Самостійна робота №12: Проєктування зіркової схеми
-- Студент: Гріджак Олександр (група ФЕІ-43, ЛНУ ім. Івана Франка)
-- Процес: Аудит надійності електропостачання та облік недовідпуску (ENS/SAIDI)
-- СУБД: DuckDB (Зіркова схема: 1 таблиця фактів + 5 таблиць вимірів)
-- ============================================================================

DROP TABLE IF EXISTS fact_outage_balance;
DROP TABLE IF EXISTS dim_time;
DROP TABLE IF EXISTS dim_grid_node;
DROP TABLE IF EXISTS dim_equipment_taxonomy;
DROP TABLE IF EXISTS dim_outage_cause;
DROP TABLE IF EXISTS dim_consumer_category;

-- 1. Вимір часу інциденту (dim_time)
-- Ієрархія: year -> quarter -> month -> full_date -> peak_period
CREATE TABLE dim_time (
    time_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER NOT NULL CHECK (year BETWEEN 2020 AND 2030),
    quarter VARCHAR(4) NOT NULL CHECK (quarter IN ('Q1', 'Q2', 'Q3', 'Q4')),
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    season VARCHAR(16) NOT NULL CHECK (season IN ('Зима', 'Весна', 'Літо', 'Осінь')),
    peak_period VARCHAR(24) NOT NULL CHECK (peak_period IN ('Ранковий пік', 'Денна зона', 'Вечірній максимум', 'Нічний провал'))
);

-- 2. Вимір вузлів мережі та приєднань (dim_grid_node) - SCD Тип 1
-- Ієрархія: region_cluster -> oblast -> substation_name -> feeder_code
CREATE TABLE dim_grid_node (
    node_key INTEGER PRIMARY KEY,
    feeder_code VARCHAR(32) NOT NULL UNIQUE,
    substation_name VARCHAR(100) NOT NULL,
    oblast VARCHAR(60) NOT NULL,
    region_cluster VARCHAR(40) NOT NULL,
    voltage_kv INTEGER NOT NULL CHECK (voltage_kv IN (110, 330, 750))
);

-- 3. Вимір класів обладнання з таксономією IRI (dim_equipment_taxonomy) - SCD Тип 2
-- Ієрархія: class_l1 -> subclass_l2 -> apparatus_model
CREATE TABLE dim_equipment_taxonomy (
    equipment_key INTEGER PRIMARY KEY,
    natural_code VARCHAR(32) NOT NULL,
    apparatus_model VARCHAR(120) NOT NULL,
    class_l1 VARCHAR(80) NOT NULL,
    subclass_l2 VARCHAR(80) NOT NULL,
    ontology_iri VARCHAR(180) NOT NULL CHECK (ontology_iri LIKE 'http://www.semanticweb.org/ontologies/2026/power-grid#%'),
    rated_power_mva DOUBLE NOT NULL CHECK (rated_power_mva > 0),
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL,
    is_current BOOLEAN NOT NULL,
    CHECK (valid_from < valid_to)
);

-- 4. Вимір першопричин аварійних відключень (dim_outage_cause) - SCD Тип 1
-- Ієрархія: cause_group -> cause_detail -> protection_stage
CREATE TABLE dim_outage_cause (
    cause_key INTEGER PRIMARY KEY,
    cause_code VARCHAR(32) NOT NULL UNIQUE,
    cause_group VARCHAR(60) NOT NULL,
    cause_detail VARCHAR(100) NOT NULL,
    protection_stage VARCHAR(60) NOT NULL
);

-- 5. Вимір категорій надійності споживачів (dim_consumer_category)
-- Ієрархія: reliability_tier -> sector_name -> tariff_group
CREATE TABLE dim_consumer_category (
    consumer_key INTEGER PRIMARY KEY,
    tier_code VARCHAR(24) NOT NULL UNIQUE,
    reliability_tier VARCHAR(40) NOT NULL,
    sector_name VARCHAR(80) NOT NULL,
    tariff_group VARCHAR(40) NOT NULL,
    penalty_rate_uah_per_mwh DOUBLE NOT NULL CHECK (penalty_rate_uah_per_mwh >= 0)
);

-- 6. Таблиця фактів (fact_outage_balance)
-- Зерно: один зафіксований інцидент небалансу/знеструмлення на приєднанні підстанції
CREATE TABLE fact_outage_balance (
    incident_id INTEGER PRIMARY KEY,
    time_key INTEGER NOT NULL REFERENCES dim_time(time_key),
    node_key INTEGER NOT NULL REFERENCES dim_grid_node(node_key),
    equipment_key INTEGER NOT NULL REFERENCES dim_equipment_taxonomy(equipment_key),
    cause_key INTEGER NOT NULL REFERENCES dim_outage_cause(cause_key),
    consumer_key INTEGER NOT NULL REFERENCES dim_consumer_category(consumer_key),
    -- Адитивні міри (Additive)
    ens_unsupplied_mwh DOUBLE NOT NULL CHECK (ens_unsupplied_mwh >= 0.0),
    restoration_duration_min DOUBLE NOT NULL CHECK (restoration_duration_min >= 0.0),
    affected_consumers_cnt INTEGER NOT NULL CHECK (affected_consumers_cnt >= 0),
    compensation_cost_uah DOUBLE NOT NULL CHECK (compensation_cost_uah >= 0.0),
    -- Напівадитивні міри (Semi-additive)
    disconnected_load_mw DOUBLE NOT NULL CHECK (disconnected_load_mw >= 0.0),
    spinning_reserve_mw DOUBLE NOT NULL CHECK (spinning_reserve_mw >= 0.0),
    -- Неадитивні міри (Non-additive)
    voltage_deviation_pct DOUBLE NOT NULL CHECK (voltage_deviation_pct BETWEEN -50.0 AND 50.0),
    frequency_nadir_hz DOUBLE NOT NULL CHECK (frequency_nadir_hz BETWEEN 47.0 AND 51.0)
);
