// Q1: Фільтрація підстанцій магістралі з напругою >= 330 кВ
MATCH (s:Substation)
WHERE s.voltageKV >= 330
RETURN s.name AS Substation, s.voltageKV AS Voltage_kV
ORDER BY s.voltageKV DESC, s.name ASC;
