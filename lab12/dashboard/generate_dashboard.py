"""
Результат 5 (Крок 3-4): Генерація аналітичної панелі (4 візуалізації за 5 бізнес-питаннями)
та інтерактивного HTML-дашборду диспетчерської служби ОЕС України.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path
import duckdb
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DASH_DIR = BASE_DIR / "dashboard"
DOCS_DIR = BASE_DIR / "docs"
DB_PATH = DATA_DIR / "olap_grid.duckdb"


def build_dashboard():
    DASH_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(DB_PATH), read_only=True)

    # 1. Питання 1 & 2: Передана електроенергія та питомий коефіцієнт втрат за енергорайонами (Q1 ROLLUP)
    df_reg = con.execute("""
        SELECT
            s.region_cluster,
            ROUND(SUM(f.energy_transmitted_mwh) / 1000.0, 2) AS energy_gwh,
            ROUND(SUM(f.tech_losses_mwh) * 100.0 / NULLIF(SUM(f.energy_transmitted_mwh), 0), 3) AS loss_rate_pct
        FROM fact_grid_telemetry f
        JOIN dim_substation s ON f.substation_key = s.substation_key
        GROUP BY s.region_cluster
        ORDER BY energy_gwh DESC;
    """).df()

    # 2. Питання 3: Drill-down за підкласами таксономії обладнання (простій SAIDI та спрацювання РЗА)
    df_tax = con.execute("""
        SELECT
            t.subclass_level2_name,
            SUM(f.protection_trips_count) AS total_trips,
            ROUND(SUM(f.outage_duration_min) * 1.0 / NULLIF(COUNT(DISTINCT f.taxonomy_key), 0), 1) AS saidi_min
        FROM fact_grid_telemetry f
        JOIN dim_taxonomy_equipment t ON f.taxonomy_key = t.taxonomy_key
        WHERE t.is_current = TRUE
        GROUP BY t.subclass_level2_name
        ORDER BY saidi_min DESC;
    """).df()

    # 3. Питання 4: Помісячна кумулятивна передача та 3-місячне ковзне середнє втрат (Західний район)
    df_win = con.execute("""
        WITH m AS (
            SELECT
                d.month,
                ROUND(SUM(f.energy_transmitted_mwh) / 1000.0, 2) AS energy_gwh,
                ROUND(SUM(f.tech_losses_mwh), 2) AS losses_mwh
            FROM fact_grid_telemetry f
            JOIN dim_substation s ON f.substation_key = s.substation_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE s.region_cluster = 'Західний'
            GROUP BY d.month
        )
        SELECT
            month,
            energy_gwh,
            ROUND(SUM(energy_gwh) OVER (ORDER BY month ROWS UNBOUNDED PRECEDING), 2) AS cum_gwh,
            losses_mwh,
            ROUND(AVG(losses_mwh) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS ma3_losses
        FROM m
        ORDER BY month;
    """).df()

    # 4. Питання 5: Матриця ризику каскадних аварій за категоріями подій та рівнем ожеледі
    df_risk = con.execute("""
        SELECT
            w.icing_risk_level,
            ROUND(AVG(CASE WHEN e.event_category = 'Нормальний режим' THEN f.risk_score END), 3) AS norm_risk,
            ROUND(AVG(CASE WHEN e.event_category = 'Комутаційне збурення' THEN f.risk_score END), 3) AS comm_risk,
            ROUND(AVG(CASE WHEN e.event_category = 'Аварійний режим' THEN f.risk_score END), 3) AS emerg_risk
        FROM fact_grid_telemetry f
        JOIN dim_weather w ON f.weather_key = w.weather_key
        JOIN dim_event_type e ON f.event_type_key = e.event_type_key
        GROUP BY w.icing_risk_level
        ORDER BY CASE w.icing_risk_level
            WHEN 'Низький' THEN 1
            WHEN 'Середній' THEN 2
            WHEN 'Високий' THEN 3
            WHEN 'Критичний' THEN 4
        END;
    """).df()

    con.close()

    # Побудова 4-панельної аналітичної візуалізації (Times New Roman, чистий інженерний стиль)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 10.5

    fig, axes = plt.subplots(2, 2, figsize=(13.2, 6.8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")

    # Панель 1 (верхня ліва): Передана енергія (ГВт*год) та питомий коефіцієнт втрат (%) за регіонами
    ax1 = axes[0, 0]
    x1 = np.arange(len(df_reg))
    bars1 = ax1.bar(x1 - 0.16, df_reg["energy_gwh"], width=0.38, color="#2B5B84", edgecolor="#1B3B58", label="Передана енергія (ГВт·год)")
    ax1.set_xticks(x1)
    ax1.set_xticklabels(df_reg["region_cluster"])
    ax1.set_ylabel("Енергія, ГВт·год")
    ax1.set_ylim(0, 515)
    ax1.set_title("1. Транзит електроенергії та питомі втрати за районами (BQ-1)")
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    for b in bars1:
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 8, f"{b.get_height():.1f}", ha="center", va="bottom", fontsize=8.5)

    ax1_twin = ax1.twinx()
    ax1_twin.plot(x1 + 0.16, df_reg["loss_rate_pct"], color="#C0392B", marker="o", linewidth=2.0, label="Коефіцієнт втрат (%)")
    ax1_twin.set_ylabel("Питомі втрати, %")
    ax1_twin.set_ylim(2.20, 2.72)
    for xi, val in zip(x1 + 0.16, df_reg["loss_rate_pct"]):
        ax1_twin.text(xi, val + 0.02, f"{val:.2f}%", ha="center", va="bottom", fontsize=8.5, color="#901A1E")

    # Панель 2 (верхня права): Drill-down таксономії (SAIDI хв/об'єкт та спрацювання РЗА)
    ax2 = axes[0, 1]
    y2 = np.arange(len(df_tax))
    bars2 = ax2.barh(y2, df_tax["saidi_min"], height=0.55, color="#3A7CA5", edgecolor="#1D4E6C")
    ax2.set_yticks(y2)
    ax2.set_yticklabels(df_tax["subclass_level2_name"])
    ax2.invert_yaxis()
    ax2.set_xlabel("Питомий простій SAIDI, хв/об'єкт")
    ax2.set_title("2. Таксономія L2: питомий простій та спрацювання РЗА (BQ-2, BQ-8)")
    ax2.grid(axis="x", linestyle="--", alpha=0.4)
    ax2.set_xlim(0, max(df_tax["saidi_min"]) * 1.25)
    for b, tr in zip(bars2, df_tax["total_trips"]):
        ax2.text(b.get_width() + 8, b.get_y() + b.get_height() / 2, f"{b.get_width():.1f} хв ({int(tr)} спр.)", va="center", fontsize=8.5)

    # Панель 3 (нижня ліва): Віконна динаміка (місячні втрати + 3-місячне ковзне середнє)
    ax3 = axes[1, 0]
    months = df_win["month"]
    ax3.bar(months, df_win["losses_mwh"], color="#A3C1AD", edgecolor="#4F7762", width=0.6, label="Місячні втрати (МВт·год)")
    ax3.plot(months, df_win["ma3_losses"], color="#1B4D3E", marker="s", linewidth=2.2, label="Ковзне середнє MA(3)")
    ax3.set_xticks(months)
    ax3.set_xticklabels([f"М{m}" for m in months])
    ax3.set_ylabel("Технологічні втрати, МВт·год")
    ax3.set_title("3. Динаміка втрат та 3-місячне ковзне середнє в Західному районі (BQ-6)")
    ax3.grid(axis="y", linestyle="--", alpha=0.4)
    ax3.legend(loc="upper right", frameon=True, fontsize=8.5)

    # Панель 4 (нижня права): Індекс ризику за категоріями подій та рівнем ожеледі (Dice / Risk Matrix)
    ax4 = axes[1, 1]
    x4 = np.arange(len(df_risk))
    w = 0.25
    ax4.bar(x4 - w, df_risk["norm_risk"], width=w, color="#5C926E", edgecolor="#2E563B", label="Нормальний режим")
    ax4.bar(x4, df_risk["comm_risk"], width=w, color="#D99B26", edgecolor="#8F620A", label="Комутаційне збурення")
    ax4.bar(x4 + w, df_risk["emerg_risk"], width=w, color="#C84B31", edgecolor="#7D2412", label="Аварійний режим")
    ax4.axhline(0.75, color="#8B0000", linestyle=":", linewidth=1.4, label="Поріг N-1 (0.75)")
    ax4.set_xticks(x4)
    ax4.set_xticklabels(df_risk["icing_risk_level"])
    ax4.set_ylabel("Середній індекс ризику (0..1)")
    ax4.set_ylim(0, 1.05)
    ax4.set_title("4. Ескалація індексу ризику при ожеледі та аваріях (BQ-4, BQ-5)")
    ax4.grid(axis="y", linestyle="--", alpha=0.4)
    ax4.legend(loc="upper left", ncol=2, frameon=True, fontsize=8.0)

    plt.tight_layout(pad=1.3)
    panel_png = DASH_DIR / "analytics_panel.png"
    fig.savefig(panel_png, dpi=300)
    fig.savefig(BASE_DIR / "analytics_panel.png", dpi=300)
    plt.close(fig)

    # Збереження HTML-версії дашборду у dashboard/index.html
    html_content = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <title>OLAP Аналітична панель ОЕС України (ЛР 12)</title>
  <style>
    body { font-family: 'Times New Roman', serif; margin: 24px; background: #f8fafc; color: #1e293b; }
    h1 { margin-bottom: 4px; }
    .subtitle { color: #475569; margin-bottom: 18px; }
    .panel-img { max-width: 100%; border: 1px solid #cbd5e1; background: #fff; padding: 8px; }
    .cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 16px; }
    .card { background: #fff; border: 1px solid #cbd5e1; padding: 12px; }
  </style>
</head>
<body>
  <h1>Аналітична панель OLAP-куба енергомережі на основі таксономії (ЛР 12)</h1>
  <div class="subtitle">Студент: Гріджак Олександр (ФЕІ-43) | СУБД: DuckDB + Семантичний шар metrics.yml</div>
  <img class="panel-img" src="analytics_panel.png" alt="OLAP Analytics Panel">
  <div class="cards">
    <div class="card"><b>Візуалізація 1 (Транзит і втрати):</b> Центральний (438.0 ГВт·год) та Дніпровський (262.5 ГВт·год) райони забезпечують основний обсяг передачі, а найвища питома частка втрат (2.60%) спостерігається у Південному районі.</div>
    <div class="card"><b>Візуалізація 2 (Drill-down таксономії):</b> Найвищий питомий простій SAIDI припадає на силові трансформатори (PowerTransformer - 578.0 хв/об'єкт) та повітряні лінії (OverheadLine - 488.8 хв/об'єкт).</div>
    <div class="card"><b>Візуалізація 3 (Віконне згладжування):</b> Тримісячне ковзне середнє MA(3) у Західному районі фіксує зимовий пік технологічних втрат у січні-лютому та грудні.</div>
    <div class="card"><b>Візуалізація 4 (Матриця ризику N-1):</b> За критичного рівня ожеледі середній індекс ризику в аварійних режимах перетинає граничний поріг 0.75, досягаючи 0.86.</div>
  </div>
</body>
</html>
"""
    (DASH_DIR / "index.html").write_text(html_content, encoding="utf-8")

    # Опис панелі та ризиків у docs/dashboard_report.md
    report_md = """# Аналітична панель та аналіз ризиків Text-to-SQL (Результат 5)

## 1. Інтерпретація 4 візуалізацій аналітичної панелі (`dashboard/analytics_panel.png`)
1. **Панель 1 (Баланс транзиту та питомих втрат за енергорайонами - BQ-1):** Центральний енергорайон транспортує найбільший обсяг електроенергії (`437.98 ГВт·год`), далі йдуть Дніпровський (`262.53 ГВт·год`) та Західний (`256.32 ГВт·год`). Питомий коефіцієнт втрат коливається від `2.471%` у Західному районі до `2.602%` у Південному через вищу частку розподільчих ліній 110 кВ.
2. **Панель 2 (Деталізація простоїв SAIDI та спрацювань РЗА за підкласами таксономії - BQ-2, BQ-8):** Перехід на рівень підкласів таксономії показує, що силові автотрансформатори (`PowerTransformer`) мають найвищий питомий простій (`578.0 хв/об'єкт`) через тривалість виведення в ремонт після диференційних відключень, тоді як повітряні лінії (`OverheadLine`) лідирують за абсолютною кількістю спрацювань захисту (`236` циклів, більшість з яких успішно ліквідується АПВ).
3. **Панель 3 (Помісячна динаміка втрат і 3-місячне ковзне середнє - BQ-6):** Віконна функція `AVG() OVER (ROWS 2 PRECEDING)` виділяє сезонний профіль навантаження Західного енергорайону: максимуми втрат припадають на зимові місяці проходження пікових навантажень.
4. **Панель 4 (Матриця каскадного ризику за категоріями подій та рівнем ожеледі - BQ-4, BQ-5):** При переході від низького до критичного ризику ожеледі індекс ризику під час аварійних подій зростає з `0.68` до `0.86`, перевищуючи нормативний поріг критерію стійкості `N-1 (0.75)`.

## 2. Ключові ризики Text-to-SQL та впроваджені механізми захисту (Крок 4)
1. **Ризик 1: Спотворення неадитивних метрик (Aggregation Fallacy):** Без семантичного словника генеративні моделі часто усереднюють відсотки (`AVG(losses/energy)`) замість обчислення відношення сум (`SUM(losses)/SUM(energy)`). *Захист:* інжекція канонічних формул із `semantic/metrics.yml` у системний контекст генератора.
2. **Ризик 2: Подвійний облік історичних версій SCD Type 2:** Забуття умови `WHERE is_current = TRUE` при агрегації паспортних потужностей виміру `dim_taxonomy_equipment` завищує встановлену потужність на величину закритих історичних записів. *Захист:* автоматичне закріплення умови `t.is_current = TRUE` у правилах `dimension_joins` семантичного шару.
3. **Ризик 3: Деструктивні SQL-ін'єкції та мутації даних:** Зловмисник може передати в промпт конструкцію `; DROP TABLE ...` або `COPY ... TO`. *Захист:* обов'язковий розбір запиту в синтаксичне дерево AST бібліотекою `sqlglot` із дозволом виключно одного кореневого вузла `exp.Select` та відкриттям бази в режимі `read_only=True`.
4. **Ризик 4: Вихід із пісочниці файлової системи та виснаження ресурсів (DoS):** У DuckDB табличні функції `read_csv_auto()` або `read_parquet()` дозволяють читати довільні файли диска, а декартові добутки без `LIMIT` завишують процес. *Захист:* блокування системних функцій у вузлах AST, примусовий `LIMIT 100`, перевірка плану `EXPLAIN` та жорсткий тайм-аут виконання `2.0 с`.
"""
    (DOCS_DIR / "dashboard_report.md").write_text(report_md, encoding="utf-8")
    print("[DASHBOARD] Аналітичну панель збережено у dashboard/analytics_panel.png та dashboard/index.html.")


if __name__ == "__main__":
    build_dashboard()
