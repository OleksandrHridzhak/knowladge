// Q3: Агрегації та підрахунки (COUNT, SUM, AVG, GROUP BY)
// Компетентнісне питання CQ3: Яка сумарна встановлена потужність генерації за типами станцій та середня напруга підстанцій у регіонах?
MATCH (p:PowerPlant)
RETURN p.type AS GenerationType,
       count(p) AS PlantCount,
       sum(p.capacityMW) AS TotalCapacityMW,
       avg(p.capacityMW) AS AvgCapacityMW
ORDER BY TotalCapacityMW DESC;
