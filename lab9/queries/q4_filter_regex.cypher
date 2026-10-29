// Q4: Фільтрація за числовим порогом та регулярними виразами
// Компетентнісне питання CQ4: Які лінії та підстанції напругою від 330 кВ містять у назві або розташуванні ключові слова західного та київського регіонів?
MATCH (n)
WHERE (n:Substation OR n:TransmissionLine)
  AND n.voltageKV >= 330.0
  AND (n.name =~ '(?i).*(Західн|Київ|Львів).*' OR n.location =~ '(?i).*(Київ|Стрий|Львів).*')
RETURN labels(n)[0] AS EntityType,
       n.id AS EntityId,
       n.name AS EntityName,
       n.voltageKV AS VoltageKV,
       coalesce(n.location, 'Не вказано') AS Location
ORDER BY n.voltageKV DESC, EntityName;
