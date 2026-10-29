// ============================================================
// Результат 2: Обмеження цілісності та індекси для Neo4j
// Дисципліна: Сховища знань та управління знаннями (СЗУЗ)
// Студент: Гріджак Олександр (ФЕІ-43)
// ============================================================

// 1. Унікальні обмеження (Constraints) для ключових міток
CREATE CONSTRAINT UniquePowerPlantId IF NOT EXISTS
FOR (p:PowerPlant) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT UniqueSubstationId IF NOT EXISTS
FOR (s:Substation) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT UniqueTransmissionLineId IF NOT EXISTS
FOR (l:TransmissionLine) REQUIRE l.id IS UNIQUE;

CREATE CONSTRAINT UniqueEquipmentId IF NOT EXISTS
FOR (e:Transformer) REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT UniqueEventId IF NOT EXISTS
FOR (ev:GridEvent) REQUIRE ev.id IS UNIQUE;

// 2. Індекси (Indexes) для швидкого пошуку та аналітики
CREATE INDEX SubstationVoltageIndex IF NOT EXISTS
FOR (s:Substation) ON (s.voltageKV);

CREATE INDEX LineCapacityIndex IF NOT EXISTS
FOR (l:TransmissionLine) ON (l.capacityMW);

CREATE INDEX EventRiskScoreIndex IF NOT EXISTS
FOR (ev:GridEvent) ON (ev.riskScore);

CREATE INDEX PlantTypeIndex IF NOT EXISTS
FOR (p:PowerPlant) ON (p.type);

// Перевірка створених обмежень та індексів
SHOW CONSTRAINTS;
SHOW INDEXES;
