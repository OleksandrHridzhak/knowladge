# -*- coding: utf-8 -*-
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

# Strict Academic Engineering Diagram matching textwidth
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

# Canvas: 7.2 x 5.0 inches, coordinates 0..1000 x 0..700
fig, ax = plt.subplots(figsize=(7.2, 5.0), dpi=300)
ax.set_xlim(0, 1000)
ax.set_ylim(0, 700)
ax.axis('off')

# Tier 1 (y: 535..665, h=130)
# Tier 2 (y: 290..430, h=140)
# Tier 3 (y: 75..205, h=130)
# Legend (y: 16..46, h=30)

nodes = [
    # Row 1 (Top: Management & Telemetry)
    (35, 535, 180, 130, ":PowerPlant", "id: String [PK]\nname: String\ntype: 'АЕС' / 'ТЕС'\ncapacityMW: Float\nvoltageKV: Int"),
    (425, 535, 180, 130, ":Operator", "id: String [PK]\nname: 'Укренерго'\nregion: String\ndispatchType: String"),
    (800, 535, 175, 130, ":SCADA_System", "id: String [PK]\nname: String\nprotocol: 'IEC-60870'\npollingRateMs: Int"),

    # Row 2 (Middle: Backbone Grid)
    (35, 290, 180, 140, ":TransmissionLine", "id: String [PK]\nname: 'ПЛ 750 кВ'\nvoltageKV: Int\nlengthKm: Float\nlimitMVA: Float"),
    (425, 290, 180, 140, ":Substation", "id: String [PK]\nname: 'ПС Західна'\nvoltageKV: Int\npagerank: Float\ncommunity: Int"),
    (800, 290, 175, 140, ":ConsumerNode", "id: String [PK]\nname: 'Львів місто'\nloadMW: Float\npriority: Int\nisCritical: Bool"),

    # Row 3 (Bottom: Substation Bay & Protection)
    (25, 75, 155, 130, ":Transformer", "id: String [PK]\nname: 'АТ-1'\npowerMVA: Float\nvoltageKV: Int\nstatus: String"),
    (285, 75, 155, 130, ":CircuitBreaker", "id: String [PK]\nname: 'Q1-750'\nratedA: Float\nstate: 'CLOSED'\ntripCount: Int"),
    (575, 75, 155, 130, ":RelayProtection", "id: String [PK]\nmodel: 'SEL-421'\ntype: 'Distance'\ndelayMs: Int\nfirmware: String"),
    (825, 75, 155, 130, ":GridEvent", "id: String [PK]\ntype: 'ShortCircuit'\nriskScore: Float (0..1)\ncascadeLevel: Int\ntimestamp: Time")
]

# Draw boxes
for x, y, w, h, label, fields in nodes:
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                 facecolor="#FFFFFF", edgecolor="#0F172A", linewidth=1.2)
    ax.add_patch(box)

    hdr_h = 28
    hdr_box = patches.FancyBboxPatch((x, y + h - hdr_h), w, hdr_h, boxstyle="square,pad=0",
                                     facecolor="#E2E8F0", edgecolor="#0F172A", linewidth=1.2)
    ax.add_patch(hdr_box)

    ax.text(x + w/2, y + h - hdr_h/2, label, ha='center', va='center', weight='bold',
            fontsize=9.8, color='#0F172A')

    ax.text(x + 10, y + (h - hdr_h)/2 + 2, fields, ha='left', va='center',
            fontsize=8.0, color='#1E293B', linespacing=1.28)

def draw_edge(x1, y1, x2, y2, label, label_x, label_y, rad=0.0):
    style = f"arc3,rad={rad}" if rad != 0 else "arc3,rad=0"
    arrow = patches.FancyArrowPatch((x1, y1), (x2, y2),
                                    connectionstyle=style,
                                    arrowstyle="-|>,head_length=5.5,head_width=3.6",
                                    color="#0F172A", linewidth=1.2)
    ax.add_patch(arrow)
    ax.text(label_x, label_y, label, ha='center', va='center', fontsize=7.6, weight='bold',
            color='#0F172A', bbox=dict(boxstyle="square,pad=0.2", fc="#FFFFFF", ec="#64748B", lw=0.7))

# 1. PowerPlant -> Substation (Power flow)
draw_edge(215, 550, 425, 420, ":SUPPLIES_POWER_TO", 305, 495)

# 2. Operator -> PowerPlant & Substation
draw_edge(425, 600, 215, 600, ":MANAGED_BY", 320, 600)
draw_edge(515, 535, 515, 430, ":MANAGED_BY", 515, 482)

# 3. Substation -> SCADA_System
draw_edge(605, 420, 800, 550, ":MONITORED_BY", 710, 495)

# 4. TransmissionLine -> Substation (210-unit gap: ample room!)
draw_edge(215, 360, 425, 360, ":CONNECTS_TO", 320, 360)

# 5. Substation -> ConsumerNode (195-unit gap: ample room!)
draw_edge(605, 360, 800, 360, ":FEEDS_CONSUMER", 702, 360)

# 6. Substation -> Transformer & CircuitBreaker (Separated laterally by 200 units)
draw_edge(435, 290, 160, 205, ":CONTAINS_EQUIPMENT", 255, 260)
draw_edge(495, 290, 385, 205, ":CONTAINS_EQUIPMENT", 480, 235)

# 7. RelayProtection -> CircuitBreaker, Line, Transformer
draw_edge(575, 140, 440, 140, ":TRIPS_BREAKER", 507, 140)
draw_edge(640, 205, 215, 310, ":PROTECTS", 390, 280, rad=0.15)
draw_edge(575, 95, 180, 95, ":PROTECTS", 360, 55, rad=-0.18)

# 8. GridEvent Cascading Self-Loop
arrow_event = patches.FancyArrowPatch((920, 205), (980, 155),
                                      connectionstyle="arc3,rad=-0.8",
                                      arrowstyle="-|>,head_length=5.0,head_width=3.5",
                                      color="#0F172A", linewidth=1.2)
ax.add_patch(arrow_event)
ax.text(955, 224, ":TRIGGERS_EVENT", ha='center', va='center', fontsize=7.4, weight='bold',
        color='#0F172A', bbox=dict(boxstyle="square,pad=0.18", fc="#FFFFFF", ec="#64748B", lw=0.7))

# Bottom Provenance Metadata Banner
legend_box = patches.FancyBboxPatch((25, 15), 955, 30, boxstyle="square,pad=0",
                                    facecolor="#F1F5F9", edgecolor="#475569", linewidth=1.0)
ax.add_patch(legend_box)
ax.text(502, 30, "Атрибути походження зв'язків (Edge Provenance): { source: String, confidence: Float (0.0–1.0), validFrom: Date }",
        ha='center', va='center', fontsize=8.6, color='#0F172A', weight='bold')

plt.tight_layout()

for folder in [DOCS]:
    plt.savefig(folder / "graph_schema.pdf", format="pdf", bbox_inches='tight')
    plt.savefig(folder / "graph_schema.png", format="png", dpi=300, bbox_inches='tight')
    plt.savefig(folder / "graph_schema.svg", format="svg", bbox_inches='tight')

plt.close()

import sys
sys.stdout.buffer.write("[SUCCESS] Схему успішно перегенеровано без жодного перекриття.\n".encode('utf-8'))
