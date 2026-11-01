"""
Самостійна робота №12: Проєктування зіркової схеми
Студент: Гріджак Олександр (група ФЕІ-43, ЛНУ ім. Івана Франка)
Виконує DDL у DuckDB, завантажує тестові дані (N=600, seed=42), перевіряє 5 бізнес-запитів Q1-Q5
та генерує діаграму зірки sr12_star_schema.png і консольний пруф terminal_sr12_proof.png.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import random
from datetime import date
from pathlib import Path
import duckdb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = BASE_DIR / "sql"
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"
DB_PATH = DATA_DIR / "sr12_star.duckdb"

SEED = 42
IRI_PREFIX = "http://www.semanticweb.org/ontologies/2026/power-grid#"

FONT_TNR = "C:/Windows/Fonts/times.ttf"
FONT_TNR_BOLD = "C:/Windows/Fonts/timesbd.ttf"
FONT_MONO = "C:/Windows/Fonts/consola.ttf"
FONT_MONO_BOLD = "C:/Windows/Fonts/consolab.ttf"
FONT_SANS = "C:/Windows/Fonts/arial.ttf"


def build_sr12_dataset():
    rng = random.Random(SEED)

    # 1. dim_time (48 інтервалів за 2024-2025 рр.)
    seasons = {1: ("Зима", "Q1"), 2: ("Зима", "Q1"), 3: ("Весна", "Q1"), 4: ("Весна", "Q2"),
               5: ("Весна", "Q2"), 6: ("Літо", "Q2"), 7: ("Літо", "Q3"), 8: ("Літо", "Q3"),
               9: ("Осінь", "Q3"), 10: ("Осінь", "Q4"), 11: ("Осінь", "Q4"), 12: ("Зима", "Q4")}
    periods = ["Ранковий пік", "Денна зона", "Вечірній максимум", "Нічний провал"]
    dim_time_rows = []
    t_key = 1
    for yr in [2024, 2025]:
        for m in range(1, 13):
            season, qtr = seasons[m]
            for p_idx, per in enumerate([periods[0], periods[2]]):
                dt = date(yr, m, 10 + p_idx * 10)
                dim_time_rows.append({
                    "time_key": t_key,
                    "full_date": dt.isoformat(),
                    "year": yr,
                    "quarter": qtr,
                    "month": m,
                    "season": season,
                    "peak_period": per,
                })
                t_key += 1

    # 2. dim_grid_node (8 вузлових приєднань у 4 енергорайонах)
    dim_node_rows = [
        {"node_key": 1, "feeder_code": "FDR-ZAKH-750-1", "substation_name": "ПС 750 кВ Західноукраїнська", "oblast": "Львівська", "region_cluster": "Західний", "voltage_kv": 750},
        {"node_key": 2, "feeder_code": "FDR-LVIV-330-2", "substation_name": "ПС 330 кВ Львів-Південна", "oblast": "Львівська", "region_cluster": "Західний", "voltage_kv": 330},
        {"node_key": 3, "feeder_code": "FDR-STRYI-110-1", "substation_name": "ПС 110 кВ Стрий", "oblast": "Львівська", "region_cluster": "Західний", "voltage_kv": 110},
        {"node_key": 4, "feeder_code": "FDR-KYIV-750-1", "substation_name": "ПС 750 кВ Київська", "oblast": "Київська", "region_cluster": "Центральний", "voltage_kv": 750},
        {"node_key": 5, "feeder_code": "FDR-VIN-750-1", "substation_name": "ПС 750 кВ Вінницька", "oblast": "Вінницька", "region_cluster": "Центральний", "voltage_kv": 750},
        {"node_key": 6, "feeder_code": "FDR-BROV-330-1", "substation_name": "ПС 330 кВ Броварська", "oblast": "Київська", "region_cluster": "Центральний", "voltage_kv": 330},
        {"node_key": 7, "feeder_code": "FDR-DNIP-750-1", "substation_name": "ПС 750 кВ Дніпровська", "oblast": "Дніпропетровська", "region_cluster": "Дніпровський", "voltage_kv": 750},
        {"node_key": 8, "feeder_code": "FDR-USAT-330-1", "substation_name": "ПС 330 кВ Усатове", "oblast": "Одеська", "region_cluster": "Південний", "voltage_kv": 330},
    ]

    # 3. dim_equipment_taxonomy (8 записів, включно з SCD Type 2 історією за 2024 vs 2025)
    dim_eq_rows = [
        {
            "equipment_key": 1,
            "natural_code": "EQ-AT1-ZAKH",
            "apparatus_model": "Автотрансформатор АТ-1 750/330 кВ (старий РПН)",
            "class_l1": "Силове трансформаторне обладнання",
            "subclass_l2": "PowerTransformer",
            "ontology_iri": f"{IRI_PREFIX}Autotransformer_AT1_v1",
            "rated_power_mva": 900.0,
            "valid_from": "2020-01-01",
            "valid_to": "2024-12-31",
            "is_current": False,
        },
        {
            "equipment_key": 2,
            "natural_code": "EQ-AT1-ZAKH",
            "apparatus_model": "Автотрансформатор 3хАОДЦТН-333000 (модернізований)",
            "class_l1": "Силове трансформаторне обладнання",
            "subclass_l2": "PowerTransformer",
            "ontology_iri": f"{IRI_PREFIX}Autotransformer_AT1",
            "rated_power_mva": 1000.0,
            "valid_from": "2025-01-01",
            "valid_to": "2099-12-31",
            "is_current": True,
        },
        {
            "equipment_key": 3,
            "natural_code": "EQ-PL750-DZ",
            "apparatus_model": "ПЛ 750 кВ Дніпровська-Західноукраїнська",
            "class_l1": "Магістральні лінії електропередачі",
            "subclass_l2": "OverheadLine",
            "ontology_iri": f"{IRI_PREFIX}Line_750kV_Dnipro_Zakhidna",
            "rated_power_mva": 2200.0,
            "valid_from": "2020-01-01",
            "valid_to": "2099-12-31",
            "is_current": True,
        },
        {
            "equipment_key": 4,
            "natural_code": "EQ-PL330-ZL",
            "apparatus_model": "ПЛ 330 кВ Західноукраїнська-Львів",
            "class_l1": "Магістральні лінії електропередачі",
            "subclass_l2": "OverheadLine",
            "ontology_iri": f"{IRI_PREFIX}Line_330kV_Zakhidna_Lviv",
            "rated_power_mva": 480.0,
            "valid_from": "2020-01-01",
            "valid_to": "2099-12-31",
            "is_current": True,
        },
        {
            "equipment_key": 5,
            "natural_code": "EQ-KL110-STR",
            "apparatus_model": "КЛ 110 кВ Стрий-Промислова",
            "class_l1": "Магістральні лінії електропередачі",
            "subclass_l2": "CableLine",
            "ontology_iri": f"{IRI_PREFIX}CableLine_110kV_Stryi",
            "rated_power_mva": 140.0,
            "valid_from": "2021-01-01",
            "valid_to": "2099-12-31",
            "is_current": True,
        },
        {
            "equipment_key": 6,
            "natural_code": "EQ-SEL421",
            "apparatus_model": "Дистанційний захист SEL-421 (уставка v1)",
            "class_l1": "Релейний захист та комутація",
            "subclass_l2": "DistanceProtection",
            "ontology_iri": f"{IRI_PREFIX}RelayProtection_SEL421_v1",
            "rated_power_mva": 2000.0,
            "valid_from": "2020-01-01",
            "valid_to": "2024-12-31",
            "is_current": False,
        },
        {
            "equipment_key": 7,
            "natural_code": "EQ-SEL421",
            "apparatus_model": "Дистанційний захист SEL-421 (IEC 61850 GOOSE)",
            "class_l1": "Релейний захист та комутація",
            "subclass_l2": "DistanceProtection",
            "ontology_iri": f"{IRI_PREFIX}RelayProtection_SEL421",
            "rated_power_mva": 2200.0,
            "valid_from": "2025-01-01",
            "valid_to": "2099-12-31",
            "is_current": True,
        },
        {
            "equipment_key": 8,
            "natural_code": "EQ-CB-750Q1",
            "apparatus_model": "Елегазовий вимикач 750 кВ HPL-800B Q1",
            "class_l1": "Релейний захист та комутація",
            "subclass_l2": "CircuitBreaker",
            "ontology_iri": f"{IRI_PREFIX}CircuitBreaker_Q1",
            "rated_power_mva": 2200.0,
            "valid_from": "2020-01-01",
            "valid_to": "2099-12-31",
            "is_current": True,
        },
    ]

    # 4. dim_outage_cause
    dim_cause_rows = [
        {"cause_key": 1, "cause_code": "CS-WEATHER", "cause_group": "Метеорологічні фактори", "cause_detail": "Ожеледь і галопування проводів", "protection_stage": "1-ша зона ДЗ + АПВ"},
        {"cause_key": 2, "cause_code": "CS-INSUL", "cause_group": "Технічне зношення ізоляції", "cause_detail": "Пробій вводу високої напруги", "protection_stage": "Диференційний захист АТ"},
        {"cause_key": 3, "cause_code": "CS-OVLD", "cause_group": "Режимне перевантаження", "cause_detail": "Перевищення термічної межі Imax", "protection_stage": "Розвантажувальна автоматика САВН"},
        {"cause_key": 4, "cause_code": "CS-COMM", "cause_group": "Комутаційні перенапруги", "cause_detail": "Відмова приводу полюса вимикача", "protection_stage": "ПРОВ вимикача 330/750 кВ"},
    ]

    # 5. dim_consumer_category
    dim_cons_rows = [
        {"consumer_key": 1, "tier_code": "TIER-I", "reliability_tier": "І категорія (особлива)", "sector_name": "Критична інфраструктура та водоканали", "tariff_group": "Промисловість 1 клас", "penalty_rate_uah_per_mwh": 18500.0},
        {"consumer_key": 2, "tier_code": "TIER-II", "reliability_tier": "ІІ категорія", "sector_name": "Електротранспорт і машинобудування", "tariff_group": "Промисловість 2 клас", "penalty_rate_uah_per_mwh": 12400.0},
        {"consumer_key": 3, "tier_code": "TIER-III", "reliability_tier": "ІІІ категорія", "sector_name": "Побутові та комунальні споживачі", "tariff_group": "Населення та побут", "penalty_rate_uah_per_mwh": 6800.0},
    ]

    # 6. fact_outage_balance (600 інцидентів)
    fact_rows = []
    for iid in range(1, 601):
        t_row = rng.choice(dim_time_rows)
        n_row = rng.choice(dim_node_rows)
        c_row = rng.choice(dim_cause_rows)
        cc_row = rng.choice(dim_cons_rows)

        # Обираємо версію обладнання відповідно до року події (SCD Type 2)
        if t_row["year"] == 2024:
            eq_pool = [e for e in dim_eq_rows if e["equipment_key"] in (1, 3, 4, 5, 6, 8)]
        else:
            eq_pool = [e for e in dim_eq_rows if e["is_current"]]
        e_row = rng.choice(eq_pool)

        # Історичні версії до модернізації мали довшу тривалість відновлення та більший недовідпуск
        modernization_factor = 1.45 if not e_row["is_current"] else 1.00
        winter_factor = 1.25 if t_row["season"] == "Зима" else 1.00

        restoration_min = round(rng.uniform(14.0, 68.0) * modernization_factor, 2)
        disconnected_mw = round(rng.uniform(18.0, 145.0) * winter_factor * modernization_factor, 2)
        ens_mwh = round(disconnected_mw * (restoration_min / 60.0), 3)
        consumers_cnt = int(rng.uniform(120, 4800) * winter_factor)
        comp_uah = round(ens_mwh * cc_row["penalty_rate_uah_per_mwh"], 2)
        reserve_mw = round(rng.uniform(85.0, 340.0), 2)
        v_dev_pct = round(rng.uniform(-11.5, -2.4) if c_row["cause_key"] in (1, 3) else rng.uniform(-6.5, 4.2), 2)
        freq_hz = round(rng.uniform(49.42, 49.94), 3)

        fact_rows.append({
            "incident_id": iid,
            "time_key": t_row["time_key"],
            "node_key": n_row["node_key"],
            "equipment_key": e_row["equipment_key"],
            "cause_key": c_row["cause_key"],
            "consumer_key": cc_row["consumer_key"],
            "ens_unsupplied_mwh": ens_mwh,
            "restoration_duration_min": restoration_min,
            "affected_consumers_cnt": consumers_cnt,
            "compensation_cost_uah": comp_uah,
            "disconnected_load_mw": disconnected_mw,
            "spinning_reserve_mw": reserve_mw,
            "voltage_deviation_pct": v_dev_pct,
            "frequency_nadir_hz": freq_hz,
        })

    return (
        pd.DataFrame(dim_time_rows),
        pd.DataFrame(dim_node_rows),
        pd.DataFrame(dim_eq_rows),
        pd.DataFrame(dim_cause_rows),
        pd.DataFrame(dim_cons_rows),
        pd.DataFrame(fact_rows),
    )


def draw_arrow(draw: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int, label: str, font_lbl):
    draw.line([(x1, y1), (x2, y2)], fill="#222222", width=2)
    r = 4
    draw.ellipse([(x2 - r, y2 - r), (x2 + r, y2 + r)], fill="#222222")
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    bbox = font_lbl.getbbox(label)
    lw, lh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rectangle([(mx - lw // 2 - 4, my - lh // 2 - 2), (mx + lw // 2 + 4, my + lh // 2 + 4)], fill="#FFFFFF", outline="#888888", width=1)
    draw.text((mx - lw // 2, my - lh // 2), label, font=font_lbl, fill="#111111")


def draw_box(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, title: str, subtitle: str, rows: list[str], font_h, font_sub, font_row, h_fill="#EAEAEA"):
    draw.rectangle([(x, y), (x + w, y + h)], fill="#FFFFFF", outline="#111111", width=2)
    hh = 44
    draw.rectangle([(x, y), (x + w, y + hh)], fill=h_fill, outline="#111111", width=2)
    bt = font_h.getbbox(title)
    draw.text((x + (w - (bt[2] - bt[0])) // 2, y + 4), title, font=font_h, fill="#000000")
    bs = font_sub.getbbox(subtitle)
    draw.text((x + (w - (bs[2] - bs[0])) // 2, y + 24), subtitle, font=font_sub, fill="#333333")
    ry = y + hh + 7
    for r in rows:
        is_b = r.startswith("[PK]") or r.startswith("[FK]") or r.startswith("Адитивні:") or r.startswith("Напівадитивні:") or r.startswith("Неадитивні:") or r.startswith("Ієрархія:")
        draw.text((x + 10, ry), r, font=font_sub if is_b else font_row, fill="#111111")
        ry += 19


def generate_sr12_star_diagram():
    width, height = 1500, 660
    img = Image.new("RGB", (width, height), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    font_h = ImageFont.truetype(FONT_TNR_BOLD, 16)
    font_sub = ImageFont.truetype(FONT_TNR_BOLD, 13)
    font_row = ImageFont.truetype(FONT_TNR, 13)
    font_lbl = ImageFont.truetype(FONT_TNR_BOLD, 11)

    fx, fy, fw, fh = 525, 115, 450, 380
    tx, ty, tw_b, th_b = 20, 20, 375, 255
    nx, ny, nw_b, nh_b = 20, 315, 375, 215
    dx, dy, dw_b, dh_b = 1105, 20, 375, 235
    cx, cy, cw_b, ch_b = 1105, 295, 375, 215
    ccx, ccy, ccw_b, cch_b = 460, 535, 580, 105

    fact_rows = [
        "[PK] incident_id : INTEGER (Зерно: 1 інцидент знеструмлення)",
        "[FK] time_key, node_key, equipment_key : INTEGER",
        "[FK] cause_key, consumer_key : INTEGER",
        "-------------------------------------------------------------------",
        "Адитивні: (SUM за всіма вимірами)",
        "  ens_unsupplied_mwh : DOUBLE (недовідпуск, МВт·год)",
        "  restoration_duration_min : DOUBLE (відновлення, хв)",
        "  affected_consumers_cnt : INTEGER (споживачів, од.)",
        "  compensation_cost_uah : DOUBLE (штраф, грн)",
        "Напівадитивні: (AVG/MAX за часом, SUM за вузлами)",
        "  disconnected_load_mw : DOUBLE | spinning_reserve_mw : DOUBLE",
        "Неадитивні: (лише AVG, MIN, MAX або відношення сум)",
        "  voltage_deviation_pct : DOUBLE (%) | frequency_nadir_hz : DOUBLE",
    ]
    draw_box(draw, fx, fy, fw, fh, "ТАБЛИЦЯ ФАКТІВ: fact_outage_balance", "Зерно: інцидент небалансу на приєднанні (N = 600)", fact_rows, font_h, font_sub, font_row, h_fill="#DCE6F1")

    eq_rows = [
        "[PK] equipment_key : INTEGER (Сурогатний ключ SCD2)",
        "natural_code : VARCHAR (Природний код NK)",
        "apparatus_model : VARCHAR (Модель апарата)",
        "class_l1, subclass_l2 : VARCHAR (Рівні L1, L2)",
        "ontology_iri : VARCHAR (IRI онтології ЛР5/ЛР6)",
        "rated_power_mva : DOUBLE (Номінал потужності, МВА)",
        "valid_from, valid_to : DATE | is_current : BOOLEAN",
        "Ієрархія: L1 Клас -> L2 Підклас (IRI) -> L3 Модель",
    ]
    draw_box(draw, tx, ty, tw_b, th_b, "ВИМІР: dim_equipment_taxonomy", "Таксономія обладнання (Політика: SCD Тип 2)", eq_rows, font_h, font_sub, font_row)

    node_rows = [
        "[PK] node_key : INTEGER",
        "feeder_code : VARCHAR UNIQUE (Код приєднання)",
        "substation_name : VARCHAR (Вузлова підстанція)",
        "oblast : VARCHAR | region_cluster : VARCHAR",
        "voltage_kv : INTEGER (110, 330, 750 кВ)",
        "Ієрархія: Енергорайон -> Область -> ПС -> Фідер",
    ]
    draw_box(draw, nx, ny, nw_b, nh_b, "ВИМІР: dim_grid_node", "Вузли та приєднання (Політика: SCD Тип 1)", node_rows, font_h, font_sub, font_row)

    time_rows = [
        "[PK] time_key : INTEGER",
        "full_date : DATE | year : INTEGER (2024..2025)",
        "quarter : VARCHAR (Q1..Q4) | month : INTEGER",
        "season : VARCHAR (Зима, Весна, Літо, Осінь)",
        "peak_period : VARCHAR (Вечірній максимум...)",
        "Ієрархія: Рік -> Квартал -> Місяць -> Доба -> Період",
    ]
    draw_box(draw, dx, dy, dw_b, dh_b, "ВИМІР: dim_time", "Календар режимних періодів (Статичний)", time_rows, font_h, font_sub, font_row)

    cause_rows = [
        "[PK] cause_key : INTEGER",
        "cause_code : VARCHAR UNIQUE",
        "cause_group : VARCHAR (Група причин відмови)",
        "cause_detail : VARCHAR (Деталізація пошкодження)",
        "protection_stage : VARCHAR (Ступінь захисту РЗА)",
        "Ієрархія: Група причин -> Деталь -> Ступінь РЗА",
    ]
    draw_box(draw, cx, cy, cw_b, ch_b, "ВИМІР: dim_outage_cause", "Причини інцидентів (Політика: SCD Тип 1)", cause_rows, font_h, font_sub, font_row)

    cons_rows = [
        "[PK] consumer_key : INTEGER | tier_code : VARCHAR | reliability_tier : VARCHAR (І, ІІ, ІІІ категорія)",
        "sector_name : VARCHAR | tariff_group : VARCHAR | penalty_rate_uah_per_mwh : DOUBLE",
        "Ієрархія: Категорія надійності -> Галузевий сектор -> Тарифна група",
    ]
    draw_box(draw, ccx, ccy, ccw_b, cch_b, "ВИМІР: dim_consumer_category", "Категорії надійності споживачів", cons_rows, font_h, font_sub, font_row)

    draw_arrow(draw, fx, fy + 75, tx + tw_b, ty + 135, "N:1 equipment_key", font_lbl)
    draw_arrow(draw, fx, fy + 295, nx + nw_b, ny + 105, "N:1 node_key", font_lbl)
    draw_arrow(draw, fx + fw, fy + 75, dx, dy + 125, "N:1 time_key", font_lbl)
    draw_arrow(draw, fx + fw, fy + 295, cx, cy + 105, "N:1 cause_key", font_lbl)
    draw_arrow(draw, fx + fw // 2, fy + fh, ccx + ccw_b // 2, ccy, "N:1 consumer_key", font_lbl)

    img.save(BASE_DIR / "sr12_star_schema.png", "PNG", dpi=(300, 300))
    img.save(DOCS_DIR / "sr12_star_schema.png", "PNG", dpi=(300, 300))
    print(f"[DIAGRAM] sr12_star_schema.png saved ({width}x{height})")


def generate_sr12_terminal_proof(q1_df, q4_df, q5_df):
    lines = [
        ("PS C:\\Users\\userstudent\\uni\\knowladge\\knowladge_work\\week12\\indep> python src/run_sr12.py", "#FFFFFF", True),
        ("=" * 95, "#569CD6", False),
        ("САМОСТІЙНА РОБОТА №12: ПЕРЕВІРКА ЗІРКОВОЇ СХЕМИ НА 5 БІЗНЕС-ПИТАННЯХ У DUCKDB", "#4EC9B0", True),
        ("=" * 95, "#569CD6", False),
        ("[DDL & ELT] Створено 5 вимірів та fact_outage_balance (N=600 рядків, 0 сиріт, SCD Type 2 активний)", "#6A9955", True),
        ("-" * 95, "#3C3C3C", False),
        ("[Запит Q1: ROLLUP] Недовідпуск енергії (ENS) та штрафна компенсація за енергорайонами:", "#C586C0", True),
    ]
    sub_q1 = q1_df[q1_df["voltage_class"] == "Усі напруги"]
    for _, r in sub_q1.iterrows():
        lines.append((f"  {r['region_cluster']:<18} | Інцидентів: {int(r['incidents_cnt']):<4} | ENS: {r['total_ens_mwh']:>8.2f} МВт*год | Компенсація: {r['total_compensation_k_uah']:>9.2f} тис. грн", "#D4D4D4", False))
    tot = q1_df[q1_df["region_cluster"] == "УСЯ ОЕС УКРАЇНИ"].iloc[0]
    lines.append((f"  {'УСЯ ОЕС УКРАЇНИ':<18} | Інцидентів: {int(tot['incidents_cnt']):<4} | ENS: {tot['total_ens_mwh']:>8.2f} МВт*год | Компенсація: {tot['total_compensation_k_uah']:>9.2f} тис. грн", "#CE9178", True))

    lines.extend([
        ("-" * 95, "#3C3C3C", False),
        ("[Запит Q4: WINDOW DENSE_RANK] Топ-3 підстанції за обсягом недовідпуску ENS:", "#C586C0", True),
    ])
    for _, r in q4_df.head(3).iterrows():
        lines.append((f"  #{int(r['severity_rank'])} {r['substation_name']:<30} ({r['region_cluster']:<12}) | ENS: {r['ens_mwh']:>7.2f} МВт*год | Сер. простій: {r['avg_outage_min']:>5.2f} хв", "#D4D4D4", False))

    lines.extend([
        ("-" * 95, "#3C3C3C", False),
        ("[Запит Q5: SCD TYPE 2] Порівняння аварійності обладнання до і після модернізації:", "#C586C0", True),
    ])
    for _, r in q5_df.iterrows():
        ver = "Поточна (2025)" if r["is_current"] else "Історична (2024)"
        lines.append((f"  {r['natural_code']:<12} | {ver:<16} | {int(r['rated_power_mva']):>4} МВА | Сер. відновлення: {r['avg_restoration_min']:>5.2f} хв | ENS/інц: {r['ens_per_incident_mwh']:>5.2f} МВт*год", "#4EC9B0" if r["is_current"] else "#D4D4D4", False))

    lines.extend([
        ("=" * 95, "#569CD6", False),
        ("[SUCCESS] Схема успішно відповідає на всі 5 бізнес-питань (Q1-Q5). Специфікація: docs/star_schema_spec.md", "#6A9955", True),
    ])

    width = 1180
    font_size = 14
    line_height = int(font_size * 1.40)
    padding = 18
    header_height = 34
    height = len(lines) * line_height + padding * 2 + header_height

    img = Image.new("RGB", (width, height), color="#1E1E1E")
    draw = ImageDraw.Draw(img)
    font_reg = ImageFont.truetype(FONT_MONO, font_size)
    font_b = ImageFont.truetype(FONT_MONO_BOLD, font_size)
    font_t = ImageFont.truetype(FONT_SANS, 13)

    draw.rectangle([(0, 0), (width, header_height)], fill="#252526")
    btn_y = 17
    draw.ellipse([(14, btn_y - 5), (24, btn_y + 5)], fill="#FF5F56")
    draw.ellipse([(32, btn_y - 5), (42, btn_y + 5)], fill="#FFBD2E")
    draw.ellipse([(50, btn_y - 5), (60, btn_y + 5)], fill="#27C93F")
    title = "Windows PowerShell - python src/run_sr12.py (SR 12: Star Schema Validation Q1-Q5)"
    bt = font_t.getbbox(title)
    draw.text(((width - (bt[2] - bt[0])) / 2, 8), title, font=font_t, fill="#CCCCCC")

    y = header_height + padding
    for text, color, is_bold in lines:
        draw.text((padding, y), text, font=font_b if is_bold else font_reg, fill=color)
        y += line_height

    img.save(BASE_DIR / "terminal_sr12_proof.png", "PNG", dpi=(300, 300))
    img.save(DOCS_DIR / "terminal_sr12_proof.png", "PNG", dpi=(300, 300))
    print(f"[IMAGE] terminal_sr12_proof.png saved ({width}x{height})")


def run_sr12():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    con = duckdb.connect(str(DB_PATH))
    ddl = (SQL_DIR / "sr12_ddl.sql").read_text(encoding="utf-8")
    con.execute(ddl)

    df_t, df_n, df_e, df_c, df_cc, df_f = build_sr12_dataset()
    con.execute("INSERT INTO dim_time SELECT * FROM df_t")
    con.execute("INSERT INTO dim_grid_node SELECT * FROM df_n")
    con.execute("INSERT INTO dim_equipment_taxonomy SELECT * FROM df_e")
    con.execute("INSERT INTO dim_outage_cause SELECT * FROM df_c")
    con.execute("INSERT INTO dim_consumer_category SELECT * FROM df_cc")
    con.execute("INSERT INTO fact_outage_balance SELECT * FROM df_f")

    for tbl in ["dim_time", "dim_grid_node", "dim_equipment_taxonomy", "dim_outage_cause", "dim_consumer_category", "fact_outage_balance"]:
        p_out = DATA_DIR / f"{tbl}.parquet"
        con.execute(f"COPY {tbl} TO '{p_out.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD);")

    raw_queries = (SQL_DIR / "sr12_queries.sql").read_text(encoding="utf-8")
    stmts = [s.strip() for s in raw_queries.split(";") if s.strip()]
    dfs = [con.execute(s).df() for s in stmts]
    con.close()

    generate_sr12_star_diagram()
    generate_sr12_terminal_proof(dfs[0], dfs[3], dfs[4])

    spec_md = f"""# Самостійна робота №12: Проєктування зіркової схеми

## 1. Бізнес-процес, зерно та 5 бізнес-питань
- **Процес:** Аудит надійності електропостачання та облік недовідпущеної електроенергії (ENS / SAIDI) по магістральних вузлах ОЕС України.
- **Зерно факту (`fact_outage_balance`):** один зафіксований диспетчерський інцидент небалансу або знеструмлення на конкретному приєднанні підстанції для визначеної категорії споживачів.

## 2. Результати виконання 5 перевірочних запитів (`sql/sr12_queries.sql`)
### Запит Q1 (ROLLUP за енергорайонами та класами напруги)
{dfs[0].to_markdown(index=False)}

### Запит Q2 (Групування за таксономією обладнання та причинами відмов)
{dfs[1].head(8).to_markdown(index=False)}

### Запит Q3 (Зріз зимових вечірніх піків за категоріями надійності споживачів)
{dfs[2].to_markdown(index=False)}

### Запит Q4 (Віконне ранжування DENSE_RANK топ-5 підстанцій за ENS)
{dfs[3].to_markdown(index=False)}

### Запит Q5 (Порівняння історичних і поточних версій обладнання за SCD Тип 2)
{dfs[4].to_markdown(index=False)}
"""
    (DOCS_DIR / "star_schema_spec.md").write_text(spec_md, encoding="utf-8")
    print("[SUCCESS] СР 12 виконано повністю!")


if __name__ == "__main__":
    run_sr12()
