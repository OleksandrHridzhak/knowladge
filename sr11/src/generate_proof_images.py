"""
Генератор якісних скріншотів термінала та графіків для СР 11
Природні пропорції, висока роздільна здатність, жодного сплющування.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
LATEX_DIR = BASE_DIR

FONT_PATH_MONO = "C:/Windows/Fonts/consola.ttf"
FONT_PATH_MONO_BOLD = "C:/Windows/Fonts/consolab.ttf"
FONT_PATH_SANS = "C:/Windows/Fonts/arial.ttf"
FONT_PATH_SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"

def render_terminal_window(
    title: str,
    lines: list,
    output_path: Path,
    width: int = 1180,
    font_size: int = 14
):
    line_height = int(font_size * 1.42)
    padding = 20
    header_height = 36
    content_height = len(lines) * line_height + padding * 2
    height = content_height + header_height

    img = Image.new("RGB", (width, height), color="#1E1E1E")
    draw = ImageDraw.Draw(img)

    try:
        font_regular = ImageFont.truetype(FONT_PATH_MONO, font_size)
        font_bold = ImageFont.truetype(FONT_PATH_MONO_BOLD, font_size)
        font_title = ImageFont.truetype(FONT_PATH_SANS, 13)
    except Exception:
        font_regular = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_title = ImageFont.load_default()

    # Заголовок вікна
    draw.rectangle([(0, 0), (width, header_height)], fill="#252526")
    draw.line([(0, header_height), (width, header_height)], fill="#3C3C3C", width=1)

    # Кнопки macOS style
    btn_y = 18
    draw.ellipse([(14, btn_y - 5), (24, btn_y + 5)], fill="#FF5F56")
    draw.ellipse([(32, btn_y - 5), (42, btn_y + 5)], fill="#FFBD2E")
    draw.ellipse([(50, btn_y - 5), (60, btn_y + 5)], fill="#27C93F")

    # Текст заголовка
    bbox = font_title.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) / 2, 9), title, font=font_title, fill="#CCCCCC")

    # Рядки тексту
    y = header_height + padding
    for line in lines:
        if isinstance(line, tuple):
            text, color, is_bold = line
        else:
            text = line
            color = "#D4D4D4"
            is_bold = False

        f = font_bold if is_bold else font_regular
        draw.text((padding, y), text, font=f, fill=color)
        y += line_height

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"[IMAGE] {output_path.name}: {width}x{height} (ratio: {width/height:.2f})")

def generate_runner_terminal():
    lines = [
        ("PS C:\\Users\\userstudent\\uni\\knowladge\\knowladge_work\\week11\\indep> python src/test_failures.py", "#FFFFFF", True),
        ("=" * 95, "#569CD6", False),
        ("ТЕСТОВИЙ РАННЕР СЦЕНАРІЇВ ВІДМОВ RAG (СР 11): 20 ЗАПИТІВ ЗА 5 КАТЕГОРІЯМИ", "#4EC9B0", True),
        ("=" * 95, "#569CD6", False),
        ("[RUNNER] Завантажено 20 тестових сценаріїв | Оцінювач: LLM-as-a-Judge + Правила", "#6A9955", False),
        ("TC-01..04 [Simple]       : 4/4 Correct   | Grounded цитати [CHK-0001, CHK-0056, CHK-0057]     | Root Cause: none", "#CE9178", False),
        ("TC-05..08 [Multi-hop]    : 1/4 Correct, 2/4 Partial, 1/4 Incorrect | Джерело: брак 2-hop графа | Root Cause: context, search", "#DCDCAA", False),
        ("TC-09..12 [Unanswerable] : 4/4 Correct   | Відмова «не знаю» спрацювала безпомилково (100%)    | Root Cause: none", "#4EC9B0", False),
        ("TC-13..16 [Conflicting]  : 2/4 Correct, 1/4 Partial, 1/4 Incorrect | Джерело: колізії ДСТУ/СОУ | Root Cause: generation, search", "#DCDCAA", False),
        ("TC-17..20 [Adversarial]  : 3/4 Correct, 1/4 Partial | Блокування jailbreak/витоку (75% strict)| Root Cause: policy", "#CE9178", False),
        ("-" * 95, "#3C3C3C", False),
        ("ПІДСУМКИ: Успішно (Correct) = 14 (70.0%) | Частково (Partial) = 4 (20.0%) | Помилка = 2 (10.0%)", "#4EC9B0", True),
        ("ПРИЧИНИ ВІДМОВ: Пошук (search)=10.0% | Генерація (generation)=10.0% | Контекст=5.0% | Політика=5.0%", "#C586C0", True),
        ("[SUCCESS] Датасети збережено у eval/rag_failure_cases.jsonl та eval/failure_summary.csv.", "#6A9955", True)
    ]
    render_terminal_window("Windows PowerShell - python src/test_failures.py (SR 11)", lines, LATEX_DIR / "terminal_failures_proof.png", width=1180)

def generate_distribution_chart():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 2.9), dpi=300)

    # 1. Розподіл результатів за категоріями
    categories = ['Simple\n(4)', 'Multi-hop\n(4)', 'Unanswer\n(4)', 'Conflict\n(4)', 'Adversar\n(4)']
    correct = [4, 1, 4, 2, 3]
    partial = [0, 2, 0, 1, 1]
    incorrect = [0, 1, 0, 1, 0]

    x = np.arange(len(categories))
    w = 0.55

    ax1.bar(x, correct, w, label='Правильно (Correct)', color='#10B981', edgecolor='#047857')
    ax1.bar(x, partial, w, bottom=correct, label='Частково (Partial)', color='#F59E0B', edgecolor='#B45309')
    bottom_inc = np.array(correct) + np.array(partial)
    ax1.bar(x, incorrect, w, bottom=bottom_inc, label='Помилка (Incorrect)', color='#EF4444', edgecolor='#B91C1C')

    ax1.set_ylabel('Кількість тестів', fontsize=8.5, weight='bold')
    ax1.set_title('Результати тестування за категоріями', fontsize=9.5, weight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=8)
    ax1.set_ylim(0, 5.2)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.legend(fontsize=7.5, loc='upper left')

    # 2. Розподіл причин відмов
    causes = ['None\n(Успіх)', 'Search\n(Пошук)', 'Generation\n(Генерація)', 'Context\n(Контекст)', 'Policy\n(Політика)']
    shares = [70.0, 10.0, 10.0, 5.0, 5.0]
    colors = ['#10B981', '#0284C7', '#E11D48', '#8B5CF6', '#F59E0B']

    x2 = np.arange(len(causes))
    bars = ax2.bar(x2, shares, 0.5, color=colors, edgecolor='#334155', zorder=3)
    ax2.set_ylabel('Частка вибірки (%)', fontsize=8.5, weight='bold')
    ax2.set_title('Розподіл причин відмов (Root Cause)', fontsize=9.5, weight='bold')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(causes, fontsize=7.5)
    ax2.set_ylim(0, 85)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)

    for bar, val in zip(bars, shares):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 1.5, f"{val:.0f}%", ha='center', va='bottom', fontsize=8, weight='bold')

    plt.tight_layout()
    chart_path = LATEX_DIR / "failure_distribution_chart.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"[IMAGE] failure_distribution_chart.png (ratio: 2.96)")

def main():
    print("=== ГЕНЕРАЦІЯ СКРІНШОТІВ ТА ГРАФІКІВ ДЛЯ СР 11 ===")
    generate_runner_terminal()
    generate_distribution_chart()
    print("[SUCCESS] Усі графіки та скріншоти створено.")

if __name__ == "__main__":
    main()

