"""
Головний скрипт автоматизованого запуску всіх етапів Лабораторної роботи №12
«OLAP-куб на основі таксономії»
Студент: Гріджак Олександр (група ФЕІ-43, ЛНУ ім. Івана Франка)
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def run_step(step_name: str, rel_path: str):
    print("\n" + "=" * 85)
    print(f"[RUNNER] Етап: {step_name} ({rel_path})")
    print("=" * 85)
    script_path = BASE_DIR / rel_path
    res = subprocess.run([sys.executable, str(script_path)], cwd=str(BASE_DIR))
    if res.returncode != 0:
        print(f"[ERROR] Помилка виконання {rel_path} (код {res.returncode})")
        sys.exit(res.returncode)


def main():
    print("=== АВТОМАТИЗОВАНИЙ ЗАПУСК ПОВНОГО ЦИКЛУ ЛАБОРАТОРНОЇ РОБОТИ №12 ===")
    run_step("Результат 1-2. Створення схеми DuckDB, ELT-завантаження та Data Quality", "etl/load.py")
    run_step("Результат 3. Виконання 8 OLAP-запитів та перевірка через pandas", "src/run_olap.py")
    run_step("Результат 4. Семантичний шар метрик та перевірка узгодженості", "src/semantic_layer.py")
    run_step("Результат 5 (а). Конвеєр Text-to-SQL з AST-захистом sqlglot", "src/text_to_sql.py")
    run_step("Результат 5 (б). Генерація аналітичної панелі з 4 візуалізацій", "dashboard/generate_dashboard.py")
    run_step("Генерація діаграми зірки та скріншотів-пруфів", "src/generate_proof_images.py")
    print("\n[COMPLETE] Усі 5 результатів ЛР 12 успішно виконано та верифіковано!")


if __name__ == "__main__":
    main()
