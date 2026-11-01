// Q5: Каскадний аналіз вимкнення ліній при спрацюванні РЗА автотрансформатора
MATCH (rp:RelayProtection)-[:TRIPS_BREAKER]->(cb:CircuitBreaker)<-[:CONTAINS_EQUIPMENT]-(ss:Substation)-[:CONNECTS_TO]->(tl:TransmissionLine)
WHERE ss.voltageKV >= 330
RETURN rp.name AS ProtectionRelay,
       cb.name AS Breaker,
       ss.name AS Substation,
       collect(tl.name) AS DeEnergizedLines
ORDER BY ss.name ASC
LIMIT 10;

