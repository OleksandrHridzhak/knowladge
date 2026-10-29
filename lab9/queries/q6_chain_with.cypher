// Q6: Ланцюгові обчислення з оператором WITH
// Компетентнісне питання CQ6: Які 5 найпотужніших ліній електропередач та які кінцеві споживачі живляться від суміжних підстанцій?
MATCH (l:TransmissionLine)
WHERE l.capacityMW IS NOT NULL
WITH l
ORDER BY l.capacityMW DESC
LIMIT 5
MATCH (l)-[:CONNECTS_TO]->(s:Substation)
OPTIONAL MATCH (s)-[:FEEDS_CONSUMER]->(c:ConsumerNode)
RETURN l.name AS LineName,
       l.capacityMW AS LineCapacityMW,
       s.name AS ConnectedSubstation,
       coalesce(c.name, 'Вузлова транзитна підстанція') AS ServedConsumer,
       coalesce(c.capacityMW, 0.0) AS ConsumerLoadMW;
