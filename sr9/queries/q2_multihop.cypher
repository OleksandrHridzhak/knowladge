// Q2: Багатохоповий обхід досяжності від АЕС (2..4 хопи)
MATCH p = (p:PowerPlant {type: 'Nuclear'})-[:SUPPLIES_POWER_TO|CONNECTS_TO*2..4]->(s:Substation)
RETURN p.name AS PowerPlant, s.name AS Substation, length(p) AS Hops
ORDER BY Hops ASC, s.name ASC
LIMIT 25;
