// Q8: Аналіз впливу 2 (Каскадний розвиток аварій, глибина >= 3)
// Компетентнісне питання CQ8: Який повний ланцюг ескалації аварійних подій ініціюється коротким замиканням на магістральній ПЛ 750 кВ та які критичні ризики фіксуються на кожному кроці?
MATCH path = (origin:GridEvent {id: 'EV_ShortCircuit_Line750_ZK'})-[:TRIGGERS_EVENT*1..5]->(cascade:GridEvent)
RETURN length(path) AS CascadeStep,
       origin.name AS InitiatingFault,
       cascade.name AS SecondaryConsequence,
       cascade.riskScore AS ConsequenceRiskScore,
       [ev in nodes(path) | ev.name] AS EscalationTrajectory
ORDER BY CascadeStep ASC, ConsequenceRiskScore DESC;
