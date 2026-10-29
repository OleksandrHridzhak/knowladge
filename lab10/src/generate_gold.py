"""
Генератор золотого набору запитів (eval/gold.jsonl) для оцінювання семантичного пошуку
ЛР 10, Результат 5.
Студент: Гріджак Олександр (ФЕІ-43)
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EVAL_DIR = BASE_DIR / "eval"
EVAL_DIR.mkdir(parents=True, exist_ok=True)

def c_id(doc_num: int, sec_num: int) -> str:
    """Повертає точний chunk_id для doc_num (1..25) та sec_num (1..9)."""
    idx = (doc_num - 1) * 9 + sec_num
    return f"CHK-{idx:04d}"

GOLD_QUERIES = [
    # --- 15 KEYWORD QUERIES ---
    {
        "query_id": "KW-01",
        "query": "SEL-421 термінал релейного захисту та дистанційного захисту ПЛ 750 кВ",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(8, 1), c_id(8, 2), c_id(8, 3)]
    },
    {
        "query_id": "KW-02",
        "query": "Автотрансформатор 3хАОДЦТН-333000/750/330 технічні параметри",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(6, 1), c_id(6, 2), c_id(6, 3)]
    },
    {
        "query_id": "KW-03",
        "query": "Підстанція 750 кВ Західноукраїнська склад обладнання РУ",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(5, 1), c_id(5, 2), c_id(5, 3)]
    },
    {
        "query_id": "KW-04",
        "query": "OHL-750-ZU-VIN характеристики лінії та розщеплена фаза",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(7, 1), c_id(7, 2), c_id(7, 3)]
    },
    {
        "query_id": "KW-05",
        "query": "Кодекс системи передачі генератори типу D вимоги FRT",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(1, 1), c_id(1, 2), c_id(1, 3)]
    },
    {
        "query_id": "KW-06",
        "query": "MicroSCADA Pro протоколи зв'язку IEC 60870-5-104 ICCP TASE.2",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(9, 1), c_id(9, 2), c_id(9, 3)]
    },
    {
        "query_id": "KW-07",
        "query": "АЧР-I та АЧР-II уставки частоти та часові витримки",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(12, 1), c_id(12, 2), c_id(12, 3)]
    },
    {
        "query_id": "KW-08",
        "query": "Black Start підняття системи від Дністровської ГЕС регламент",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(14, 1), c_id(14, 2), c_id(14, 3)]
    },
    {
        "query_id": "KW-09",
        "query": "Хроматографічний аналіз розчинених газів DGA критерій Дюваля",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(25, 1), c_id(25, 2), c_id(25, 3)]
    },
    {
        "query_id": "KW-10",
        "query": "Інтерконектор 750 кВ Хмельницька АЕС Жешув Польща ENTSO-E",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(15, 1), c_id(15, 2), c_id(15, 3)]
    },
    {
        "query_id": "KW-11",
        "query": "Векторні вимірювачі PMU стандарт IEEE C37.118 протокол WAMS",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(19, 1), c_id(19, 2), c_id(19, 3)]
    },
    {
        "query_id": "KW-12",
        "query": "Стандарт IEC 61850 шина процесу Process Bus GOOSE та Sampled Values SV",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(21, 1), c_id(21, 2), c_id(21, 3)]
    },
    {
        "query_id": "KW-13",
        "query": "Dynamic Line Rating DLR датчики температури проводу та провисання",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(22, 1), c_id(22, 2), c_id(22, 3)]
    },
    {
        "query_id": "KW-14",
        "query": "Критерій статичної та динамічної стійкості N-1 та N-2 перевантаження",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(23, 1), c_id(23, 2), c_id(23, 3)]
    },
    {
        "query_id": "KW-15",
        "query": "Кібербезпека АСУ ТП сегментація мережі DMZ фаєрвол SCADA",
        "type": "keyword",
        "relevant_chunk_ids": [c_id(20, 1), c_id(20, 2), c_id(20, 3)]
    },

    # --- 15 PARAPHRASE QUERIES ---
    {
        "query_id": "PP-01",
        "query": "Як налаштовуються пристрої швидкої ліквідації міжфазних коротких замикань на надвисокій напрузі?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(8, 1), c_id(8, 2), c_id(8, 4)]
    },
    {
        "query_id": "PP-02",
        "query": "Яка конструктивна будова та охолодження використовується у велетенських силових перетворювачах 750 кВ?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(6, 1), c_id(6, 2), c_id(6, 6)]
    },
    {
        "query_id": "PP-03",
        "query": "Як саме забезпечується збереження генерації в мережі під час раптових глибоких просідань напруги?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(1, 2), c_id(1, 3), c_id(1, 4)]
    },
    {
        "query_id": "PP-04",
        "query": "Які кроки здійснює диспетчерська служба для збереження єдності синхронної зони при загрозі системної аварії?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(2, 1), c_id(2, 2), c_id(2, 5)]
    },
    {
        "query_id": "PP-05",
        "query": "Механізм автоматичного скидання споживачів для недопущення лавини зниження частоти нижче критичної позначки",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(12, 1), c_id(12, 2), c_id(12, 5)]
    },
    {
        "query_id": "PP-06",
        "query": "Як діагностують внутрішній стан ізоляційного масла силових агрегатів без їхнього вимкнення та розбирання?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(25, 1), c_id(25, 2), c_id(25, 5)]
    },
    {
        "query_id": "PP-07",
        "query": "Особливості експорту та транзиту надлишкової потужності вітчизняних атомних станцій до європейських сусідів",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(15, 1), c_id(15, 2), c_id(15, 4)]
    },
    {
        "query_id": "PP-08",
        "query": "Як оператор відстежує геометрію та коливання фаз синусоїди струму по всій країні з прив'язкою до атомного годинника?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(19, 1), c_id(19, 2), c_id(19, 5)]
    },
    {
        "query_id": "PP-09",
        "query": "Заходи захисту комп'ютерних серверів та пультів управління енергетичними об'єктами від зовнішніх мережевих вторгнень",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(20, 1), c_id(20, 2), c_id(20, 5)]
    },
    {
        "query_id": "PP-10",
        "query": "Як погода та сила вітру допомагають тимчасово передавати лінією більше струму без ризику перепалу дротів?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(22, 1), c_id(22, 2), c_id(22, 4)]
    },
    {
        "query_id": "PP-11",
        "query": "Яка черговість запуску гідроагрегатів для подачі напруги на власні потреби теплових станцій після повного знеструмлення?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(14, 1), c_id(14, 2), c_id(14, 4)]
    },
    {
        "query_id": "PP-12",
        "query": "Як розраховується баланс активних потужностей для мінімізації загальних технічних втрат у дротах магістралі?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(24, 1), c_id(24, 2), c_id(24, 4)]
    },
    {
        "query_id": "PP-13",
        "query": "Які споживачі гарантовано залишаються підключеними при запровадженні екстрених обмежень навантаження?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(17, 1), c_id(17, 2), c_id(17, 3)]
    },
    {
        "query_id": "PP-14",
        "query": "Відмова від мідних контрольних кабелів на користь оптичних пакетних потоків всередині розподільчих установок",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(21, 1), c_id(21, 2), c_id(21, 3)]
    },
    {
        "query_id": "PP-15",
        "query": "Які показники спотворення синусоїди напруги вважаються допустимими згідно з чинними галузевими нормами?",
        "type": "paraphrase",
        "relevant_chunk_ids": [c_id(18, 1), c_id(18, 2), c_id(18, 3)]
    },

    # --- 10 MULTI-HOP QUERIES ---
    {
        "query_id": "MH-01",
        "query": "Як узгоджуються дії автоматики розвантаження АЧР із роботою захистів ліній SEL-421 при аварійному відключенні блоку АЕС?",
        "type": "multi_hop",
        "relevant_chunk_ids": [c_id(12, 2), c_id(8, 2), c_id(15, 3)]
    },
    {
        "query_id": "MH-02",
        "query": "Яка послідовність дій диспетчера при отриманні сигналу тривоги DGA з трансформатора ПС Західноукраїнська та переведення навантаження на резервну фазу?",
        "type": "multi_hop",
        "relevant_chunk_ids": [c_id(25, 3), c_id(5, 2), c_id(6, 3)]
    },
    {
        "query_id": "MH-03",
        "query": "Вплив впровадження Dynamic Line Rating на транзитну спроможність інтерконектора з ENTSO-E та виконання критерію надійності N-1",
        "type": "multi_hop",
        "relevant_chunk_ids": [c_id(22, 2), c_id(4, 2), c_id(23, 2)]
    },
    {
        "query_id": "MH-04",
        "query": "Спільне використання даних WAMS PMU та алгоритмів SCADA для виявлення та запобігання міжсистемним низькочастотним коливанням",
        "type": "multi_hop",
        "relevant_chunk_ids": [c_id(19, 3), c_id(9, 2), c_id(10, 2)]
    },
    {
        "query_id": "MH-05",
        "query": "Перехід цифрової підстанції IEC 61850 на протиаварійне живлення від ГЕС у рамках сценарію розгортання Black Start",
        "type": "multi_hop",
        "relevant_chunk_ids": [c_id(21, 4), c_id(14, 2), c_id(14, 3)]
    },
    {
        "query_id": "MH-06",
        "query": "Координація між відключеннями споживачів за графіками ГАВ та вимогами Кодексу системи передачі щодо допустимих меж частоти 49.5-50.5 Гц",
        "type": "multi_hop",
        "relevant_chunk_ids": [c_id(11, 2), c_id(17, 2), c_id(1, 2)]
    },
    {
        "query_id": "MH-07",
        "query": "Вплив гармонічних спотворень від вставок постійного струму на показники якості електроенергії ДСТУ EN 50160 та нагрів обмоток автотрансформаторів",
        "type": "multi_hop",
        "relevant_chunk_ids": [c_id(16, 3), c_id(18, 2), c_id(6, 4)]
    },
    {
        "query_id": "MH-08",
        "query": "Оптимізація перетоків OPF з урахуванням температурних обмежень дротів DLR та вимог резервів первинного регулювання FCR",
        "type": "multi_hop",
        "relevant_chunk_ids": [c_id(24, 2), c_id(22, 3), c_id(3, 2)]
    },
    {
        "query_id": "MH-09",
        "query": "Забезпечення кіберзахисту шлюзів зв'язку IEC 60870-5-104 у терміналах релейного захисту та SCADA-контролерах опорних підстанцій",
        "type": "multi_hop",
        "relevant_chunk_ids": [c_id(20, 2), c_id(9, 3), c_id(8, 4)]
    },
    {
        "query_id": "MH-10",
        "query": "Розподіл обов'язків балансування між пиловугільними блоками ТЕС та маневровими гідроелектростанціями при дотриманні положень технічної угоди ENTSO-E",
        "type": "multi_hop",
        "relevant_chunk_ids": [c_id(13, 2), c_id(3, 3), c_id(4, 3)]
    },

    # --- 5 UNANSWERABLE QUERIES ---
    {
        "query_id": "UN-01",
        "query": "Яка середня вартість тонни збагаченого урану U3O8 на Лондонській товарній біржі за підсумками першого кварталу 2026 року?",
        "type": "unanswerable",
        "relevant_chunk_ids": []
    },
    {
        "query_id": "UN-02",
        "query": "Як налаштувати маршрутизацію BGP confederation на прикордонному маршрутизаторі Cisco ASR 9000 для глобального інтернет-провайдера?",
        "type": "unanswerable",
        "relevant_chunk_ids": []
    },
    {
        "query_id": "UN-03",
        "query": "Хімічний склад та технологія виробництва катодних матеріалів для літій-залізо-фосфатних акумуляторів LiFePO4 фірми CATL",
        "type": "unanswerable",
        "relevant_chunk_ids": []
    },
    {
        "query_id": "UN-04",
        "query": "Правила дорожнього руху для великовагових вантажівок у Республіці Польща при перетині прикордонних автошляхів",
        "type": "unanswerable",
        "relevant_chunk_ids": []
    },
    {
        "query_id": "UN-05",
        "query": "Архітектура та квантові алгоритми обчислення факторизації великих чисел Шора на процесорах IBM Eagle",
        "type": "unanswerable",
        "relevant_chunk_ids": []
    }
]

def main():
    out_file = EVAL_DIR / "gold.jsonl"
    with open(out_file, "w", encoding="utf-8") as f:
        for q in GOLD_QUERIES:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")
            
    print(f"[SUCCESS] Згенеровано {len(GOLD_QUERIES)} запитів у {out_file} з точними CHK-xxxx ID.")

if __name__ == "__main__":
    main()
