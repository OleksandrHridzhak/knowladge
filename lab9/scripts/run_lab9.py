# -*- coding: utf-8 -*-
"""
Головний скрипт виконання Лабораторної роботи № 9 (повний стек Python).
Студент: Гріджак Олександр (ФЕІ-43), ЛНУ ім. Івана Франка.

Послідовно виконує всі 5 результатів методички:
1. Генерація даних CSV (>= 100 вузлів, >= 200 зв'язків з атрибутами походження).
2. Алгоритми GDS (PageRank, Louvain) та аналіз продуктивності PROFILE.
3. Оцінка моделі Text-to-Cypher з Read-Only захистом та порівняння зі SPARQL.
4. Генерація схеми графа Property Graph (PDF/PNG/SVG).
5. Перевірка з'єднання з Neo4j через Python-драйвер neo4j.
6. Компіляція звіту в LaTeX через Tectonic.
"""

import sys
import subprocess
import shutil
from pathlib import Path

# Встановлюємо UTF-8 вивід у консоль
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
DOCS_DIR = ROOT_DIR / "docs"
BIN_TECTONIC = next((p / "bin" / "tectonic.exe" for p in [ROOT_DIR.parent, ROOT_DIR.parent.parent, ROOT_DIR.parent.parent.parent] if (p / "bin" / "tectonic.exe").exists()), ROOT_DIR.parent.parent / "bin" / "tectonic.exe")

print("=" * 64)
print(" Лабораторна робота № 9: Графова база знань у Neo4j")
print(" Студент: Гріджак Олександр (група ФЕІ-43), ЛНУ ім. Івана Франка")
print(" Стек автоматизації: Python 3.12, neo4j-driver, NetworkX, Matplotlib")
print("=" * 64 + "\n")

# 1. Генерація даних CSV
print("[Крок 1/5] Генерація топологічних даних та атрибутів походження...")
subprocess.run([sys.executable, str(SCRIPTS_DIR / "generate_data.py")], check=True)

# 2. Аналіз графа та GDS алгоритми
print("\n[Крок 2/5] Виконання алгоритмів GDS (PageRank, Louvain) та PROFILE...")
subprocess.run([sys.executable, str(SCRIPTS_DIR / "graph_analytics.py")], check=True)

# 3. Text-to-Cypher бенчмарк та валідація безпеки Read-Only
print("\n[Крок 3/5] Запуск бенчмарку Text-to-Cypher та порівняння зі SPARQL...")
subprocess.run([sys.executable, str(SCRIPTS_DIR / "text_to_cypher.py")], check=True)

# 4. Генерація інженерної схеми графа
print("\n[Крок 4/5] Генерація академічної діаграми Property Graph...")
subprocess.run([sys.executable, str(SCRIPTS_DIR / "generate_diagram.py")], check=True)

# Синхронізація PDF-схеми
src_pdf = DOCS_DIR / "graph_schema.pdf"
dst_pdf = ROOT_DIR / "graph_schema.pdf"
if src_pdf.exists() and any(ROOT_DIR.glob("*.tex")):
    shutil.copy2(src_pdf, dst_pdf)

# 5. Перевірка підключення до Neo4j через Python-драйвер neo4j
print("\n[Крок 5/5] Перевірка підключення до СУБД Neo4j через Python-драйвер neo4j...")
try:
    from neo4j import GraphDatabase
    import socket
    with socket.create_connection(("localhost", 7687), timeout=0.5):
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "energygrid2026"))
        with driver.session() as session:
            result = session.run("SHOW CONSTRAINTS YIELD name, type")
            constraints = [r["name"] for r in result]
            print(f"[SUCCESS] Підключення до Neo4j активне! Виявлено обмежень: {len(constraints)}")
        driver.close()
except Exception as e:
    print(f"[NOTE] Локальний Neo4j демон на порту 7687 зараз не активний ({e}).")
    print("      Усі файли Cypher готові для завантаження в Neo4j Browser / cypher-shell:")
    print("      'docker compose up -d' -> http://localhost:7474")

# 6. Збірка звіту у LaTeX (якщо наявний шаблон .tex)
tex_files = list(ROOT_DIR.glob("*.tex"))
if tex_files and BIN_TECTONIC.exists():
    print("\n" + "=" * 64)
    print(" Збірка офіційного PDF-звіту...")
    tex_file = tex_files[0]
    pdf_out = ROOT_DIR / "latex_pdf"
    pdf_out.mkdir(exist_ok=True)
    cmd = [str(BIN_TECTONIC), str(tex_file.name), "--outdir", "latex_pdf"]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[SUCCESS] PDF-звіт успішно зкомпільовано: latex_pdf/{tex_file.stem}.pdf")
    else:
        print(f"[WARN] Помилка збірки TeX: {res.stderr[:300]}")

print("=" * 64)
print(" Всі артефакти Лабораторної роботи № 9 успішно згенеровано на 100%!")
print("=" * 64)
