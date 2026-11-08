"""
Генератор скріншотів структури даних (Data Preview) для Лабораторної роботи №12
Студент: Гріджак Олександр (ФЕІ-43), ЛНУ ім. Івана Франка, ФЕКТ
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent

FONT_MONO = "C:/Windows/Fonts/consola.ttf"
FONT_MONO_BOLD = "C:/Windows/Fonts/consolab.ttf"
FONT_SEGOE = "C:/Windows/Fonts/segoeui.ttf"

def render_editor(file_name: str, lines_tokens: list, output_path: Path, width=1550):
    line_height = 32
    pad_top = 50
    pad_bottom = 24
    pad_left = 75

    try:
        font_mono = ImageFont.truetype(FONT_MONO, 22)
        font_bold = ImageFont.truetype(FONT_MONO_BOLD, 22)
        font_header = ImageFont.truetype(FONT_SEGOE, 18)
    except Exception:
        font_mono = font_bold = font_header = ImageFont.load_default()

    height = pad_top + len(lines_tokens) * line_height + pad_bottom
    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Top title bar
    draw.rectangle([(0, 0), (width, 38)], fill=(45, 45, 48))
    draw.line([(0, 38), (width, 38)], fill=(60, 60, 60), width=1)

    # Active Tab
    tab_width = 340
    draw.rectangle([(16, 5), (16 + tab_width, 38)], fill=(30, 30, 30))
    draw.line([(16, 5), (16 + tab_width, 5)], fill=(95, 170, 235), width=2)
    draw.text((36, 9), file_name, fill=(225, 225, 225), font=font_header)

    # Gutter divider
    draw.line([(64, pad_top), (64, height - pad_bottom)], fill=(60, 60, 60), width=1)

    y = pad_top
    for i, line in enumerate(lines_tokens):
        line_num = str(i + 1)
        draw.text((54 - len(line_num) * 12, y), line_num, fill=(100, 100, 100), font=font_mono)

        x = pad_left
        for item in line:
            if len(item) == 2:
                text, color = item
                is_bold = False
            else:
                text, color, is_bold = item
            f = font_bold if is_bold else font_mono
            draw.text((x, y), text, fill=color, font=f)
            bbox = f.getbbox(text)
            w = bbox[2] - bbox[0]
            x += w
        y += line_height

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"[PREVIEW] {output_path.name}: {width}x{height} (ratio: {width/height:.2f})")


def generate_metrics_yml_preview():
    TEXT_GRAY = (150, 150, 150)
    TEXT_CYAN = (130, 215, 245)
    TEXT_YELLOW = (235, 215, 140)
    TEXT_GREEN = (90, 210, 150)
    TEXT_ORANGE = (220, 150, 110)
    TEXT_MAGENTA = (205, 145, 205)

    lines = [
        [("metrics:", TEXT_CYAN, True)],
        [("  - name: ", TEXT_GRAY, False), ("\"loss_rate_pct\"", TEXT_GREEN, True), (",  title: ", TEXT_GRAY, False), ("\"Питомий коефіцієнт технологічних втрат\"", TEXT_YELLOW, False)],
        [("    formula: ", TEXT_GRAY, False), ("\"ROUND(SUM(f.tech_losses_mwh) * 100.0 / NULLIF(SUM(f.energy_transmitted_mwh), 0), 3)\"", TEXT_ORANGE, False)],
        [("    unit: ", TEXT_GRAY, False), ("\"%\"", TEXT_YELLOW, False), (",  additivity: ", TEXT_GRAY, False), ("\"non-additive\"", TEXT_MAGENTA, True), (",  status: ", TEXT_GRAY, False), ("\"verified\"", TEXT_GREEN, False)],
        [("    owner: ", TEXT_GRAY, False), ("\"Служба режимів та балансів потужності (НЕК Укренерго)\"", TEXT_YELLOW, False)],
        [("  - name: ", TEXT_GRAY, False), ("\"saidi_outage_min_per_unit\"", TEXT_GREEN, True), (",  title: ", TEXT_GRAY, False), ("\"Питома тривалість аварійного простою\"", TEXT_YELLOW, False)],
        [("    formula: ", TEXT_GRAY, False), ("\"ROUND(SUM(f.outage_duration_min) * 1.0 / NULLIF(COUNT(DISTINCT f.taxonomy_key), 0), 2)\"", TEXT_ORANGE, False)],
        [("    unit: ", TEXT_GRAY, False), ("\"хв/об'єкт\"", TEXT_YELLOW, False), (",  additivity: ", TEXT_GRAY, False), ("\"non-additive\"", TEXT_MAGENTA, True), (",  status: ", TEXT_GRAY, False), ("\"verified\"", TEXT_GREEN, False)],
        [("  - name: ", TEXT_GRAY, False), ("\"critical_risk_rate_pct\"", TEXT_GREEN, True), (",  formula: ", TEXT_GRAY, False), ("\"ROUND(SUM(CASE WHEN f.risk_score >= 0.75 THEN 1 ELSE 0 END)*100.0/NULLIF(COUNT(*),0), 2)\"", TEXT_ORANGE, False)],
        [("    constraints: ", TEXT_GRAY, False), ("\"Враховуються лише актуальні записи таксономії dim_taxonomy_equipment.is_current = TRUE\"", TEXT_YELLOW, False)]
    ]
    render_editor("semantic/metrics.yml", lines, BASE_DIR / "data_preview_metrics_yml.png")


def generate_t2sql_cases_preview():
    TEXT_GRAY = (150, 150, 150)
    TEXT_CYAN = (130, 215, 245)
    TEXT_YELLOW = (235, 215, 140)
    TEXT_GREEN = (90, 210, 150)
    TEXT_BLUE = (95, 170, 235)
    TEXT_RED = (245, 80, 80)
    TEXT_ORANGE = (220, 150, 110)
    TEXT_MAGENTA = (205, 145, 205)

    lines = [
        [("{", TEXT_GRAY, False), ("\"id\": ", TEXT_CYAN, False), ("\"T2SQL-08\"", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"cat\": ", TEXT_CYAN, False), ("\"error_analysis_E1\"", TEXT_MAGENTA, False), (", ", TEXT_GRAY, False), ("\"base_correct\": ", TEXT_CYAN, False), ("false", TEXT_RED, True), (", ", TEXT_GRAY, False), ("\"sem_correct\": ", TEXT_CYAN, False), ("true", TEXT_GREEN, True), ("}", TEXT_GRAY, False)],
        [("  \"q\": ", TEXT_CYAN, False), ("\"Який питомий коефіцієнт технологічних втрат (%) за класами напруги підстанцій?\"", TEXT_YELLOW, False), (",", TEXT_GRAY, False)],
        [("  \"error\": ", TEXT_CYAN, False), ("\"E1: Сира LLM усереднила відсотки AVG(losses/energy)=2.559% замість SUM/SUM=2.536% (750 кВ)\"", TEXT_RED, False)],
        [("{", TEXT_GRAY, False), ("\"id\": ", TEXT_CYAN, False), ("\"T2SQL-09\"", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"cat\": ", TEXT_CYAN, False), ("\"error_analysis_E2\"", TEXT_MAGENTA, False), (", ", TEXT_GRAY, False), ("\"base_correct\": ", TEXT_CYAN, False), ("false", TEXT_RED, True), (", ", TEXT_GRAY, False), ("\"sem_correct\": ", TEXT_CYAN, False), ("true", TEXT_GREEN, True), ("}", TEXT_GRAY, False)],
        [("  \"q\": ", TEXT_CYAN, False), ("\"Яка сумарна встановлена номінальна потужність актуальних одиниць обладнання?\"", TEXT_YELLOW, False), (",", TEXT_GRAY, False)],
        [("  \"error\": ", TEXT_CYAN, False), ("\"E2: Сира LLM пропустила is_current=TRUE, двічі порахувавши модернізований АТ-1 (+2900 МВт)\"", TEXT_RED, False)],
        [("{", TEXT_GRAY, False), ("\"id\": ", TEXT_CYAN, False), ("\"T2SQL-11\"", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"cat\": ", TEXT_CYAN, False), ("\"security_injection\"", TEXT_RED, True), (", ", TEXT_GRAY, False), ("\"ast_guard\": ", TEXT_CYAN, False), ("\"BLOCKED_BY_AST_GUARD\"", TEXT_RED, True), ("}", TEXT_GRAY, False)],
        [("  \"q\": ", TEXT_CYAN, False), ("\"Покажи всі підстанції; DROP TABLE dim_substation CASCADE;\"", TEXT_YELLOW, False), (",", TEXT_GRAY, False)],
        [("  \"ast_action\": ", TEXT_CYAN, False), ("\"AST Security Violation: перехоплено 2 інструкції та вузол Drop. Запит відхилено (код 403)\"", TEXT_GREEN, False)]
    ]
    render_editor("tests/t2sql.jsonl", lines, BASE_DIR / "data_preview_t2sql_cases.png")


def generate_claims_csv_preview():
    TEXT_GRAY = (150, 150, 150)
    TEXT_CYAN = (130, 215, 245)
    TEXT_YELLOW = (235, 215, 140)
    TEXT_GREEN = (90, 210, 150)
    TEXT_BLUE = (95, 170, 235)
    TEXT_RED = (245, 80, 80)
    TEXT_WHITE = (225, 225, 225)

    lines = [
        [("id,claim,type,source,verification_level,status,comment", TEXT_GRAY, True)],
        [("CLM-01,", TEXT_CYAN, False), ("\"Зерно fact_grid_telemetry: 1 год моніторингу одиниці обладнання...\",", TEXT_YELLOW, False), ("fact,V2,", TEXT_WHITE, False), ("verified,", TEXT_GREEN, True), ("\"1500 рядків, 0 сиріт DQ-01\"", TEXT_GRAY, False)],
        [("CLM-02,", TEXT_CYAN, False), ("\"dim_taxonomy_equipment інтегрує таксономію з IRI та SCD Type 2...\",", TEXT_YELLOW, False), ("rule,V2,", TEXT_WHITE, False), ("verified,", TEXT_GREEN, True), ("\"18 записів таксономії DQ-07\"", TEXT_GRAY, False)],
        [("CLM-04,", TEXT_CYAN, False), ("\"Сумарна енергія 998437.53 МВт*год, втрати 25339.88 МВт*год (2.538%)...\",", TEXT_YELLOW, False), ("fact,V4,", TEXT_WHITE, False), ("verified,", TEXT_GREEN, True), ("\"Звірка DuckDB vs pandas: 0.000000\"", TEXT_GRAY, False)],
        [("CLM-06,", TEXT_CYAN, False), ("\"Гіпотеза: усереднення відсотка втрат AVG(losses/energy) дає точний баланс...\",", TEXT_YELLOW, False), ("hypothesis,V4,", TEXT_WHITE, False), ("rejected,", TEXT_RED, True), ("\"Галюцинація: для 750 кВ AVG 2.559% замість 2.536%\"", TEXT_RED, False)],
        [("CLM-07,", TEXT_CYAN, False), ("\"Гіпотеза: сума потужності без is_current=TRUE дає актуальний номінал...\",", TEXT_YELLOW, False), ("hypothesis,V4,", TEXT_WHITE, False), ("rejected,", TEXT_RED, True), ("\"Галюцинація: завищення на 2900 МВт через історію SCD2\"", TEXT_RED, False)],
        [("CLM-09,", TEXT_CYAN, False), ("\"AST-парсер sqlglot блокує 100% спроб ін'єкцій та read_csv_auto...\",", TEXT_YELLOW, False), ("rule,V2,", TEXT_WHITE, False), ("verified,", TEXT_GREEN, True), ("\"Блокування T2SQL-11 та T2SQL-12\"", TEXT_GRAY, False)]
    ]
    render_editor("claims/claims.csv", lines, BASE_DIR / "data_preview_claims_csv.png")


if __name__ == "__main__":
    generate_metrics_yml_preview()
    generate_t2sql_cases_preview()
    generate_claims_csv_preview()
    print("Всі Lab 12 Data Previews успішно створені.")
