// Q2: Найкоротший шлях через shortestPath
// Компетентнісне питання CQ2: Який найкоротший фізичний маршрут передачі енергії від Дніпровської ГЕС до Львівської агломерації?
MATCH (source:PowerPlant {id: 'DniproHPP'}),
      (target:ConsumerNode {id: 'Consumer_Lviv_Metropolis'})
MATCH path = shortestPath((source)-[:SUPPLIES_POWER_TO|CONNECTS_TO|FEEDS_CONSUMER*]-(target))
RETURN source.name AS OriginPlant,
       target.name AS DestinationConsumer,
       length(path) AS RouteLengthHops,
       [node in nodes(path) | coalesce(node.name, node.id)] AS RouteNodes,
       [rel in relationships(path) | type(rel)] AS RelationshipSequence;
