// Q5: Опційні співставлення (OPTIONAL MATCH)
// Компетентнісне питання CQ5: Які підстанції мають встановлені автотрансформатори та які вимикачі чи комплекти захисту з ними пов'язані?
MATCH (s:Substation)
WHERE s.voltageKV >= 330.0
OPTIONAL MATCH (s)-[:CONTAINS_EQUIPMENT]->(t:Transformer)
OPTIONAL MATCH (s)-[:CONTAINS_EQUIPMENT]->(cb:CircuitBreaker)
OPTIONAL MATCH (rp:RelayProtection)-[:PROTECTS]->(t)
RETURN s.name AS Substation,
       s.voltageKV AS VoltageKV,
       collect(DISTINCT coalesce(t.name, 'Без трансформатора')) AS Transformers,
       collect(DISTINCT coalesce(cb.name, 'Без вимикача')) AS CircuitBreakers,
       collect(DISTINCT coalesce(rp.name, 'Без окремого захисту')) AS RelayProtectionSystems
ORDER BY s.voltageKV DESC, Substation
LIMIT 10;
