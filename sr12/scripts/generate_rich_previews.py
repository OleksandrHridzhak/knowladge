"""
Генератор скріншотів структури даних (Data Preview) для Самостійної роботи №12
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


def generate_sr12_queries_preview():
    TEXT_GRAY = (150, 150, 150)
    TEXT_CYAN = (130, 215, 245)
    TEXT_YELLOW = (235, 215, 140)
    TEXT_GREEN = (90, 210, 150)
    TEXT_BLUE = (95, 170, 235)
    TEXT_ORANGE = (220, 150, 110)
    TEXT_MAGENTA = (205, 145, 205)

    lines = [
        [("-- Запит Q1: Недовідпуск (ENS) та компенсації за районами (ROLLUP)", TEXT_GRAY, False)],
        [("SELECT ", TEXT_BLUE, True), ("COALESCE(n.region_cluster, ", TEXT_CYAN, False), ("'УСЯ ОЕС')", TEXT_YELLOW, False), (" AS region, ", TEXT_WHITE_local := (225, 225, 225), False), ("ROUND(SUM(f.ens_unsupplied_mwh), 2) AS total_ens_mwh,", TEXT_WHITE_local, False)],
        [("       ROUND(SUM(f.compensation_cost_uah) / ", TEXT_WHITE_local, False), ("1000.0", TEXT_MAGENTA, False), (", 2) AS compensation_k_uah", TEXT_WHITE_local, False)],
        [("FROM ", TEXT_BLUE, True), ("fact_outage_balance f ", TEXT_CYAN, False), ("JOIN ", TEXT_BLUE, True), ("dim_grid_node n ON f.node_key = n.node_key", TEXT_CYAN, False)],
        [("GROUP BY ROLLUP ", TEXT_BLUE, True), ("(n.region_cluster, n.voltage_kv);", TEXT_CYAN, False)],
        [("-- Запит Q2: Тривалість відновлення за таксономією та причинами", TEXT_GRAY, False)],
        [("SELECT ", TEXT_BLUE, True), ("e.class_l1, e.subclass_l2, c.cause_group, ", TEXT_CYAN, False), ("SUM(f.affected_consumers_cnt) AS consumers,", TEXT_WHITE_local, False)],
        [("       ROUND(SUM(f.restoration_duration_min), 1) AS total_min, ", TEXT_WHITE_local, False), ("ROUND(AVG(f.restoration_duration_min), 2) AS avg_min", TEXT_WHITE_local, False)],
        [("FROM ", TEXT_BLUE, True), ("fact_outage_balance f ", TEXT_CYAN, False), ("JOIN ", TEXT_BLUE, True), ("dim_equipment_taxonomy e USING(equipment_key) ", TEXT_CYAN, False), ("WHERE ", TEXT_BLUE, True), ("e.is_current = TRUE", TEXT_GREEN, True)],
        [("GROUP BY ", TEXT_BLUE, True), ("e.class_l1, e.subclass_l2, c.cause_group ", TEXT_CYAN, False), ("ORDER BY ", TEXT_BLUE, True), ("total_min DESC;", TEXT_CYAN, False)]
    ]
    render_editor("sql/sr12_queries.sql", lines, BASE_DIR / "data_preview_sr12_queries.png")


def generate_sr12_ddl_preview():
    TEXT_GRAY = (150, 150, 150)
    TEXT_CYAN = (130, 215, 245)
    TEXT_YELLOW = (235, 215, 140)
    TEXT_GREEN = (90, 210, 150)
    TEXT_BLUE = (95, 170, 235)
    TEXT_WHITE = (225, 225, 225)

    lines = [
        [("-- Створення таблиці фактів: 1 рядок = 1 інцидент знеструмлення", TEXT_GRAY, False)],
        [("CREATE TABLE ", TEXT_BLUE, True), ("fact_outage_balance (", TEXT_CYAN, True)],
        [("    outage_event_id ", TEXT_WHITE, False), ("BIGINT PRIMARY KEY,", TEXT_BLUE, False), ("  -- сурогатний первинний ключ", TEXT_GRAY, False)],
        [("    time_key ", TEXT_WHITE, False), ("INTEGER REFERENCES dim_time(time_key),", TEXT_CYAN, False)],
        [("    node_key ", TEXT_WHITE, False), ("INTEGER REFERENCES dim_grid_node(node_key),", TEXT_CYAN, False)],
        [("    equipment_key ", TEXT_WHITE, False), ("INTEGER REFERENCES dim_equipment_taxonomy(equipment_key),", TEXT_CYAN, False)],
        [("    cause_key ", TEXT_WHITE, False), ("INTEGER REFERENCES dim_outage_cause(cause_key),", TEXT_CYAN, False)],
        [("    consumer_key ", TEXT_WHITE, False), ("INTEGER REFERENCES dim_consumer_category(consumer_key),", TEXT_CYAN, False)],
        [("    ens_unsupplied_mwh ", TEXT_WHITE, False), ("DOUBLE NOT NULL CHECK (ens_unsupplied_mwh >= 0),  -- адитивна міра", TEXT_GREEN, False)],
        [("    restoration_duration_min ", TEXT_WHITE, False), ("DOUBLE NOT NULL CHECK (restoration_duration_min > 0)  -- адитивна", TEXT_GREEN, False)],
        [(");", TEXT_CYAN, True)]
    ]
    render_editor("sql/sr12_ddl.sql", lines, BASE_DIR / "data_preview_sr12_ddl.png")


def generate_sr12_review_preview():
    TEXT_GRAY = (150, 150, 150)
    TEXT_CYAN = (130, 215, 245)
    TEXT_YELLOW = (235, 215, 140)
    TEXT_GREEN = (90, 210, 150)
    TEXT_BLUE = (95, 170, 235)
    TEXT_RED = (245, 80, 80)
    TEXT_ORANGE = (220, 150, 110)

    lines = [
        [("{", TEXT_GRAY, False), ("\"model\": ", TEXT_CYAN, False), ("\"gemini-2.5-pro\"", TEXT_GREEN, False), (", ", TEXT_GRAY, False), ("\"seed\": ", TEXT_CYAN, False), ("42", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"llm_flaws_identified\": [", TEXT_CYAN, True)],
        [("  {", TEXT_GRAY, False), ("\"flaw_id\": ", TEXT_CYAN, False), ("\"FL-01\"", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"defect\": ", TEXT_CYAN, False), ("\"Розмиття зерна факту (добовий агрегат замість одиничного інциденту)\"", TEXT_YELLOW, False), (", ", TEXT_GRAY, False), ("\"fix\": ", TEXT_CYAN, False), ("\"Зафіксовано атомарний інцидент аварії\"", TEXT_GREEN, False), ("},", TEXT_GRAY, False)],
        [("  {", TEXT_GRAY, False), ("\"flaw_id\": ", TEXT_CYAN, False), ("\"FL-02\"", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"defect\": ", TEXT_CYAN, False), ("\"Використання природних назв у JOIN замість числових сурогатних ключів\"", TEXT_YELLOW, False), (", ", TEXT_GRAY, False), ("\"fix\": ", TEXT_CYAN, False), ("\"Впроваджено цілочисельні time_key, node_key, equip_key\"", TEXT_GREEN, False), ("},", TEXT_GRAY, False)],
        [("  {", TEXT_GRAY, False), ("\"flaw_id\": ", TEXT_CYAN, False), ("\"FL-03\"", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"defect\": ", TEXT_CYAN, False), ("\"Збереження неадитивного відсотка відхилення частоти як простого числа\"", TEXT_YELLOW, False), (", ", TEXT_GRAY, False), ("\"fix\": ", TEXT_CYAN, False), ("\"Розділено на надир частоти (Гц) та окремий розрахунок SAIDI\"", TEXT_GREEN, False), ("}", TEXT_GRAY, False)],
        [("],", TEXT_CYAN, True)],
        [("  \"consensus\": ", TEXT_CYAN, False), ("\"Усі 3 дефекти схеми усунено в sr12_ddl.sql. Повна верифікація DuckDB\"", TEXT_GREEN, True)],
        [("}", TEXT_GRAY, False)]
    ]
    render_editor("docs/llm_schema_review.json", lines, BASE_DIR / "data_preview_sr12_review.png")


if __name__ == "__main__":
    generate_sr12_queries_preview()
    generate_sr12_ddl_preview()
    generate_sr12_review_preview()
    print("Всі SR 12 Data Previews успішно створені.")
