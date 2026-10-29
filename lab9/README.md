# Лабораторна робота № 9: Графова база знань у Neo4j

- **Студент:** Гріджак Олександр (група ФЕІ-43)
- **Дисципліна:** «Сховища знань та управління знаннями» (СЗУЗ)
- **Викладач:** Асист. Керод Тарас
- **Тематична область:** Моделювання енергомереж
- **Стек реалізації:** Python 3.12 (драйвер `neo4j`, `networkx`, `matplotlib`, `pandas`), Cypher, Neo4j, Docker

---

## 1. Склад артефактів роботи

Робота містить усі обов'язкові результати та супровідні матеріали згідно з методичними вимогами:

### Результат 1: Графова схема під CQ
- `docs/graph_schema.pdf` та `docs/graph_schema.png` — діаграма Property Graph (LPG) з 10 мітками вузлів, 9 типами зв'язків та атрибутами походження.
- `docs/scheme.mmd` — вихідний код схеми у форматі Mermaid.
- `docs/cq_mapping.md` — відображення 8 компетентнісних питань (CQ1–CQ8) на Cypher-шаблони та порівняльна таблиця трансформації онтології з ЛР 7–8 у граф властивостей.

### Результат 2: Імпорт, обмеження та індекси
- `data/nodes.csv` — набір із **146 вузлів** (електростанції, підстанції 750/330/110 кВ, лінії, трансформатори, вимикачі, РЗА, SCADA, споживачі, події, оператор).
- `data/relationships.csv` — набір із **280 типізованих зв'язків** з обов'язковими атрибутами походження (`source`, `confidence`, `validFrom`).
- `import/01_constraints_and_indexes.cypher` — декларація 5 унікальних обмежень та 4 індексів.
- `import/02_import_nodes.cypher` — ідемпотентний імпорт вузлів через `LOAD CSV` та `MERGE`.
- `import/03_import_relationships.cypher` — ідемпотентний імпорт зв'язків.
- `import/04_test_idempotency_and_violation.cypher` — верифікація ідемпотентності та демонстрація блокування дубліката з кодом помилки `ConstraintValidationFailed`.

### Результат 3: Запити Cypher
- `queries/q1_paths.cypher` — шляхи змінної довжини (`*1..4`) від АЕС до підстанцій.
- `queries/q2_shortest_path.cypher` — пошук найкоротшого шляху передачі через `shortestPath`.
- `queries/q3_aggregations.cypher` — агрегації `COUNT`, `SUM`, `AVG`, `GROUP BY` за типами генерації.
- `queries/q4_filter_regex.cypher` — комбінована фільтрація за напругою та регулярними виразами.
- `queries/q5_optional_match.cypher` — опційні зв'язки `OPTIONAL MATCH` для аудиту РЗА та вимикачів.
- `queries/q6_chain_with.cypher` — ланцюгові обчислення з оператором `WITH`.
- `queries/q7_impact_substation_failure.cypher` — аналіз впливу 1 (Impact Analysis, глибина $\ge 3$) у разі відмови ПС 750 кВ Західноукраїнська.
- `queries/q8_impact_relay_cascade.cypher` — аналіз впливу 2 (ескалація каскадної аварії від короткого замикання, глибина $\ge 3$).
- `queries/manual_check_subgraph.cypher` — ручна верифікація 3 запитів на виділеному малому підграфі з 5 вузлів зі 100% збігом.
- `docs/cypher_results.md` — повний звіт із результатами виконання всіх запитів та інженерною інтерпретацією.

### Результат 4: Аналіз графа та продуктивність
- `scripts/graph_analytics.py` — розрахунок PageRank (топ-10 вузлів) та виявлення регіональних спільнот (Louvain / NetworkX / Neo4j GDS).
- `docs/gds_report.md` — аналітичний звіт за алгоритмами GDS, збереження властивостей у графі та оцінка планів `PROFILE` з прискоренням пошуку у 5.2 раза.

### Результат 5: Порівняння зі SPARQL та text-to-Cypher
- `docs/sparql_vs_cypher.md` — детальне порівняння 5 запитів SPARQL vs Cypher, матриця характеристик за 6 критеріями.
- `scripts/text_to_cypher.py` — пайплайн перевірки text-to-Cypher з Read-Only захистом та обов'язковим `LIMIT`.
- `tests/t2c.jsonl` — тестовий бенчмарк із 12 сценаріїв (100% точність на валідних питаннях та детальний аналіз 3 крайових помилок).

### Протокол «LLM-експерт»
- `llm_log/llm_interaction_log.json` — журнал запитів, моделей, параметрів (температура, seed), підказок та людських рішень.
- `claims/claims.csv` — таблиця 10 інженерних тверджень із рівнями верифікації V1–V4 та джерелами.

---

## 2. Відтворення та запуск з нуля

1. **Запуск графової бази даних Neo4j (через Docker Compose):**
   ```powershell
   docker compose up -d
   ```
   *Веб-інтерфейс Neo4j Browser доступний за адресою: `http://localhost:7474` (логін: `neo4j`, пароль: `energygrid2026`).*

2. **Встановлення залежностей Python:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Повний цикл генерації та тестування (Python runner):**
   ```powershell
   python scripts/run_lab9.py
   ```

4. **Окремі етапи виконання (за потреби):**
   ```powershell
   # Генерація CSV даних:
   python scripts/generate_data.py

   # Аналіз графа PageRank та Louvain:
   python scripts/graph_analytics.py

   # Тестування Text-to-Cypher та безпеки:
   python scripts/text_to_cypher.py

   # Генерація академічної схеми:
   python scripts/generate_diagram.py
   ```
