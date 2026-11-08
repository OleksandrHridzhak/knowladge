# Agent graph execution engine with verification
import json

MOCK_TOPOLOGY = {
    "substations": [
        {"id": "PS_ZAHID", "name": "ПС 750 кВ Західноукраїнська", "voltage": 750, "lines": ["L_ZAHID_VIN", "L_ZAHID_RIVNE"]},
        {"id": "PS_VIN", "name": "ПС 750 кВ Вінницька", "voltage": 750, "lines": ["L_ZAHID_VIN", "L_VIN_KYIV"]},
        {"id": "PS_KYIV", "name": "ПС 750 кВ Київська", "voltage": 750, "lines": ["L_VIN_KYIV", "L_KYIV_RIVNE"]},
        {"id": "PS_RIVNE", "name": "ПС 330 кВ Рівне", "voltage": 330, "lines": ["L_ZAHID_RIVNE", "L_KYIV_RIVNE"]}
    ],
    "transformers": [
        {"id": "AT_1", "substation": "PS_VIN", "type": "3xАОДЦТН-333000", "rating_mva": 1000, "status": "OPERATIONAL"}
    ],
    "regulations": [
        {"doc_id": "REG-01", "section": "3.2", "title": "Уставки ДФЗ-504", "content": "Струм спрацювання ДФЗ-504 на ПЛ 750 кВ складає 2100 А (ревізія 2025 р.)", "score": 0.94},
        {"doc_id": "REG-02", "section": "5.1", "title": "Режим Black Start", "content": "Дністровська ГАЕС забезпечує первинну подачу напруги на ПС Вінницька за 15 хвилин", "score": 0.89},
        {"doc_id": "REG-03", "section": "8.4", "title": "Клас напруги лінії", "content": "ПЛ Західноукраїнська - Вінницька експлуатується на напрузі 750 кВ", "score": 0.96}
    ],
    "telemetry": [
        {"line_id": "L_ZAHID_VIN", "current_a": 1650, "p_mw": 1780, "q_mvar": 120, "temp_c": 38.5},
        {"line_id": "L_VIN_KYIV", "current_a": 1420, "p_mw": 1510, "q_mvar": 95, "temp_c": 35.0}
    ]
}

def tool_graph_cypher_query(query):
    forbidden = ["CREATE", "DELETE", "SET", "MERGE", "DROP", "ALTER", "REMOVE"]
    if any(w in query.upper() for w in forbidden):
        return {"error": "SECURITY_VIOLATION: Mutating Cypher commands are prohibited in read-only mode"}
    if "Substation" in query or "substations" in query:
        return {"result": MOCK_TOPOLOGY["substations"], "count": len(MOCK_TOPOLOGY["substations"])}
    if "Transformer" in query:
        return {"result": MOCK_TOPOLOGY["transformers"], "count": len(MOCK_TOPOLOGY["transformers"])}
    return {"result": [], "count": 0}

def tool_vector_semantic_search(prompt, top_k=5, min_score=0.70):
    p_lower = prompt.lower()
    matches = []
    for r in MOCK_TOPOLOGY["regulations"]:
        if any(w in r["content"].lower() or w in r["title"].lower() for w in p_lower.split()):
            if r["score"] >= min_score:
                matches.append(r)
    return {"matches": matches[:top_k], "total": len(matches)}

def tool_sql_metrics_query(sql):
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "ATTACH"]
    if any(w in sql.upper() for w in forbidden):
        return {"error": "SECURITY_VIOLATION: Write SQL commands are strictly prohibited"}
    if "telemetry" in sql.lower():
        return {"rows": MOCK_TOPOLOGY["telemetry"], "count": len(MOCK_TOPOLOGY["telemetry"])}
    return {"rows": [], "count": 0}

class PowerGridAgent:
    def __init__(self):
        self.max_steps = 6
        self.trace_log = []

    def run(self, user_query):
        steps = []
        steps.append({"step": 1, "action": "plan", "thought": f"Аналіз запиту: {user_query}. Визначення джерел."})
        
        if "уставк" in user_query.lower() or "дфз" in user_query.lower() or "black start" in user_query.lower():
            tool_res = tool_vector_semantic_search(user_query)
            steps.append({"step": 2, "action": "vector_semantic_search", "result": tool_res})
        elif "струм" in user_query.lower() or "потужність" in user_query.lower() or "навантаження" in user_query.lower():
            tool_res = tool_sql_metrics_query("SELECT * FROM telemetry WHERE line_id='L_ZAHID_VIN'")
            steps.append({"step": 2, "action": "sql_metrics_query", "result": tool_res})
        elif "підстанц" in user_query.lower() or "ліні" in user_query.lower():
            tool_res = tool_graph_cypher_query("MATCH (s:Substation) RETURN s")
            steps.append({"step": 2, "action": "graph_cypher_query", "result": tool_res})
        else:
            steps.append({"step": 2, "action": "lookup", "result": {"matches": []}})

        citations = []
        has_verified_data = False
        for s in steps:
            if "result" in s:
                r = s["result"]
                if "matches" in r and r["matches"]:
                    citations.extend([f"[{m['doc_id']}:{m['section']}]" for m in r["matches"]])
                    has_verified_data = True
                elif "rows" in r and r["rows"]:
                    citations.append("[SQL:telemetry]")
                    has_verified_data = True
                elif "result" in r and r["result"]:
                    citations.append("[Graph:topology]")
                    has_verified_data = True

        steps.append({"step": 3, "action": "verify_citations", "citations": citations, "status": "VERIFIED" if has_verified_data else "NO_DATA"})

        if not has_verified_data:
            answer = "У доступних сховищах даних ОЕС України немає інформації за цим запитом. Зверніться до головного диспетчера."
            status = "UNKNOWN"
        else:
            answer = f"Запит успішно оброблено. Отримано дані з підтверджених джерел {', '.join(citations)}."
            status = "SUCCESS"

        steps.append({"step": 4, "action": "draft_response", "answer": answer, "status": status})
        trace = {"query": user_query, "steps": steps, "status": status, "step_count": len(steps)}
        self.trace_log.append(trace)
        return trace