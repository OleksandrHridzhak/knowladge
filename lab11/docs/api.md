# Документація REST API: PowerGrid Hybrid RAG (Результат 3)

## 1. Загальний огляд
REST API розроблено на базі фреймворку **FastAPI** для забезпечення виробничої інтеграції гібридного конвеєра RAG та графа знань диспетчерського управління.
- **Базовий URL:** `http://127.0.0.1:8000`
- **Інтерактивна документація Swagger UI:** `http://127.0.0.1:8000/docs`
- **Специфікація OpenAPI JSON:** `http://127.0.0.1:8000/openapi.json`

## 2. Автентифікація та матриця ролей
Автентифікація реалізована через заголовок `X-API-Key` або `Authorization: Bearer <token>`.

| Роль | API-Ключ | Рівень доступу | Ліміт запитів (Rate Limit) |
|:---|:---|:---|:---:|
| **analyst** | `key-analyst-12345` | Лише відкрита документація (`public`) | 10 запитів / хв |
| **engineer** | `key-engineer-67890` | Повний доступ (`public` + `restricted` РЗА) | 30 запитів / хв |

## 3. Специфікація ендпоінтів

### 3.1. Перевірка працездатності: `GET /health`
Повертає стан індексів, завантажену кількість чанків і топологічних вузлів.
```bash
curl -X GET "http://127.0.0.1:8000/health"
```
**Відповідь `200 OK`:**
```json
{
  "status": "operational",
  "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
  "corpus_chunks": 225,
  "graph_nodes": 146,
  "graph_relationships": 280,
  "uptime_seconds": 14.28
}
```

---

### 3.2. Інженерний запит до RAG: `POST /ask`
Приймає текст запиту, параметри пошуку та повертає вивірену відповідь із цитатами.
```bash
curl -X POST "http://127.0.0.1:8000/ask" \
     -H "X-API-Key: key-engineer-67890" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Які уставки та протоколи зв'язку терміналу SEL-421 на ПЛ 750 кВ?",
       "include_graph": true,
       "top_k": 3
     }'
```
**Відповідь `200 OK`:**
```json
{
  "query": "Які уставки та протоколи зв'язку терміналу SEL-421 на ПЛ 750 кВ?",
  "role": "engineer",
  "answer": "Згідно з нормативним документом «Системи релейного захисту...» [CHK-0057]: Телеметричні параметри... Графова перевірка підтверджує топологічний зв'язок: [NODE-RP_SEL421_Zakhidna] ==[PROTECTS]==> [NODE-SS_Zakhidna].",
  "citations": ["CHK-0057"],
  "citations_valid": true,
  "retrieved_sources": [
    {
      "chunk_id": "CHK-0057",
      "doc_id": "DOC-07",
      "title": "Системи релейного захисту (РЗА)",
      "section": "Взаємодія з диспетчерським центром SCADA",
      "sensitivity": "public",
      "score": 0.0318
    }
  ],
  "graph_entities_linked": ["RP_SEL421_Zakhidna", "SS_Zakhidna"],
  "latency_ms": 42.15,
  "timestamp": "2026-11-01T13:46:00Z"
}
```

---

### 3.3. Отримання джерела за ID: `GET /sources/{chunk_id}`
Повертає детальний зміст фрагмента з перевіркою рівня конфіденційності.
```bash
# Запит від аналітика на закритий документ:
curl -X GET "http://127.0.0.1:8000/sources/CHK-0007" \
     -H "X-API-Key: key-analyst-12345"
```
**Відповідь `403 Forbidden`:**
```json
{
  "detail": "Доступ заборонено: даний документ містить обмежені уставки РЗА та вимагає ролі 'engineer'."
}
```

---

## 4. Коди відповідей та обробка помилок
- `200 OK`: Успішне виконання запиту.
- `401 Unauthorized`: Відсутній або невалідний токен/API-ключ.
- `403 Forbidden`: Спроба доступу до документів з грифом `restricted` без відповідних повноважень.
- `404 Not Found`: Запитаний `chunk_id` відсутній в індексі.
- `422 Unprocessable Entity`: Помилка валідації Pydantic (закороткий або некоректний запит).
- `429 Too Many Requests`: Перевищення ліміту запитів на хвилину (Rate Limit).

