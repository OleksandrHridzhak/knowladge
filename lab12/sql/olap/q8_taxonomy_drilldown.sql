-- Q8: TAXONOMY DRILL-DOWN — Деталізація показників по ієрархії таксономії (Клас L1 -> Підклас L2 -> Екземпляр з IRI)
SELECT
    CASE
        WHEN GROUPING(t.class_level1_name) = 1 THEN 'L0: УСЯ МЕРЕЖА'
        WHEN GROUPING(t.subclass_level2_name) = 1 THEN 'L1: Клас таксономії'
        WHEN GROUPING(t.equipment_name) = 1 THEN 'L2: Підклас таксономії'
        ELSE 'L3: Екземпляр (IRI)'
    END AS hierarchy_level,
    COALESCE(t.class_level1_name, 'Усі класи') AS class_level1,
    COALESCE(t.subclass_level2_name, 'Усі підкласи') AS subclass_level2,
    COALESCE(t.equipment_name, 'Усі апарати підкласу') AS equipment_instance,
    COALESCE(t.taxonomy_iri, t.parent_iri, 'http://www.semanticweb.org/ontologies/2026/power-grid#GridComponent') AS semantic_iri,
    COUNT(*) AS records_cnt,
    ROUND(SUM(f.energy_transmitted_mwh), 2) AS energy_mwh,
    ROUND(SUM(f.tech_losses_mwh), 2) AS losses_mwh,
    ROUND(SUM(f.outage_duration_min), 2) AS outage_min,
    ROUND(AVG(f.risk_score), 3) AS avg_risk
FROM fact_grid_telemetry f
JOIN dim_taxonomy_equipment t ON f.taxonomy_key = t.taxonomy_key
WHERE t.is_current = TRUE
GROUP BY GROUPING SETS (
    (t.class_level1_name),
    (t.class_level1_name, t.subclass_level2_name, t.parent_iri),
    (t.class_level1_name, t.subclass_level2_name, t.equipment_name, t.taxonomy_iri, t.parent_iri)
)
ORDER BY t.class_level1_name, GROUPING(t.subclass_level2_name) DESC, t.subclass_level2_name, GROUPING(t.equipment_name) DESC, energy_mwh DESC;
