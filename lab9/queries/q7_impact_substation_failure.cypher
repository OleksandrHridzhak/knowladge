// Q7: Аналіз впливу 1 (Impact Analysis, глибина >= 3)
// Компетентнісне питання CQ7: Які лінії, проміжні підстанції та кінцеві споживачі опиняться під загрозою знеструмлення у разі аварійного відключення ПС 750 кВ Західноукраїнська?
MATCH path = (root:Substation {id: 'SS_Zakhidna'})-[:CONNECTS_TO|FEEDS_CONSUMER*1..4]-(downstream)
WHERE downstream <> root
WITH downstream, min(length(path)) AS DepthLevel, collect(path)[0] AS SamplePath
RETURN labels(downstream)[0] AS ImpactedType,
       downstream.id AS ImpactedId,
       coalesce(downstream.name, downstream.id) AS ImpactedEntity,
       DepthLevel,
       [n in nodes(SamplePath) | coalesce(n.name, n.id)] AS PropagationChain
ORDER BY DepthLevel ASC, ImpactedType, ImpactedEntity;
