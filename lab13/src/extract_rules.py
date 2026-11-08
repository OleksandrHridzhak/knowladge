"""
Method A: Rule-based & Pattern Information Extraction using spaCy and Regex.
Extracts entities and relations from Ukrainian energy dispatch text.
"""
import os
import json
import re
import spacy
from spacy.tokens import Doc

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Voltage regex patterns
VOLT_PATTERN = re.compile(r'\b(750|330|110|35|10|0\.4)\s*кВ\b', re.IGNORECASE)
SUBSTATION_PATTERN = re.compile(r'ПС\s+(?:(?:\d+\s*кВ\s+)?)([А-ЯЄІЇҐ][а-яєіїґ\w\-]+)', re.IGNORECASE)
LINE_PATTERN = re.compile(r'ПЛ\s+(?:(?:\d+\s*кВ\s+)?)([А-ЯЄІЇҐ][а-яєіїґ\w\-]+(?:\s*-\s*[А-ЯЄІЇҐ][а-яєіїґ\w\-]+)+)', re.IGNORECASE)
EQUIP_PATTERN = re.compile(r'\b(автотрансформатор[а-я]*\s+АТ-\d+|вимикач[а-я]*\s+В-\d+|реактор[а-я]*\s+[\w\-]+|трансформатор[а-я]*\s+струму\s+[\w\-]+|шинн[а-я]+\s+міст|щит\s+власних\s+потреб|грозозахисн[а-я]+\s+трос(?:і|у)?|кабельн[а-я]+\s+муфт[а-я]*)\b', re.IGNORECASE)
RELAY_PATTERN = re.compile(r'\b(ДФЗ-\d+|SEL-\d+|ДЗШ(?:-\d+)?|РГТ(?:-\d+)?|РТ-\d+|ДЗТ-\d+|УРОВ|АОП|АРПН|РПН-\d+|ВМП|МТЗ(?:-\d+)?|АВР)\b')
FAULT_PATTERN = re.compile(r'\b(коротке\s+замикання|перегрів\s+контактного\s+з\'єднання|налипання\s+мокрого\s+снігу|ожеледоутворення|пляска\s+проводів|розряд\s+блискавки|струмове\s+перевантаження|витік\s+елегазу|руйнування\s+фарфорового\s+ізолятора|зниження\s+рівня\s+масла|обрив\s+оптичного\s+кабелю)\b', re.IGNORECASE)
WEATHER_PATTERN = re.compile(r'\b(шквальн[а-я]+\s+віт(?:ер|ру)|мокр[а-я]+\s+сніг[а-я]*|ожелед[а-я]*|грозов[а-я]+\s+фронт[а-я]*|падіння\s+дерева)\b', re.IGNORECASE)

nlp = spacy.blank("uk")

def extract_entities_and_relations(text, doc_id):
    results = []
    
    # 1. Regex Entity Matching
    volts = [m.group(0) for m in VOLT_PATTERN.finditer(text)]
    substations = [m.group(0) for m in SUBSTATION_PATTERN.finditer(text)]
    lines = [m.group(0) for m in LINE_PATTERN.finditer(text)]
    equips = [m.group(0) for m in EQUIP_PATTERN.finditer(text)]
    relays = [m.group(0) for m in RELAY_PATTERN.finditer(text)]
    faults = [m.group(0) for m in FAULT_PATTERN.finditer(text)]
    weathers = [m.group(0) for m in WEATHER_PATTERN.finditer(text)]
    
    # Rule 1: Equipment/Relay located at Substation
    for ps in substations:
        for eq in equips:
            results.append({
                "doc_id": doc_id,
                "subject": eq.strip(),
                "subject_type": "PowerEquipment",
                "predicate": "LOCATED_AT",
                "object": ps.strip(),
                "object_type": "Substation",
                "method": "rules_spacy_v1.0",
                "confidence": 0.88,
                "evidence_quote": f"{eq} ... {ps}"
            })
        for rl in relays:
            results.append({
                "doc_id": doc_id,
                "subject": rl.strip(),
                "subject_type": "ProtectionRelay",
                "predicate": "LOCATED_AT",
                "object": ps.strip(),
                "method": "rules_spacy_v1.0",
                "confidence": 0.85,
                "evidence_quote": f"{rl} ... {ps}"
            })

    # Rule 2: Line connected to Substation
    for ln in lines:
        for ps in substations:
            ps_clean = re.sub(r'ПС\s+(\d+\s*кВ\s+)?', '', ps).strip()
            if ps_clean.lower() in ln.lower():
                results.append({
                    "doc_id": doc_id,
                    "subject": ln.strip(),
                    "subject_type": "TransmissionLine",
                    "predicate": "CONNECTED_TO",
                    "object": ps.strip(),
                    "method": "rules_spacy_v1.0",
                    "confidence": 0.95,
                    "evidence_quote": f"{ln} -> {ps}"
                })

    # Rule 3: Operates at Voltage
    for ln in lines:
        v_match = VOLT_PATTERN.search(ln)
        if v_match:
            results.append({
                "doc_id": doc_id,
                "subject": ln.strip(),
                "subject_type": "TransmissionLine",
                "predicate": "OPERATES_AT_VOLTAGE",
                "object": v_match.group(0).strip(),
                "object_type": "VoltageClass",
                "method": "rules_spacy_v1.0",
                "confidence": 0.98,
                "evidence_quote": ln
            })

    for ps in substations:
        v_match = VOLT_PATTERN.search(ps)
        if v_match:
            results.append({
                "doc_id": doc_id,
                "subject": ps.strip(),
                "subject_type": "Substation",
                "predicate": "OPERATES_AT_VOLTAGE",
                "object": v_match.group(0).strip(),
                "object_type": "VoltageClass",
                "method": "rules_spacy_v1.0",
                "confidence": 0.98,
                "evidence_quote": ps
            })

    # Rule 4: Fault triggered protection
    for flt in faults:
        for rl in relays:
            results.append({
                "doc_id": doc_id,
                "subject": flt.strip(),
                "subject_type": "FaultType",
                "predicate": "TRIGGERED_PROTECTION",
                "object": rl.strip(),
                "object_type": "ProtectionRelay",
                "method": "rules_spacy_v1.0",
                "confidence": 0.90,
                "evidence_quote": f"{flt} ... {rl}"
            })

    # Rule 5: Fault caused by weather
    for flt in faults:
        for w in weathers:
            results.append({
                "doc_id": doc_id,
                "subject": flt.strip(),
                "subject_type": "FaultType",
                "predicate": "CAUSED_BY_WEATHER",
                "object": w.strip(),
                "object_type": "WeatherPhenomenon",
                "method": "rules_spacy_v1.0",
                "confidence": 0.92,
                "evidence_quote": f"{flt} ... {w}"
            })

    return results

def run_extraction():
    docs_file = os.path.join(DATA_DIR, "raw_documents.jsonl")
    all_extractions = []
    with open(docs_file, "r", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            exts = extract_entities_and_relations(doc["text"], doc["doc_id"])
            all_extractions.extend(exts)
            
    out_file = os.path.join(DATA_DIR, "extractions_rules.jsonl")
    with open(out_file, "w", encoding="utf-8") as f:
        for item in all_extractions:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
    print(f"[Rules Extractor] Extracted {len(all_extractions)} relations from {len(open(docs_file, 'r', encoding='utf-8').readlines())} documents.")

if __name__ == "__main__":
    run_extraction()
