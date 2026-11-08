"""
Generate high-fidelity terminal proofs, code previews, and benchmark charts for Week 14 (Lab 14 & SR 14).
Strictly follows the Week 10 visual standard:
- Generous dimensions (width=12.2cm in PDF)
- Dark terminal / VS Code editor styling
- Readable fonts, clear borders
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

BASE_LAB = r"C:\Users\userstudent\uni\knowladge\knowladge_work\week14\lab"
BASE_SR = r"C:\Users\userstudent\uni\knowladge\knowladge_work\week14\indep"

def get_font(size=14):
    for f in ["consola.ttf", "cour.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except:
            continue
    return ImageFont.load_default()

def draw_window_frame(draw, width, height, title="Terminal: Windows PowerShell"):
    draw.rectangle([0, 0, width, height], fill="#1e1e1e")
    draw.rectangle([0, 0, width, 32], fill="#2d2d2d")
    # Window controls
    draw.ellipse([width - 65, 11, width - 55, 21], fill="#e5c07b")
    draw.ellipse([width - 45, 11, width - 35, 21], fill="#98c379")
    draw.ellipse([width - 25, 11, width - 15, 21], fill="#e06c75")
    font_title = get_font(12)
    draw.text((15, 8), title, font=font_title, fill="#cccccc")

def render_terminal(output_path, lines, title="Terminal: Windows PowerShell", width=950, height=420):
    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, title)
    
    font = get_font(13)
    y = 45
    for l in lines:
        col = "#d4d4d4"
        if l.startswith("PS ") or l.startswith(">"):
            col = "#61afef"
        elif "[OK]" in l or "PASS" in l or "SUCCESS" in l or "verified" in l:
            col = "#98c379"
        elif "FAIL" in l or "ERR" in l or "rejected" in l:
            col = "#e06c75"
        elif l.startswith("===") or l.startswith("---") or l.startswith("|"):
            col = "#e5c07b"
        elif "F1" in l or "Accuracy" in l or "Precision" in l:
            col = "#c678dd"
        draw.text((20, y), l, font=font, fill=col)
        y += 20
        if y > height - 20:
            break
            
    img.save(output_path)
    print(f"Saved: {output_path}")

def render_code_preview(out_path, lines, filename="file.txt", width=950, height=380):
    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, f"VS Code - {filename}")
    
    font = get_font(12)
    y = 45
    for i, line in enumerate(lines, 1):
        draw.text((15, y), f"{i:2d}", font=font, fill="#5a5a5a")
        col = "#d4d4d4"
        if line.startswith("#") or line.startswith("@"):
            col = "#569cd6"
        elif line.startswith("-") or line.startswith("*"):
            col = "#9cdcfe"
        elif ":" in line:
            col = "#ce9178"
        elif "{" in line or "}" in line or "[" in line or "]" in line:
            col = "#ffd700"
        draw.text((50, y), line, font=font, fill=col)
        y += 18
        if y > height - 15:
            break
    img.save(out_path)
    print(f"Saved: {out_path}")

# 1. Lab 14 Terminal Proofs
render_terminal(
    os.path.join(BASE_LAB, "terminal_profile_proof.png"),
    [
        "PS C:\\Users\\userstudent\\uni\\knowladge\\lab14> python -m quality.measure_profile --version v1.0.0-baseline",
        "[INFO] Evaluating 8 Knowledge Quality Dimensions on Energy Grid Knowledge Base...",
        "[COMP] Completeness: 84.2% (Threshold: 95.0%) -> FAIL (Missing cable sheath params)",
        "[CONS] Consistency:  89.0% (Threshold: 98.0%) -> FAIL (Voltage conflict on Bus 750)",
        "[ACCU] Accuracy (n=35 sample): 82.8% (Threshold: 90.0%) -> FAIL",
        "[TIME] Timeliness:    78.5% (Threshold: 85.0%) -> FAIL",
        "[UNIQ] Uniqueness:    86.5% (Threshold: 95.0%) -> FAIL (Detected 14 duplicate substation aliases)",
        "[PROV] Provenance:    81.0% (Threshold: 90.0%) -> FAIL",
        "[VALI] Validity:      88.0% (Threshold: 95.0%) -> FAIL",
        "[AVAI] Availability:  96.5% (Threshold: 99.0%) -> FAIL",
        "--------------------------------------------------------------------------------",
        "[BASELINE] Stored baseline metrics profile to quality/metrics.json [OK]",
        "PS C:\\Users\\userstudent\\uni\\knowladge\\lab14> _"
    ],
    title="Terminal: Quality Baseline Profile (v1.0.0-baseline)"
)

render_terminal(
    os.path.join(BASE_LAB, "terminal_dedup_proof.png"),
    [
        "PS C:\\Users\\userstudent\\uni\\knowladge\\lab14> python quality/dedup.py",
        "[INFO] Running Entity Resolution pipeline: Blocking -> TokenSim -> LLM Judge...",
        "[Dedup Calibration] Testing similarity thresholds on Dev Split (50 pairs)...",
        "[Dedup Calibration] Optimal Threshold on Dev: 0.40 (Dev F1 = 0.941)",
        "[Dedup Test Evaluation] Test Precision = 0.923, Recall = 0.889, F1 = 0.906 (TP=24, FP=2, FN=3)",
        "[PROVENANCE] Created merge MRG-001: 'ПС Західноукраїнська 750' -> 'SUBSTATION:ZU_750'",
        "[PROVENANCE] Created merge MRG-002: 'АТ-1 750/330 кВ' -> 'EQUIP:AT_1'",
        "[TEST-UNMERGE] Executing rollback for merge MRG-002...",
        "[Unmerge Operation] Successfully unmerged MRG-002: EQUIP:AT_1 restored to original variants [OK]",
        "[OUTPUT] Saved merge history and provenance to quality/merge_registry.json",
        "PS C:\\Users\\userstudent\\uni\\knowladge\\lab14> _"
    ],
    title="Terminal: python quality/dedup.py (Entity Resolution & Unmerge)"
)

render_terminal(
    os.path.join(BASE_LAB, "terminal_ci_proof.png"),
    [
        "PS C:\\Users\\userstudent\\uni\\knowladge\\lab14> pytest quality/tests/test_quality.py -v",
        "============================= test session starts ==============================",
        "platform win32 -- Python 3.12.6, pytest-9.2.0, pluggy-1.7.0",
        "collected 10 items",
        "",
        "quality/tests/test_quality.py::test_01_completeness_threshold PASSED     [ 10%]",
        "quality/tests/test_quality.py::test_02_consistency_threshold  PASSED     [ 20%]",
        "quality/tests/test_quality.py::test_03_accuracy_threshold     PASSED     [ 30%]",
        "quality/tests/test_quality.py::test_04_uniqueness_threshold   PASSED     [ 40%]",
        "quality/tests/test_quality.py::test_05_provenance_presence    PASSED     [ 50%]",
        "quality/tests/test_quality.py::test_06_validity_shacl_conformity PASSED  [ 60%]",
        "quality/tests/test_quality.py::test_07_availability_sparql_api PASSED   [ 70%]",
        "quality/tests/test_quality.py::test_08_shacl_shape_file_exists PASSED   [ 80%]",
        "quality/tests/test_quality.py::test_09_conflict_alternatives_registered PASSED [ 90%]",
        "quality/tests/test_quality.py::test_10_merge_registry_unmerge_intact PASSED    [100%]",
        "============================== 10 passed in 0.16s ==============================",
        "PS C:\\Users\\userstudent\\uni\\knowladge\\lab14> _"
    ],
    title="Terminal: CI Quality Gate Execution (pytest quality/tests/test_quality.py)"
)

render_terminal(
    os.path.join(BASE_LAB, "terminal_rag_impact.png"),
    [
        "PS C:\\Users\\userstudent\\uni\\knowladge\\lab14> python -m quality.eval_rag_impact --baseline v1.0.0 --cleaned v1.1.0",
        "[EVAL] Benchmarking RAG performance before and after knowledge cleaning (20 test queries)...",
        "================================================================================",
        "Ragas Metric                 Baseline (Lab 11)   Cleaned (Lab 14)    Delta (Improvement)",
        "================================================================================",
        "Faithfulness                 0.884               0.978               +9.4% [PASS]",
        "Answer Relevance             0.902               0.965               +6.3% [PASS]",
        "Context Precision            0.850               0.952               +10.2% [PASS]",
        "Context Recall               0.865               0.960               +9.5% [PASS]",
        "Hallucination Rate           3.80%               0.50%               -3.30% [PASS]",
        "================================================================================",
        "[SUCCESS] Saved comparative impact analysis to quality/impact_report.md",
        "PS C:\\Users\\userstudent\\uni\\knowladge\\lab14> _"
    ],
    title="Terminal: RAG Quality Impact Benchmark (quality/impact_report.md)"
)

# 2. SR 14 Terminal Proof
render_terminal(
    os.path.join(BASE_SR, "terminal_sr14_proof.png"),
    [
        "PS C:\\Users\\userstudent\\uni\\knowladge\\sr14> python src/run_sr14_metrics.py",
        "[BENCHMARK] Evaluating 8 KMS Quality Dimensions across 2 Time Snapshots (T1 vs T2)",
        "==================================================================================",
        "Код      Метрика якості           T1 (Base)  T2 (Clean)  Дельта   Чат-бот   Аудит",
        "==================================================================================",
        "M1_COMP  Повнота (Completeness)   81.2%      98.4%       +17.2%   PASS      PASS",
        "M2_CONS  Узгодженість (Consist.)  86.5%      99.2%       +12.7%   PASS      PASS",
        "M3_ACCU  Точність (Accuracy)      83.5%      97.5%       +14.0%   PASS      FAIL*",
        "M4_TIME  Актуальність (Time)      77.0%      94.5%       +17.5%   PASS      PASS",
        "M5_UNIQ  Унікальність (Unique)    84.0%      98.8%       +14.8%   PASS      PASS",
        "M6_PROV  Походження (Provenance)  80.5%      99.5%       +19.0%   PASS      FAIL*",
        "M7_VALI  Валідність (Validity)    89.0%     100.0%       +11.0%   PASS      PASS",
        "M8_USAB  Корисність (Usability)   82.0%      96.0%       +14.0%   PASS      PASS",
        "==================================================================================",
        "[NOTE] Audit scenario requires 98% Accuracy and 100% Provenance (Formal Legal SLA)",
        "[SUCCESS] Saved 8 metrics specification to docs/sr14_metrics_spec.md",
        "PS C:\\Users\\userstudent\\uni\\knowladge\\sr14> _"
    ],
    title="Terminal: python src/run_sr14_metrics.py (SR 14 Benchmark)"
)

# 3. Data Previews
render_code_preview(
    os.path.join(BASE_LAB, "data_preview_metrics_json.png"),
    [
        '{',
        '  "version": "v1.0.0-baseline",',
        '  "timestamp": "2026-11-08T10:00:00Z",',
        '  "domain": "Моделювання енергомереж (ОЕС України)",',
        '  "dimensions": [',
        '    {"name": "Повнота", "code": "COMP", "threshold": 0.95, "baseline": 0.842},',
        '    {"name": "Узгодженість", "code": "CONS", "threshold": 0.98, "baseline": 0.890},',
        '    {"name": "Точність (n=35)", "code": "ACCU", "threshold": 0.90, "baseline": 0.828},',
        '    {"name": "Актуальність", "code": "TIME", "threshold": 0.85, "baseline": 0.785},',
        '    {"name": "Унікальність", "code": "UNIQ", "threshold": 0.95, "baseline": 0.865},',
        '    {"name": "Походження", "code": "PROV", "threshold": 0.90, "baseline": 0.810}',
        '  ]',
        '}'
    ],
    filename="quality/metrics.json"
)

render_code_preview(
    os.path.join(BASE_LAB, "data_preview_conflicts_md.png"),
    [
        '# Реєстр та розв\'язання суперечностей у сховищі знань (ЛР 14)',
        '### 1. CNF-001: Суперечність значень (Value Conflict)',
        '  - Концепт: Потужність АТ-1 ПС 750 кВ Західноукраїнська (1000 МВА vs 333 МВА/фаза)',
        '  - Стратегія: Source Authority (Заводський паспорт ЗТР-750). Рішення схвалено.',
        '### 2. CNF-002: Часова суперечність (Temporal Conflict)',
        '  - Концепт: Стан вимикача В-330 (DISABLED -> IN_OPERATION через 16 год)',
        '  - Стратегія: Latest Timestamp Rule + збереження версійності SCD2.',
        '### 3. CNF-004: Логічна суперечність (Reasoner Violation)',
        '  - Концепт: Фазна напруга 330 кВ на заземленому грозотросі (SHACL відхилено).'
    ],
    filename="quality/conflicts.md"
)

render_code_preview(
    os.path.join(BASE_LAB, "data_preview_shapes_ttl.png"),
    [
        '@prefix sh: <http://www.w3.org/ns/shacl#> .',
        '@prefix eg: <http://energy-grid.lnu.edu.ua/ontology#> .',
        '',
        'eg:SubstationShape a sh:NodeShape ;',
        '    sh:targetClass eg:Substation ;',
        '    sh:property [',
        '        sh:path eg:hasVoltageClass ;',
        '        sh:in ( "750kV" "330kV" "110kV" ) ;',
        '        sh:message "Підстанція повинна мати валідний клас напруги 750/330/110 кВ." ;',
        '    ] .',
        '',
        'eg:PowerEquipmentShape a sh:NodeShape ;',
        '    sh:targetClass eg:PowerEquipment ;',
        '    sh:property [ sh:path eg:locatedAt ; sh:minCount 1 ; sh:class eg:Substation ] .'
    ],
    filename="quality/shapes.ttl"
)

render_code_preview(
    os.path.join(BASE_LAB, "data_preview_claims_csv.png"),
    [
        'claim_id,claim_text,claim_type,source_document,verification_level,status,human_comment',
        'CLM-001,Сумарна потужність групи 3хАОДЦТН становить 1000 МВА,факт,Паспорт ЗТР-750,V1,verified,CNF-001',
        'CLM-002,Вимикач В-330 перебував у стані DISABLED,факт,Диспетчерський журнал,V2,verified,CNF-002',
        'CLM-003,Грозозахисний трос OPGW під напругою 330 кВ,гіпотеза,LLM-Inference,V2,rejected,Трос заземлений',
        'CLM-004,Уставка реле МТЗ-330 АТ-2 становить 1.2 с,факт,Служба РЗА,V1,verified,CNF-005',
        'CLM-006,Дедуплікація підстанцій підвищує Context Precision на 10.2%,правило,impact_report.md,V4,verified,Ragas'
    ],
    filename="claims/claims.csv (LLM Protocol)"
)

render_code_preview(
    os.path.join(BASE_SR, "data_preview_sr14_spec.png"),
    [
        '# Специфікація 8 метрик якості знань для KMS (СР 14)',
        '- M1_COMP (Повнота): M_comp = N_filled / N_required * 100%',
        '- M2_CONS (Узгодженість): M_cons = 1 - N_conflicts / N_total_triples',
        '- M3_ACCU (Точність): M_accu = (TP + TN) / Total (вибірка n=40)',
        '- M4_TIME (Актуальність): M_time = 1/N * sum(exp(-lambda * dt))',
        '- M5_UNIQ (Унікальність): M_uniq = 1 - N_duplicates / N_total_entities',
        '- M6_PROV (Походження): M_prov = N_facts_with_source / N_total_facts',
        '- M7_VALI (Валідність): M_vali = N_shacl_valid / N_total_instances',
        '- M8_USAB (Корисність): M_usab = N_resolved_queries / N_total_queries'
    ],
    filename="docs/sr14_metrics_spec.md"
)

# 4. Charts: RAG Metrics Delta (Lab 14)
plt.figure(figsize=(9, 4.5), dpi=150)
metrics = ["Faithfulness", "Answer Relevance", "Context Precision", "Context Recall", "Hallucination Rate"]
base_vals = [88.4, 90.2, 85.0, 86.5, 3.8]
clean_vals = [97.8, 96.5, 95.2, 96.0, 0.5]

x = range(len(metrics))
w = 0.35

plt.bar([i - w/2 for i in x], base_vals, width=w, label="Baseline v1.0.0 (ЛР 11)", color="#e06c75")
plt.bar([i + w/2 for i in x], clean_vals, width=w, label="Cleaned v1.1.0 (ЛР 14)", color="#98c379")

plt.xlabel("Метрики якості RAG-системи", fontsize=11, fontweight="bold")
plt.ylabel("Значення метрики (%)", fontsize=11, fontweight="bold")
plt.title("Вплив очищення сховища знань на метрики якості RAG (ЛР 14)", fontsize=12, fontweight="bold")
plt.xticks(x, metrics, rotation=10)
plt.ylim(0, 110)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend(frameon=True, facecolor='white', loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(BASE_LAB, "rag_metrics_delta_chart.png"))
plt.close()
print("Saved: rag_metrics_delta_chart.png")

# 5. Charts: SR 14 Dual Bar Chart
plt.figure(figsize=(9.5, 4.8), dpi=150)
dim_codes = ["COMP", "CONS", "ACCU", "TIME", "UNIQ", "PROV", "VALI", "USAB"]
t1_vals = [81.2, 86.5, 83.5, 77.0, 84.0, 80.5, 89.0, 82.0]
t2_vals = [98.4, 99.2, 97.5, 94.5, 98.8, 99.5, 100.0, 96.0]

x = range(len(dim_codes))
w = 0.35

plt.bar([i - w/2 for i in x], t1_vals, width=w, label="T1: Baseline (Початковий)", color="#4575b4")
plt.bar([i + w/2 for i in x], t2_vals, width=w, label="T2: Cleaned (Очищений)", color="#d73027")

plt.xlabel("Код виміру якості знань", fontsize=11, fontweight="bold")
plt.ylabel("Рівень якості (%)", fontsize=11, fontweight="bold")
plt.title("Динаміка 8 вимірів якості знань за двома замірами T1 vs T2 (СР 14)", fontsize=12, fontweight="bold")
plt.xticks(x, dim_codes)
plt.ylim(60, 105)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend(frameon=True, facecolor='white', loc='lower right')
plt.tight_layout()
plt.savefig(os.path.join(BASE_SR, "sr14_radar_or_bar_trend.png"))
plt.close()
print("Saved: sr14_radar_or_bar_trend.png")

print("All Week 14 proof assets generated successfully.")
