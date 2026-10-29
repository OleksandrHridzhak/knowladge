// ============================================================
// Результат 2: Тестування ідемпотентності та порушення обмежень
// ============================================================

// 1. Тест ідемпотентності:
// Повторне виконання MERGE для існуючого вузла не повинно змінювати кількість вузлів у графі.
MERGE (s:Substation {id: 'SS_Zakhidna'})
ON MATCH SET s.lastVerified = datetime()
RETURN s.id, s.name, s.voltageKV;

// Кількість вузлів залишається незмінною:
MATCH (n) RETURN count(n) AS nodesAfterReImport;

// 2. Демонстрація порушення обмеження унікальності (Constraint Violation):
// Спроба вставити вузол з існуючим id через CREATE замість MERGE.
// Очікуваний виняток Neo4j:
// Neo.ClientError.Schema.ConstraintValidationFailed:
// Node(id) already exists with label `Substation` and property `id` = 'SS_Zakhidna'
CREATE (dup:Substation {
    id: 'SS_Zakhidna',
    name: 'Дублікат Західноукраїнської ПС',
    voltageKV: 750.0
});
