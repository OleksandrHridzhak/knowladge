// ============================================================
// Результат 2: Ідемпотентний імпорт зв'язків з атрибутами походження
// ============================================================

// 1. Постачання потужності (SUPPLIES_POWER_TO)
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'SUPPLIES_POWER_TO'
MATCH (source {id: row.start_id})
MATCH (target {id: row.end_id})
MERGE (source)-[r:SUPPLIES_POWER_TO]->(target)
SET r.source = row.source,
    r.confidence = toFloat(row.confidence),
    r.validFrom = date(row.validFrom);

// 2. Топологічне з'єднання (CONNECTS_TO)
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'CONNECTS_TO'
MATCH (source {id: row.start_id})
MATCH (target {id: row.end_id})
MERGE (source)-[r:CONNECTS_TO]->(target)
SET r.source = row.source,
    r.confidence = toFloat(row.confidence),
    r.validFrom = date(row.validFrom);

// 3. Розміщення обладнання (CONTAINS_EQUIPMENT)
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'CONTAINS_EQUIPMENT'
MATCH (source {id: row.start_id})
MATCH (target {id: row.end_id})
MERGE (source)-[r:CONTAINS_EQUIPMENT]->(target)
SET r.source = row.source,
    r.confidence = toFloat(row.confidence),
    r.validFrom = date(row.validFrom);

// 4. Релейний захист обладнання (PROTECTS)
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'PROTECTS'
MATCH (source {id: row.start_id})
MATCH (target {id: row.end_id})
MERGE (source)-[r:PROTECTS]->(target)
SET r.source = row.source,
    r.confidence = toFloat(row.confidence),
    r.validFrom = date(row.validFrom);

// 5. Дія на вимикач (TRIPS_BREAKER)
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'TRIPS_BREAKER'
MATCH (source {id: row.start_id})
MATCH (target {id: row.end_id})
MERGE (source)-[r:TRIPS_BREAKER]->(target)
SET r.source = row.source,
    r.confidence = toFloat(row.confidence),
    r.validFrom = date(row.validFrom);

// 6. Телеметрія та моніторинг SCADA (MONITORED_BY)
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'MONITORED_BY'
MATCH (source {id: row.start_id})
MATCH (target {id: row.end_id})
MERGE (source)-[r:MONITORED_BY]->(target)
SET r.source = row.source,
    r.confidence = toFloat(row.confidence),
    r.validFrom = date(row.validFrom);

// 7. Електропостачання споживача (FEEDS_CONSUMER)
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'FEEDS_CONSUMER'
MATCH (source {id: row.start_id})
MATCH (target {id: row.end_id})
MERGE (source)-[r:FEEDS_CONSUMER]->(target)
SET r.source = row.source,
    r.confidence = toFloat(row.confidence),
    r.validFrom = date(row.validFrom);

// 8. Каскадний розвиток подій (TRIGGERS_EVENT)
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'TRIGGERS_EVENT'
MATCH (source {id: row.start_id})
MATCH (target {id: row.end_id})
MERGE (source)-[r:TRIGGERS_EVENT]->(target)
SET r.source = row.source,
    r.confidence = toFloat(row.confidence),
    r.validFrom = date(row.validFrom);

// 9. Оперативне управління (MANAGED_BY)
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
WITH row WHERE row.type = 'MANAGED_BY'
MATCH (source {id: row.start_id})
MATCH (target {id: row.end_id})
MERGE (source)-[r:MANAGED_BY]->(target)
SET r.source = row.source,
    r.confidence = toFloat(row.confidence),
    r.validFrom = date(row.validFrom);

// Підрахунок створених зв'язків
MATCH ()-[r]->() RETURN count(r) AS totalRelationships;
