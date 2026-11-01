// Q4: Агрегація встановленої потужності генерації за типами станцій
MATCH (p:PowerPlant)
RETURN p.type AS GenerationType,
       count(p) AS PlantCount,
       sum(p.capacityMW) AS TotalCapacityMW,
       round(avg(p.capacityMW), 1) AS AvgCapacityMW
ORDER BY TotalCapacityMW DESC;

