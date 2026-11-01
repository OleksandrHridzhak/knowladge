// Q3: Найкоротший шлях транзиту потужності Дніпровська -> Західноукраїнська
MATCH (start:Substation {name: 'ПС 750 кВ Дніпровська'}),
      (target:Substation {name: 'ПС 750 кВ Західноукраїнська'}),
      p = shortestPath((start)-[:CONNECTS_TO*]-(target))
RETURN [n in nodes(p) | n.name] AS Path, length(p) AS Distance;
