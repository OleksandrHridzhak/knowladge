"""
Головний скрипт запуску всіх етапів Лабораторної роботи №10
«Векторне сховище та семантичний пошук»
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
    print("\n" + "=" * 70)
    print(f"[RUNNER] Запуск етапу: {step_name} ({script_name})")
    print("=" * 70)
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
    parser = argparse.ArgumentParser(description="Автоматизований запуск ЛР 10")
    parser.add_argument("--all", action="store_true", help="Виконати всі етапи послідовно")
    parser.add_argument("--corpus", action="store_true", help="1. Генерація корпусу та карток (src/generate_corpus.py)")
    parser.add_argument("--chunking", action="store_true", help="2. Порівняння стратегій чанкінгу (src/chunking.py)")
    parser.add_argument("--index", action="store_true", help="3. Векторний індекс FAISS та ембедінги (src/index.py)")
    parser.add_argument("--hybrid", action="store_true", help="4. Гібридний пошук BM25 + Dense + Rerank (src/hybrid.py)")
    parser.add_argument("--gold", action="store_true", help="5a. Генерація gold.jsonl (src/generate_gold.py)")
    parser.add_argument("--eval", action="store_true", help="5b. Комплексне оцінювання пошуку (src/eval.py)")
    
    args = parser.parse_args()
    
    # Якщо аргументи не задані, показуємо довідку або запускаємо перевірку
    if len(sys.argv) == 1 or args.all:
        print("=== ЗАПУСК ПОВНОГО ЦИКЛУ ЛАБОРАТОРНОЇ РОБОТИ №10 ===")
        run_step("1. Корпус та метадані", "generate_corpus.py")
        run_step("2. Порівняння чанкінгу", "chunking.py")
        run_step("3. Векторний індекс FAISS HNSW", "index.py")
        run_step("4. Гібридний пошук та Reranker", "hybrid.py")
        run_step("5a. Генерація Gold Standard", "generate_gold.py")
        run_step("5b. Оцінювання та аналіз метрик", "eval.py")
        print("\n[COMPLETE] Усі етапи ЛР 10 успішно завершено! Документація збережена у docs/.")
    else:
        if args.corpus:
            run_step("1. Корпус та метадані", "generate_corpus.py")
        if args.chunking:
            run_step("2. Порівняння чанкінгу", "chunking.py")
        if args.index:
            run_step("3. Векторний індекс FAISS HNSW", "index.py")
        if args.hybrid:
            run_step("4. Гібридний пошук та Reranker", "hybrid.py")
        if args.gold:
            run_step("5a. Генерація Gold Standard", "generate_gold.py")
        if args.eval:
            run_step("5b. Оцінювання та аналіз метрик", "eval.py")

if __name__ == "__main__":
    main()

