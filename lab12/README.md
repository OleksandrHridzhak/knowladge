# Лабораторна робота №12: OLAP-куб на основі таксономії

- **Студент:** Гріджак Олександр (група ФЕІ-43, ЛНУ ім. Івана Франка, ФЕКТ)
- **Курс:** «Сховища знань та управління знаннями»
- **Тематична область:** Моделювання енергомереж (Сектор: Енергетика)
- **Інструменти:** Python 3.12, DuckDB 2.0.0, pandas 2.2.3, PyArrow 21.0.0, sqlglot 30.27.0, PyYAML, Matplotlib

## Структура проєкту та артефакти за результатами
1. **Результат 1 (Зерно, питання та схема):**
   - `docs/star_design.md` - опис бізнес-процесу, зерна факту, 8 бізнес-питань, ієрархій вимірів, політики SCD Тип 1/2 та класифікації мір за адитивністю.
   - `sql/ddl.sql` - DDL зіркової схеми у DuckDB (`fact_grid_telemetry` + 5 вимірів, зокрема `dim_taxonomy_equipment` з глобальними IRI `http://www.semanticweb.org/ontologies/2026/power-grid#`).
   - `docs/scheme.mmd` та `star_schema.png` - діаграма зіркової схеми.
2. **Результат 2 (Завантаження даних ELT):**
   - `etl/load.py` - детермінований генератор (`seed = 42`, `1500` рядків факту), перевірка відсутності «сиріт» (`orphan_count = 0`), 7 перевірок якості даних (`DQ-01..DQ-07`) та експорт у Parquet.
   - `data/*.parquet` - 6 збережених Parquet-файлів зі стисненням ZSTD (`v1.0.0`).
   - `docs/dq_report.md` - звіт перевірок якості та контрольні суми SHA-256.
3. **Результат 3 (OLAP-запити):**
   - `sql/olap/q1_rollup.sql` .. `q8_taxonomy_drilldown.sql` - 8 OLAP-запитів (`ROLLUP`, `CUBE`, `Slice`, `Dice`, `PIVOT`, віконні функції накопичення/ковзного середнього/ранжування, `GROUPING SETS` drill-down по таксономії).
   - `src/run_olap.py` та `docs/olap_results.md` - результати запитів, інженерна інтерпретація та незалежна перевірка 2 результатів через `pandas` (розбіжність `0.000000`).
4. **Результат 4 (Семантичний шар):**
   - `semantic/metrics.yml` - формальний опис 6 бізнес-метрик із власниками, датою перегляду (`2026-11-01`) та статусом `verified`.
   - `src/semantic_layer.py` та `docs/semantic_layer.md` - програмний генератор SQL за назвою метрики та перевірка ідентичності результатів різними шляхами.
5. **Результат 5 (Text-to-SQL та аналітична панель):**
   - `src/text_to_sql.py` та `tests/t2sql.jsonl` - конвеєр Text-to-SQL із семантичним контекстом, AST-валідатором `sqlglot` (лише `SELECT`), примусовим `LIMIT 100`, `EXPLAIN` та тайм-аутом `2.0 с`. Оцінка на 12 питаннях і розбір 3 помилок.
   - `dashboard/generate_dashboard.py`, `dashboard/analytics_panel.png`, `dashboard/index.html`, `docs/dashboard_report.md` - аналітична панель на 4 візуалізації та опис ризиків.
6. **Протокол «LLM-експерт»:**
   - `llm_log/llm_interaction_log.json` та `claims/claims.csv` - журнал взаємодії з LLM та таблиця верифікованих тверджень (рівні V2, V4).

## Відтворюваний запуск з нуля (`seed = 42`)
```powershell
pip install -r requirements.txt
python scripts/run_lab12.py
```
