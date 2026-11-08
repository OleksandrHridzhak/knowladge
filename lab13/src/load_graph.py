"""
Result 5: Entity Normalization (>= 20 entities) and Graph Loading with Provenance.
"""
import os
import json
import networkx as nx

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# Normalization dictionary for >= 20 entities
ENTITY_NORMALIZATION = {
    # Substations
    "ПС 750 кВ Західноукраїнська": "SUBSTATION:ZACHIDNOUKRAINSKA_750",
    "ПС 750 кВ Вінницька": "SUBSTATION:VINNYTSKA_750",
    "ПС 750 кВ Київська": "SUBSTATION:KYIVSKA_750",
    "ПС 330 кВ Рівне": "SUBSTATION:RIVNE_330",
    "ПС 330 кВ Тернопільська": "SUBSTATION:TERNOPILSKA_330",
    
    # Transmission Lines
    "ПЛ 750 кВ Західноукраїнська - Вінницька": "LINE:ZU_VIN_750",
    "ПЛ 750 кВ Вінницька - Дніпровська": "LINE:VIN_DNIPRO_750",
    "ПЛ 750 кВ ХАЕС - Західноукраїнська": "LINE:KHAES_ZU_750",
    "ПЛ 330 кВ Рівне - Луцьк": "LINE:RIVNE_LUTSK_330",
    "ПЛ 330 кВ Тернопіль - Хмельницька": "LINE:TERNOPIL_KHMEL_330",
    "ПЛ 330 кВ Західноукраїнська - Богородчани": "LINE:ZU_BOGOROD_330",
    "ПЛ 330 кВ Вінницька - Чернівці": "LINE:VIN_CHERNIVTSI_330",
    "ПЛ 330 кВ Тернопільська - Чернівецька": "LINE:TERNOPIL_CHERNIV_330",
    
    # Equipment
    "автотрансформатор АТ-1": "EQUIP:AT_1",
    "автотрансформатор АТ-2": "EQUIP:AT_2",
    "вимикач В-750": "EQUIP:CB_750",
    "вимикач В-330": "EQUIP:CB_330",
    "трансформатор струму ТФЗМ-330": "EQUIP:CT_TFZM_330",
    "дугогасний реактор РЗДСО-330": "EQUIP:REACTOR_RZDSO_330",
    "шунтуючий реактор ШР-750": "EQUIP:REACTOR_SHR_750",
    "роз'єднувач РНД-330": "EQUIP:DISC_RND_330",
    "грозозахисний трос": "EQUIP:SHIELD_WIRE",
    "грозозахисний трос OPGW": "EQUIP:OPGW_WIRE",
    
    # Protection Relays
    "диференційно-фазний захист ДФЗ-504": "RELAY:DFZ_504",
    "термінал SEL-421": "RELAY:SEL_421",
    "диференційний захист шин ДЗШ": "RELAY:DZSH",
    "газовий захист РГТ-80": "RELAY:RGT_80",
    "лінійний захист REL-670": "RELAY:REL_670",
    "захист від перевантаження РТ-40": "RELAY:RT_40",
    "струмовий захист МТЗ": "RELAY:MTZ",
    "диференційний захист ДЗТ-11": "RELAY:DZT_11",
    "пристрій резервування УРОВ": "RELAY:UROV"
}

def normalize_entity(ent):
    clean = ent.strip()
    for raw, canonical in ENTITY_NORMALIZATION.items():
        if raw.lower() == clean.lower() or raw.lower() in clean.lower():
            return canonical
    return f"ENTITY:{clean.upper().replace(' ', '_')}"

def build_knowledge_graph():
    G = nx.MultiDiGraph()
    
    # Load LLM validated extractions with provenance
    ext_file = os.path.join(DATA_DIR, "extractions_llm.jsonl")
    loaded_triples = 0
    with open(ext_file, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            s_norm = normalize_entity(rec["subject"])
            o_norm = normalize_entity(rec["object"])
            pred = rec["predicate"]
            
            G.add_node(s_norm, label=rec["subject_type"], raw_name=rec["subject"])
            G.add_node(o_norm, label=rec["object_type"], raw_name=rec["object"])
            
            G.add_edge(
                s_norm, o_norm,
                relation=pred,
                doc_id=rec["doc_id"],
                evidence_quote=rec["evidence_quote"],
                extractor="gemini-2.5-pro_schema_v2.1",
                timestamp=rec.get("extraction_timestamp")
            )
            loaded_triples += 1
            
    print(f"[Graph Builder] Loaded knowledge graph with {G.number_of_nodes()} unique entities and {G.number_of_edges()} triples with full provenance.")
    
    # Export graph stats
    graph_stats = {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "normalized_entities_count": len(ENTITY_NORMALIZATION),
        "density": round(nx.density(G), 5)
    }
    with open(os.path.join(DATA_DIR, "graph_stats.json"), "w", encoding="utf-8") as f:
        json.dump(graph_stats, f, indent=2)
        
    return G

if __name__ == "__main__":
    build_knowledge_graph()
