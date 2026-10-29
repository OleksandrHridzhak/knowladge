// ============================================================
// Результат 2: Ідемпотентний імпорт вузлів через LOAD CSV та MERGE
// ============================================================

// Імпорт електростанцій (PowerPlant)
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.label = 'PowerPlant'
MERGE (n:PowerPlant {id: row.id})
SET n.name = row.name,
    n.type = row.type,
    n.voltageKV = toFloat(row.voltageKV),
    n.capacityMW = toFloat(row.capacityMW),
    n.operational = toBoolean(row.operational),
    n.location = row.location;

// Імпорт підстанцій (Substation)
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.label = 'Substation'
MERGE (n:Substation {id: row.id})
SET n.name = row.name,
    n.type = row.type,
    n.voltageKV = toFloat(row.voltageKV),
    n.operational = toBoolean(row.operational),
    n.location = row.location;

// Імпорт ліній електропередач (TransmissionLine)
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.label = 'TransmissionLine'
MERGE (n:TransmissionLine {id: row.id})
SET n.name = row.name,
    n.type = row.type,
    n.voltageKV = toFloat(row.voltageKV),
    n.capacityMW = toFloat(row.capacityMW),
    n.operational = toBoolean(row.operational),
    n.location = row.location;

// Імпорт трансформаторів (Transformer)
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.label = 'Transformer'
MERGE (n:Transformer {id: row.id})
SET n.name = row.name,
    n.type = row.type,
    n.voltageKV = toFloat(row.voltageKV),
    n.capacityMW = toFloat(row.capacityMW),
    n.operational = toBoolean(row.operational),
    n.location = row.location;

// Імпорт вимикачів (CircuitBreaker)
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.label = 'CircuitBreaker'
MERGE (n:CircuitBreaker {id: row.id})
SET n.name = row.name,
    n.type = row.type,
    n.voltageKV = toFloat(row.voltageKV),
    n.operational = toBoolean(row.operational),
    n.location = row.location;

// Імпорт комплектів релейного захисту (RelayProtection)
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.label = 'RelayProtection'
MERGE (n:RelayProtection {id: row.id})
SET n.name = row.name,
    n.type = row.type,
    n.tripDelayS = toFloat(row.riskScore),
    n.operational = toBoolean(row.operational),
    n.location = row.location;

// Імпорт систем диспетчеризації SCADA (SCADA_System)
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.label = 'SCADA_System'
MERGE (n:SCADA_System {id: row.id})
SET n.name = row.name,
    n.type = row.type,
    n.operational = toBoolean(row.operational),
    n.location = row.location;

// Імпорт вузлів споживання (ConsumerNode)
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.label = 'ConsumerNode'
MERGE (n:ConsumerNode {id: row.id})
SET n.name = row.name,
    n.type = row.type,
    n.voltageKV = toFloat(row.voltageKV),
    n.capacityMW = toFloat(row.capacityMW),
    n.operational = toBoolean(row.operational),
    n.location = row.location;

// Імпорт подій та аварій (GridEvent)
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.label = 'GridEvent'
MERGE (n:GridEvent {id: row.id})
SET n.name = row.name,
    n.type = row.type,
    n.riskScore = toFloat(row.riskScore),
    n.location = row.location;

// Імпорт системного оператора (Operator)
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
WITH row WHERE row.label = 'Operator'
MERGE (n:Operator {id: row.id})
SET n.name = row.name,
    n.type = row.type,
    n.location = row.location;

// Перевірка кількості імпортованих вузлів
MATCH (n) RETURN count(n) AS totalNodes;
