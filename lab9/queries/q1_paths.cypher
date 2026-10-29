// Q1: Шляхи змінної довжини (*1..4)
// Компетентнісне питання CQ1: Які магістральні підстанції досяжні від атомних електростанцій через ланцюги передачі потужності до 4 стрибків?
MATCH path = (p:PowerPlant {type: 'Nuclear'})-[:SUPPLIES_POWER_TO|CONNECTS_TO*1..4]-(s:Substation)
WHERE s.voltageKV >= 330.0
RETURN p.name AS PowerPlant,
       length(path) AS HopLength,
       [node in nodes(path) | coalesce(node.name, node.id)] AS TransmissionPath,
       s.name AS TargetSubstation
ORDER BY HopLength ASC, PowerPlant
LIMIT 15;
