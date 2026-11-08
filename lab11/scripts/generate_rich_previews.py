"""
Генерація додаткових скріншотів структури даних (Data Preview) для Лабораторної роботи №11
Студент: Гріджак Олександр (ФЕІ-43)
"""

import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

BG_COLOR = (30, 30, 30)
BAR_COLOR = (45, 45, 48)
TAB_ACTIVE_COLOR = (30, 30, 30)
BORDER_COLOR = (60, 60, 60)
LINE_NUM_COLOR = (100, 100, 100)

TEXT_WHITE = (225, 225, 225)
TEXT_GRAY = (150, 150, 150)
TEXT_GREEN = (90, 210, 150)
TEXT_BLUE = (95, 170, 235)
TEXT_YELLOW = (235, 215, 140)
TEXT_ORANGE = (220, 150, 110)
TEXT_RED = (245, 80, 80)
TEXT_CYAN = (130, 215, 245)
TEXT_MAGENTA = (205, 145, 205)

try:
    FONT = ImageFont.truetype("C:/WINDOWS/fonts/consola.ttf", 22)
    FONT_BOLD = ImageFont.truetype("C:/WINDOWS/fonts/consolab.ttf", 22)
    FONT_HEADER = ImageFont.truetype("C:/WINDOWS/fonts/segoeui.ttf", 18)
except Exception:
    FONT = ImageFont.load_default()
    FONT_BOLD = FONT
    FONT_HEADER = FONT

def render_editor(file_name: str, lines_tokens: list, output_path: str, width=1550):
    line_height = 32
    pad_top = 50
    pad_bottom = 24
    pad_left = 75
    
    height = pad_top + len(lines_tokens) * line_height + pad_bottom
    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([(0, 0), (width, 38)], fill=BAR_COLOR)
    draw.line([(0, 38), (width, 38)], fill=BORDER_COLOR, width=1)
    
    tab_width = 320
    draw.rectangle([(16, 5), (16 + tab_width, 38)], fill=TAB_ACTIVE_COLOR)
    draw.line([(16, 5), (16 + tab_width, 5)], fill=TEXT_BLUE, width=2)
    draw.text((36, 9), file_name, fill=TEXT_WHITE, font=FONT_HEADER)
    
    draw.line([(64, pad_top), (64, height - pad_bottom)], fill=BORDER_COLOR, width=1)
    
    y = pad_top
    for i, line in enumerate(lines_tokens):
        line_num = str(i + 1)
        draw.text((54 - len(line_num) * 12, y), line_num, fill=LINE_NUM_COLOR, font=FONT)
        
        x = pad_left
        for item in line:
            if len(item) == 2:
                text, color = item
                is_bold = False
            else:
                text, color, is_bold = item
            f = FONT_BOLD if is_bold else FONT
            draw.text((x, y), text, fill=color, font=f)
            bbox = f.getbbox(text)
            w = bbox[2] - bbox[0]
            x += w
        y += line_height
        
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"[PREVIEW] Збережено: {output_path}")

def generate_queries_jsonl_preview():
    lines = [
        [("{", TEXT_GRAY, False), ("\"query_id\": ", TEXT_CYAN, False), ("\"RQ-01\"", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"role\": ", TEXT_CYAN, False), ("\"engineer\"", TEXT_GREEN, False), (", ", TEXT_GRAY, False), ("\"latency_ms\": ", TEXT_CYAN, False), ("42.15", TEXT_MAGENTA, False), ("}", TEXT_GRAY, False)],
        [("  \"query\": ", TEXT_CYAN, False), ("\"Які параметри та час дії захисту SEL-421 на ПЛ 750 кВ?\"", TEXT_YELLOW, False), (",", TEXT_GRAY, False)],
        [("  \"citations\": [", TEXT_CYAN, False), ("\"CHK-0057\"", TEXT_ORANGE, False), ("],  ", TEXT_GRAY, False), ("\"citations_valid\": ", TEXT_CYAN, False), ("true", TEXT_BLUE, True), (",  ", TEXT_GRAY, False), ("\"tokens\": ", TEXT_CYAN, False), ("412", TEXT_MAGENTA, False)],
        [("  \"answer\": ", TEXT_CYAN, False), ("\"Термінал SEL-421 реалізує 5 зон дистанційного захисту... [CHK-0057]\"", TEXT_WHITE, False)],
        [("{", TEXT_GRAY, False), ("\"query_id\": ", TEXT_CYAN, False), ("\"RQ-03\"", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"role\": ", TEXT_CYAN, False), ("\"analyst\"", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"rbac_blocked\": ", TEXT_CYAN, False), ("true", TEXT_RED, True), ("}", TEXT_GRAY, False)],
        [("  \"query\": ", TEXT_CYAN, False), ("\"Які закриті уставки дифзахисту шин підстанції 750 кВ?\"", TEXT_YELLOW, False), (",", TEXT_GRAY, False)],
        [("  \"policy_action\": ", TEXT_CYAN, False), ("\"FORBIDDEN_403\"", TEXT_RED, True), (",  ", TEXT_GRAY, False), ("\"reason\": ", TEXT_CYAN, False), ("\"Sensitivity 'restricted' requires engineer role\"", TEXT_GRAY, False)],
        [("{", TEXT_GRAY, False), ("\"query_id\": ", TEXT_CYAN, False), ("\"RQ-04\"", TEXT_ORANGE, False), (", ", TEXT_GRAY, False), ("\"abstention\": ", TEXT_CYAN, False), ("\"TRIGGERED_IDK\"", TEXT_CYAN, True), (", ", TEXT_GRAY, False), ("\"max_sim\": ", TEXT_CYAN, False), ("0.24", TEXT_MAGENTA, False), ("}", TEXT_GRAY, False)],
        [("  \"query\": ", TEXT_CYAN, False), ("\"Які сорти винограду найкраще підходять для білого вина?\"", TEXT_YELLOW, False), (",", TEXT_GRAY, False)],
        [("  \"answer\": ", TEXT_CYAN, False), ("\"Я не маю достовірної інформації у наданих регламентах ОЕС України.\"", TEXT_WHITE, False)]
    ]
    render_editor("llm_log/rag_queries.jsonl", lines, str(BASE_DIR / "data_preview_queries_jsonl.png"))

def generate_claims_csv_preview():
    lines = [
        [("id,statement,type,source,verification_level,status,comment", TEXT_GRAY, True)],
        [("C01,", TEXT_CYAN, False), ("\"Генеруючі одиниці типу D (від 75 МВт)...\",", TEXT_YELLOW, False), ("правило,DOC-01,", TEXT_WHITE, False), ("V1,", TEXT_BLUE, True), ("verified,", TEXT_GREEN, True), ("\"Кодекс системи передачі\"", TEXT_GRAY, False)],
        [("C04,", TEXT_CYAN, False), ("\"SEL-421 транслює телеметрію IEC 60870-5-104...\",", TEXT_YELLOW, False), ("факт,DOC-07,", TEXT_WHITE, False), ("V4,", TEXT_BLUE, True), ("verified,", TEXT_GREEN, True), ("\"Сервер SCADA Укренерго\"", TEXT_GRAY, False)],
        [("C07,", TEXT_CYAN, False), ("\"ПС Західноукраїнська зв'язана лініями 750 кВ...\",", TEXT_YELLOW, False), ("факт,Graph,", TEXT_WHITE, False), ("V1,", TEXT_BLUE, True), ("verified,", TEXT_GREEN, True), ("\"Топологічний граф ОЕС\"", TEXT_GRAY, False)],
        [("C09,", TEXT_CYAN, False), ("\"Запити ролі analyst обмежені відкритими даними...\",", TEXT_YELLOW, False), ("правило,API,", TEXT_WHITE, False), ("V3,", TEXT_BLUE, True), ("verified,", TEXT_GREEN, True), ("\"RBAC pre-filtering 403\"", TEXT_GRAY, False)],
        [("C11,", TEXT_CYAN, False), ("\"SEL-421 автоматично синхронізує розімкнені енергосистеми...\",", TEXT_YELLOW, False), ("гіпотеза,LLM,", TEXT_WHITE, False), ("V1,", TEXT_BLUE, True), ("rejected,", TEXT_RED, True), ("\"Галюцинація: потрібен автосинхронізатор\"", TEXT_RED, False)],
        [("C12,", TEXT_CYAN, False), ("\"Граничний струм ПЛ 750 кВ може досягати 15000 А...\",", TEXT_YELLOW, False), ("факт,LLM,", TEXT_WHITE, False), ("V3,", TEXT_BLUE, True), ("rejected,", TEXT_RED, True), ("\"Галюцинація: ліміт 2000-2400 А за нагрівом\"", TEXT_RED, False)]
    ]
    render_editor("claims/claims.csv", lines, str(BASE_DIR / "data_preview_claims_csv.png"))

def generate_subgraph_context_preview():
    lines = [
        [("=== ЛІНЕАРИЗОВАНИЙ КОНТЕКСТ ПІДГРАФА (GraphRAG Context) ===", TEXT_CYAN, True)],
        [("[NODE-SS_Zakhidna] (Substation, 750/330 kV, Region: Western Grid)", TEXT_YELLOW, True)],
        [("  ==[CONNECTS_TO]==> [NODE-LINE_750_ZAKH_VIN] (Line 750 kV, Length: 345 km)", TEXT_WHITE, False)],
        [("  ==[SUPPLIES_POWER_TO]==> [NODE-SS_Vinnytska] (Substation, 750/330 kV)", TEXT_WHITE, False)],
        [("  ==[PROTECTED_BY]==> [NODE-RP_SEL421_Zakhidna] (Relay Protection Terminal)", TEXT_WHITE, False)],
        [("[NODE-RP_SEL421_Zakhidna] (Protection Terminal, Firmware: R104, Vendor: SEL)", TEXT_YELLOW, True)],
        [("  ==[COMMUNICATES_VIA]==> [NODE-SCADA_Central_NPC] (Protocol: IEC 60870-5-104)", TEXT_GREEN, False)],
        [("  ==[CONTROLS_BREAKER]==> [NODE-Q1_750kV_Zakhidna] (SF6 Breaker 750 kV)", TEXT_GREEN, False)],
        [("[GRAPH METRICS] Nodes retrieved: 6, Critical Edges: 8, Context tokens: +367", TEXT_MAGENTA, True)]
    ]
    render_editor("docs/subgraph_context_preview.txt", lines, str(BASE_DIR / "data_preview_subgraph.png"))

if __name__ == "__main__":
    generate_queries_jsonl_preview()
    generate_claims_csv_preview()
    generate_subgraph_context_preview()
    print("Всі Data Preview успішно згенеровано.")

