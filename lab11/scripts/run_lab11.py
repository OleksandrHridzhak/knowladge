"""
Головний скрипт автоматизованого запуску всіх етапів Лабораторної роботи №11
«Чат-бот на основі гібридного сховища (RAG + граф)»
Студент: Гріджак Олександр (група ФЕІ-43)
ЛНУ ім. Івана Франка, ФЕКТ, 2026
"""

import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import sys
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

def run_step(step_name: str, script_name: str):
    print("\n" + "=" * 75)
    print(f"[RUNNER] Запуск етапу: {step_name} ({script_name})")
    print("=" * 75)
    script_path = SRC_DIR / script_name
    cmd = [sys.executable, str(script_path)]
    env = os.environ.copy()
    env["HF_HUB_OFFLINE"] = "1"
    env["TRANSFORMERS_OFFLINE"] = "1"

    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        print(f"[ERROR] Помилка виконання {script_name} (код {result.returncode})")
        sys.exit(result.returncode)
    print(f"[SUCCESS] Етап {step_name} успішно виконано.")

def main():
    parser = argparse.ArgumentParser(description="Автоматизований запуск ЛР 11")
    parser.add_argument("--all", action="store_true", help="Виконати всі етапи послідовно")
    parser.add_argument("--rag", action="store_true", help="1. RAG-конвеєр з цитуванням (src/rag.py)")
    parser.add_argument("--graph", action="store_true", help="2. Підграф знань у контексті (src/graph_context.py)")
    parser.add_argument("--eval", action="store_true", help="4. Комплексне оцінювання (src/eval_rag.py)")
    parser.add_argument("--optimize", action="store_true", help="5. Оптимізація «До / Після» (src/optimize.py)")
    parser.add_argument("--proofs", action="store_true", help="Генерація скріншотів та графіків (src/generate_proof_images.py)")

    args = parser.parse_args()

    if len(sys.argv) == 1 or args.all:
        print("=== ЗАПУСК ПОВНОГО ЦИКЛУ ЛАБОРАТОРНОЇ РОБОТИ №11 ===")
        run_step("1. RAG-конвеєр з цитуванням", "rag.py")
        run_step("2. Підграф знань у контексті", "graph_context.py")
        run_step("4. Комплексне оцінювання", "eval_rag.py")
        run_step("5. Оптимізація «До / Після»", "optimize.py")
        run_step("Скріншоти та графіки", "generate_proof_images.py")
        print("\n[COMPLETE] Усі етапи ЛР 11 успішно завершено! Звіти та графіки збережено.")
    else:
        if args.rag:
            run_step("1. RAG-конвеєр з цитуванням", "rag.py")
        if args.graph:
            run_step("2. Підграф знань у контексті", "graph_context.py")
        if args.eval:
            run_step("4. Комплексне оцінювання", "eval_rag.py")
        if args.optimize:
            run_step("5. Оптимізація «До / Після»", "optimize.py")
        if args.proofs:
            run_step("Скріншоти та графіки", "generate_proof_images.py")

if __name__ == "__main__":
    main()

