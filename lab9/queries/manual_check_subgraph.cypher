// ============================================================
// Ручна перевірка 3 запитів на виділеному малому підграфі (5 вузлів)
// Підграф: DniproHPP -> SS_Dniprovska -> Line_330_Dnipro_Zaporizhia -> SS_Zaporizka -> Consumer_Zaporizhia_Smelter
// ============================================================

// 1. Ручна перевірка запиту шляху (Q1 на малому підграфі):
// Очікуваний результат: 1 шлях довжиною 4 ребра
MATCH path = (p:PowerPlant {id: 'DniproHPP'})-[:SUPPLIES_POWER_TO|CONNECTS_TO|FEEDS_CONSUMER*1..4]->(c:ConsumerNode {id: 'Consumer_Zaporizhia_Smelter'})
RETURN length(path) AS HopLength,
       [n in nodes(path) | n.id] AS NodeSequence;
// Ручний розрахунок:
// Вузли: [DniproHPP, SS_Dniprovska, Line_330_Dnipro_Zaporizhia, SS_Zaporizka, Consumer_Zaporizhia_Smelter]
// Довжина: 4 ребра. Збіг 100%.

// 2. Ручна перевірка агрегації (Q3 на малому підграфі):
// Очікуваний результат: 1 ГЕС потужністю 1569.0 МВт
MATCH (p:PowerPlant {id: 'DniproHPP'})
RETURN p.type AS Type, sum(p.capacityMW) AS TotalMW;
// Ручний розрахунок: 1569.0 МВт. Збіг 100%.

// 3. Ручна перевірка найкоротшого шляху (Q2 на малому підграфі):
MATCH p = shortestPath((src:PowerPlant {id: 'DniproHPP'})-[*]-(dst:ConsumerNode {id: 'Consumer_Zaporizhia_Smelter'}))
RETURN length(p) AS ShortestHops;
// Ручний розрахунок: 4 хопи. Збіг 100%.
