# -*- coding: utf-8 -*-
"""
Генерація топологічних даних енергосистеми України для Neo4j.
Формує CSV-файли вузлів (nodes.csv) та зв'язків (relationships.csv)
з обов'язковими атрибутами походження (source, confidence, validFrom).

Критерії методички (Результат 2):
 - >= 100 вузлів (згенеровано 146)
 - >= 200 зв'язків (згенеровано 280)
"""

import os
import csv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 1. Вузли (Nodes) - 146 сутностей
nodes = [
    # Operator (1)
    {"id": "Operator_Ukrenergo", "label": "Operator", "name": "НЕК Укренерго", "type": "TSO", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "Київ", "riskScore": ""},

    # PowerPlants (12)
    {"id": "DniproHPP", "label": "PowerPlant", "name": "Дніпровська ГЕС", "type": "Hydro", "voltageKV": "330.0", "capacityMW": "1569.0", "operational": "true", "location": "Запоріжжя", "riskScore": ""},
    {"id": "DniesterHPP", "label": "PowerPlant", "name": "Дністровська ГЕС", "type": "Hydro", "voltageKV": "330.0", "capacityMW": "702.0", "operational": "true", "location": "Новодністровськ", "riskScore": ""},
    {"id": "DnistrovskaPSPP", "label": "PowerPlant", "name": "Дністровська ГАЕС", "type": "PumpedStorage", "voltageKV": "330.0", "capacityMW": "972.0", "operational": "true", "location": "Сокиряни", "riskScore": ""},
    {"id": "TrypilskaTPP", "label": "PowerPlant", "name": "Трипільська ТЕС", "type": "Thermal", "voltageKV": "330.0", "capacityMW": "1800.0", "operational": "true", "location": "Українка", "riskScore": ""},
    {"id": "BurshtynTPP", "label": "PowerPlant", "name": "Бурштинська ТЕС", "type": "Thermal", "voltageKV": "400.0", "capacityMW": "2300.0", "operational": "true", "location": "Бурштин", "riskScore": ""},
    {"id": "KryvorizkaTPP", "label": "PowerPlant", "name": "Криворізька ТЕС", "type": "Thermal", "voltageKV": "330.0", "capacityMW": "2000.0", "operational": "true", "location": "Зеленодольськ", "riskScore": ""},
    {"id": "LadyzhynskaTPP", "label": "PowerPlant", "name": "Ладижинська ТЕС", "type": "Thermal", "voltageKV": "330.0", "capacityMW": "1800.0", "operational": "true", "location": "Ладижин", "riskScore": ""},
    {"id": "RivneNPP", "label": "PowerPlant", "name": "Рівненська АЕС", "type": "Nuclear", "voltageKV": "750.0", "capacityMW": "2835.0", "operational": "true", "location": "Вараш", "riskScore": ""},
    {"id": "KhmelnytskyiNPP", "label": "PowerPlant", "name": "Хмельницька АЕС", "type": "Nuclear", "voltageKV": "750.0", "capacityMW": "2000.0", "operational": "true", "location": "Нетішин", "riskScore": ""},
    {"id": "SouthUkraineNPP", "label": "PowerPlant", "name": "Південноукраїнська АЕС", "type": "Nuclear", "voltageKV": "750.0", "capacityMW": "3000.0", "operational": "true", "location": "Південноукраїнськ", "riskScore": ""},
    {"id": "PokrovskaSES", "label": "PowerPlant", "name": "Покровська СЕС", "type": "Solar", "voltageKV": "110.0", "capacityMW": "240.0", "operational": "true", "location": "Покров", "riskScore": ""},
    {"id": "BotievoVES", "label": "PowerPlant", "name": "Ботієвська ВЕС", "type": "Wind", "voltageKV": "150.0", "capacityMW": "200.0", "operational": "true", "location": "Приморськ", "riskScore": ""},

    # Substations 750 kV, 330 kV, 110 kV (25)
    {"id": "SS_Zakhidna", "label": "Substation", "name": "ПС 750 кВ Західноукраїнська", "type": "TransmissionSubstation", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "Стрийський район", "riskScore": ""},
    {"id": "SS_Kyivska", "label": "Substation", "name": "ПС 750 кВ Київська", "type": "TransmissionSubstation", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "Макарівський район", "riskScore": ""},
    {"id": "SS_Vinnytska", "label": "Substation", "name": "ПС 750 кВ Вінницька", "type": "TransmissionSubstation", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "Вінницький район", "riskScore": ""},
    {"id": "SS_Dniprovska", "label": "Substation", "name": "ПС 750 кВ Дніпровська", "type": "TransmissionSubstation", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "Дніпровський район", "riskScore": ""},
    {"id": "SS_Pivnichna", "label": "Substation", "name": "ПС 750 кВ Північноукраїнська", "type": "TransmissionSubstation", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "Сумська область", "riskScore": ""},
    {"id": "SS_Donbaska", "label": "Substation", "name": "ПС 750 кВ Донбаська", "type": "TransmissionSubstation", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "Бахмутський район", "riskScore": ""},

    {"id": "SS_Lviv2", "label": "Substation", "name": "ПС 330 кВ Львів-2", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Львів", "riskScore": ""},
    {"id": "SS_Rivne330", "label": "Substation", "name": "ПС 330 кВ Рівне", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Рівне", "riskScore": ""},
    {"id": "SS_Ternopilska", "label": "Substation", "name": "ПС 330 кВ Тернопільська", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Тернопіль", "riskScore": ""},
    {"id": "SS_IvanoFrankivska", "label": "Substation", "name": "ПС 330 кВ Івано-Франківська", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Івано-Франківськ", "riskScore": ""},
    {"id": "SS_Zhytomyrska", "label": "Substation", "name": "ПС 330 кВ Житомирська", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Житомир", "riskScore": ""},
    {"id": "SS_Cherkaska", "label": "Substation", "name": "ПС 330 кВ Черкаська", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Черкаси", "riskScore": ""},
    {"id": "SS_Poltavska", "label": "Substation", "name": "ПС 330 кВ Полтавська", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Полтава", "riskScore": ""},
    {"id": "SS_Kryvorizka", "label": "Substation", "name": "ПС 330 кВ Криворізька", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Кривий Ріг", "riskScore": ""},
    {"id": "SS_Zaporizka", "label": "Substation", "name": "ПС 330 кВ Запорізька", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Запоріжжя", "riskScore": ""},
    {"id": "SS_Odeska", "label": "Substation", "name": "ПС 330 кВ Усатове-Одеса", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Одеса", "riskScore": ""},
    {"id": "SS_Mykolaivska", "label": "Substation", "name": "ПС 330 кВ Миколаївська", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Миколаїв", "riskScore": ""},
    {"id": "SS_Khmelnytska", "label": "Substation", "name": "ПС 330 кВ Хмельницька", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Хмельницький", "riskScore": ""},
    {"id": "SS_Chernivtsi", "label": "Substation", "name": "ПС 330 кВ Чернівецька", "type": "DistributionSubstation", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Чернівці", "riskScore": ""},

    {"id": "SS_LvivKnyazhyi", "label": "Substation", "name": "ПС 110 кВ Княжий Львів", "type": "DistributionSubstation", "voltageKV": "110.0", "capacityMW": "", "operational": "true", "location": "Львів-Центр", "riskScore": ""},
    {"id": "SS_Sykhiv", "label": "Substation", "name": "ПС 110 кВ Сихівська", "type": "DistributionSubstation", "voltageKV": "110.0", "capacityMW": "", "operational": "true", "location": "Львів-Сихів", "riskScore": ""},
    {"id": "SS_Brody", "label": "Substation", "name": "ПС 110 кВ Броди", "type": "DistributionSubstation", "voltageKV": "110.0", "capacityMW": "", "operational": "true", "location": "Броди", "riskScore": ""},
    {"id": "SS_Boryspil", "label": "Substation", "name": "ПС 110 кВ Бориспільська", "type": "DistributionSubstation", "voltageKV": "110.0", "capacityMW": "", "operational": "true", "location": "Бориспіль", "riskScore": ""},
    {"id": "SS_Brovary", "label": "Substation", "name": "ПС 110 кВ Броварська", "type": "DistributionSubstation", "voltageKV": "110.0", "capacityMW": "", "operational": "true", "location": "Бровари", "riskScore": ""},
    {"id": "SS_Fastiv", "label": "Substation", "name": "ПС 110 кВ Фастівська", "type": "DistributionSubstation", "voltageKV": "110.0", "capacityMW": "", "operational": "true", "location": "Фастів", "riskScore": ""},

    # TransmissionLines (30)
    {"id": "Line_750_Zakhidna_Kyiv", "label": "TransmissionLine", "name": "ПЛ 750 кВ Західноукраїнська — Київська", "type": "OverheadLine", "voltageKV": "750.0", "capacityMW": "2200.0", "operational": "true", "location": "Захід-Центр", "riskScore": ""},
    {"id": "Line_750_Zakhidna_Vinnytsia", "label": "TransmissionLine", "name": "ПЛ 750 кВ Західноукраїнська — Вінницька", "type": "OverheadLine", "voltageKV": "750.0", "capacityMW": "2150.0", "operational": "true", "location": "Захід-Поділля", "riskScore": ""},
    {"id": "Line_750_Vinnytsia_Kyiv", "label": "TransmissionLine", "name": "ПЛ 750 кВ Вінницька — Київська", "type": "OverheadLine", "voltageKV": "750.0", "capacityMW": "2100.0", "operational": "true", "location": "Поділля-Центр", "riskScore": ""},
    {"id": "Line_750_Kyiv_Pivnichna", "label": "TransmissionLine", "name": "ПЛ 750 кВ Київська — Північноукраїнська", "type": "OverheadLine", "voltageKV": "750.0", "capacityMW": "2050.0", "operational": "true", "location": "Центр-Північ", "riskScore": ""},
    {"id": "Line_750_Pivnichna_Dnipro", "label": "TransmissionLine", "name": "ПЛ 750 кВ Північноукраїнська — Дніпровська", "type": "OverheadLine", "voltageKV": "750.0", "capacityMW": "2250.0", "operational": "true", "location": "Північ-Схід", "riskScore": ""},
    {"id": "Line_750_Vinnytsia_Dnipro", "label": "TransmissionLine", "name": "ПЛ 750 кВ Вінницька — Дніпровська", "type": "OverheadLine", "voltageKV": "750.0", "capacityMW": "2180.0", "operational": "true", "location": "Поділля-Дніпро", "riskScore": ""},
    {"id": "Line_750_Khmelnytskyi_Kyiv", "label": "TransmissionLine", "name": "ПЛ 750 кВ ХАЕС — Київська", "type": "OverheadLine", "voltageKV": "750.0", "capacityMW": "2400.0", "operational": "true", "location": "ХАЕС-Київ", "riskScore": ""},
    {"id": "Line_750_Rivne_Kyiv", "label": "TransmissionLine", "name": "ПЛ 750 кВ РАЕС — Київська", "type": "OverheadLine", "voltageKV": "750.0", "capacityMW": "2400.0", "operational": "true", "location": "РАЕС-Київ", "riskScore": ""},
    {"id": "Line_750_SouthUkraine_Vinnytsia", "label": "TransmissionLine", "name": "ПЛ 750 кВ ПАЕС — Вінницька", "type": "OverheadLine", "voltageKV": "750.0", "capacityMW": "2500.0", "operational": "true", "location": "ПАЕС-Вінниця", "riskScore": ""},
    {"id": "Line_750_SouthUkraine_Dnipro", "label": "TransmissionLine", "name": "ПЛ 750 кВ ПАЕС — Дніпровська", "type": "OverheadLine", "voltageKV": "750.0", "capacityMW": "2450.0", "operational": "true", "location": "ПАЕС-Дніпро", "riskScore": ""},

    {"id": "Line_330_Zakhidna_Lviv2", "label": "TransmissionLine", "name": "ПЛ 330 кВ Західноукраїнська — Львів-2", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "520.0", "operational": "true", "location": "Львівщина", "riskScore": ""},
    {"id": "Line_330_Lviv2_Rivne", "label": "TransmissionLine", "name": "ПЛ 330 кВ Львів-2 — Рівне", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "500.0", "operational": "true", "location": "Львів-Рівне", "riskScore": ""},
    {"id": "Line_330_Lviv2_IvanoFrankivsk", "label": "TransmissionLine", "name": "ПЛ 330 кВ Львів-2 — Івано-Франківськ", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "480.0", "operational": "true", "location": "Прикарпаття", "riskScore": ""},
    {"id": "Line_330_Zakhidna_Ternopil", "label": "TransmissionLine", "name": "ПЛ 330 кВ Західноукраїнська — Тернопіль", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "490.0", "operational": "true", "location": "Галичина", "riskScore": ""},
    {"id": "Line_330_Ternopil_Khmelnytskyi", "label": "TransmissionLine", "name": "ПЛ 330 кВ Тернопіль — Хмельницька", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "470.0", "operational": "true", "location": "Поділля-Захід", "riskScore": ""},
    {"id": "Line_330_Dniester_Chernivtsi", "label": "TransmissionLine", "name": "ПЛ 330 кВ Дністровська ГЕС — Чернівці", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "510.0", "operational": "true", "location": "Буковина", "riskScore": ""},
    {"id": "Line_330_Chernivtsi_IvanoFrankivsk", "label": "TransmissionLine", "name": "ПЛ 330 кВ Чернівці — Івано-Франківськ", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "460.0", "operational": "true", "location": "Південний Захід", "riskScore": ""},
    {"id": "Line_330_Kyiv_Zhytomyr", "label": "TransmissionLine", "name": "ПЛ 330 кВ Київська — Житомирська", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "490.0", "operational": "true", "location": "Полісся", "riskScore": ""},
    {"id": "Line_330_Kyiv_Cherkasy", "label": "TransmissionLine", "name": "ПЛ 330 кВ Київська — Черкаська", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "480.0", "operational": "true", "location": "Наддніпрянщина", "riskScore": ""},
    {"id": "Line_330_Kyiv_Brovary", "label": "TransmissionLine", "name": "ПЛ 330 кВ Київська — Броварська", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "510.0", "operational": "true", "location": "Київщина", "riskScore": ""},
    {"id": "Line_330_Dnipro_Zaporizhia", "label": "TransmissionLine", "name": "ПЛ 330 кВ Дніпровська — Запорізька", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "620.0", "operational": "true", "location": "Подніпров'я", "riskScore": ""},
    {"id": "Line_330_Dnipro_KryvyiRih", "label": "TransmissionLine", "name": "ПЛ 330 кВ Дніпровська — Криворізька", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "590.0", "operational": "true", "location": "Кривбас", "riskScore": ""},
    {"id": "Line_330_Zaporizhia_DniproHPP", "label": "TransmissionLine", "name": "ПЛ 330 кВ Запорізька — Дніпровська ГЕС", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "650.0", "operational": "true", "location": "Запоріжжя", "riskScore": ""},
    {"id": "Line_330_SouthUkraine_Mykolaiv", "label": "TransmissionLine", "name": "ПЛ 330 кВ ПАЕС — Миколаївська", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "540.0", "operational": "true", "location": "Прибужжя", "riskScore": ""},
    {"id": "Line_330_Mykolaiv_Odesa", "label": "TransmissionLine", "name": "ПЛ 330 кВ Миколаївська — Одеська", "type": "OverheadLine", "voltageKV": "330.0", "capacityMW": "550.0", "operational": "true", "location": "Причорномор'я", "riskScore": ""},

    {"id": "Line_110_Lviv2_Knyazhyi", "label": "TransmissionLine", "name": "КЛ 110 кВ Львів-2 — Княжий", "type": "CableLine", "voltageKV": "110.0", "capacityMW": "85.0", "operational": "true", "location": "Львів-Кабель", "riskScore": ""},
    {"id": "Line_110_Lviv2_Sykhiv", "label": "TransmissionLine", "name": "КЛ 110 кВ Львів-2 — Сихів", "type": "CableLine", "voltageKV": "110.0", "capacityMW": "90.0", "operational": "true", "location": "Львів-Сихів-Кабель", "riskScore": ""},
    {"id": "Line_110_Zakhidna_Brody", "label": "TransmissionLine", "name": "ПЛ 110 кВ Західноукраїнська — Броди", "type": "OverheadLine", "voltageKV": "110.0", "capacityMW": "70.0", "operational": "true", "location": "Бродівщина", "riskScore": ""},
    {"id": "Line_110_Kyiv_Boryspil", "label": "TransmissionLine", "name": "КЛ 110 кВ Київська — Бориспіль", "type": "CableLine", "voltageKV": "110.0", "capacityMW": "95.0", "operational": "true", "location": "Бориспіль-Кабель", "riskScore": ""},
    {"id": "Line_110_Kyiv_Fastiv", "label": "TransmissionLine", "name": "ПЛ 110 кВ Київська — Фастів", "type": "OverheadLine", "voltageKV": "110.0", "capacityMW": "75.0", "operational": "true", "location": "Фастівщина", "riskScore": ""},

    # Transformers (17)
    {"id": "AT_Zakhidna_1", "label": "Transformer", "name": "Автотрансформатор АТ-1 750/330 кВ Західна", "type": "Autotransformer", "voltageKV": "750.0", "capacityMW": "1000.0", "operational": "true", "location": "ПС Західноукраїнська", "riskScore": ""},
    {"id": "AT_Zakhidna_2", "label": "Transformer", "name": "Автотрансформатор АТ-2 750/330 кВ Західна", "type": "Autotransformer", "voltageKV": "750.0", "capacityMW": "1000.0", "operational": "true", "location": "ПС Західноукраїнська", "riskScore": ""},
    {"id": "AT_Kyivska_1", "label": "Transformer", "name": "Автотрансформатор АТ-1 750/330 кВ Київська", "type": "Autotransformer", "voltageKV": "750.0", "capacityMW": "1000.0", "operational": "true", "location": "ПС Київська", "riskScore": ""},
    {"id": "AT_Kyivska_2", "label": "Transformer", "name": "Автотрансформатор АТ-2 750/330 кВ Київська", "type": "Autotransformer", "voltageKV": "750.0", "capacityMW": "1000.0", "operational": "true", "location": "ПС Київська", "riskScore": ""},
    {"id": "AT_Vinnytska_1", "label": "Transformer", "name": "Автотрансформатор АТ-1 750/330 кВ Вінницька", "type": "Autotransformer", "voltageKV": "750.0", "capacityMW": "1000.0", "operational": "true", "location": "ПС Вінницька", "riskScore": ""},
    {"id": "AT_Dniprovska_1", "label": "Transformer", "name": "Автотрансформатор АТ-1 750/330 кВ Дніпровська", "type": "Autotransformer", "voltageKV": "750.0", "capacityMW": "1000.0", "operational": "true", "location": "ПС Дніпровська", "riskScore": ""},
    {"id": "TR_Lviv2_T1", "label": "Transformer", "name": "Трансформатор Т-1 330/110 кВ Львів-2", "type": "StepDownTransformer", "voltageKV": "330.0", "capacityMW": "250.0", "operational": "true", "location": "ПС Львів-2", "riskScore": ""},
    {"id": "TR_Lviv2_T2", "label": "Transformer", "name": "Трансформатор Т-2 330/110 кВ Львів-2", "type": "StepDownTransformer", "voltageKV": "330.0", "capacityMW": "250.0", "operational": "true", "location": "ПС Львів-2", "riskScore": ""},
    {"id": "TR_Rivne_T1", "label": "Transformer", "name": "Трансформатор Т-1 330/110 кВ Рівне", "type": "StepDownTransformer", "voltageKV": "330.0", "capacityMW": "200.0", "operational": "true", "location": "ПС Рівне", "riskScore": ""},
    {"id": "TR_Ternopil_T1", "label": "Transformer", "name": "Трансформатор Т-1 330/110 кВ Тернопіль", "type": "StepDownTransformer", "voltageKV": "330.0", "capacityMW": "200.0", "operational": "true", "location": "ПС Тернопіль", "riskScore": ""},
    {"id": "TR_Kyiv_T3", "label": "Transformer", "name": "Трансформатор Т-3 330/110 кВ Київська", "type": "StepDownTransformer", "voltageKV": "330.0", "capacityMW": "250.0", "operational": "true", "location": "ПС Київська", "riskScore": ""},
    {"id": "TR_Dnipro_T2", "label": "Transformer", "name": "Трансформатор Т-2 330/110 кВ Дніпровська", "type": "StepDownTransformer", "voltageKV": "330.0", "capacityMW": "250.0", "operational": "true", "location": "ПС Дніпровська", "riskScore": ""},
    {"id": "TR_Zaporizhia_T1", "label": "Transformer", "name": "Трансформатор Т-1 330/110 кВ Запоріжжя", "type": "StepDownTransformer", "voltageKV": "330.0", "capacityMW": "250.0", "operational": "true", "location": "ПС Запорізька", "riskScore": ""},
    {"id": "TR_Odesa_T1", "label": "Transformer", "name": "Трансформатор Т-1 330/110 кВ Одеса", "type": "StepDownTransformer", "voltageKV": "330.0", "capacityMW": "200.0", "operational": "true", "location": "ПС Одеса", "riskScore": ""},
    {"id": "TR_Mykolaiv_T1", "label": "Transformer", "name": "Трансформатор Т-1 330/110 кВ Миколаїв", "type": "StepDownTransformer", "voltageKV": "330.0", "capacityMW": "200.0", "operational": "true", "location": "ПС Миколаїв", "riskScore": ""},
    {"id": "TR_Knyazhyi_T1", "label": "Transformer", "name": "Трансформатор Т-1 110/10 кВ Княжий", "type": "DistributionTransformer", "voltageKV": "110.0", "capacityMW": "63.0", "operational": "true", "location": "ПС Княжий", "riskScore": ""},
    {"id": "TR_Sykhiv_T1", "label": "Transformer", "name": "Трансформатор Т-1 110/10 кВ Сихів", "type": "DistributionTransformer", "voltageKV": "110.0", "capacityMW": "63.0", "operational": "true", "location": "ПС Сихів", "riskScore": ""},

    # CircuitBreakers (20)
    {"id": "CB_Q1_Zakhidna", "label": "CircuitBreaker", "name": "Елегазовий вимикач 750 кВ Q1 Західна", "type": "SF6_Breaker", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "ПС Західноукраїнська", "riskScore": ""},
    {"id": "CB_Q2_Zakhidna", "label": "CircuitBreaker", "name": "Елегазовий вимикач 330 кВ Q2 Західна", "type": "SF6_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "ПС Західноукраїнська", "riskScore": ""},
    {"id": "CB_Q3_Kyivska", "label": "CircuitBreaker", "name": "Елегазовий вимикач 750 кВ Q3 Київська", "type": "SF6_Breaker", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "ПС Київська", "riskScore": ""},
    {"id": "CB_Q4_Kyivska", "label": "CircuitBreaker", "name": "Елегазовий вимикач 330 кВ Q4 Київська", "type": "SF6_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "ПС Київська", "riskScore": ""},
    {"id": "CB_Q5_Vinnytska", "label": "CircuitBreaker", "name": "Елегазовий вимикач 750 кВ Q5 Вінницька", "type": "SF6_Breaker", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "ПС Вінницька", "riskScore": ""},
    {"id": "CB_Q6_Dniprovska", "label": "CircuitBreaker", "name": "Елегазовий вимикач 750 кВ Q6 Дніпровська", "type": "SF6_Breaker", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "ПС Дніпровська", "riskScore": ""},
    {"id": "CB_Q7_Lviv2", "label": "CircuitBreaker", "name": "Елегазовий вимикач 330 кВ Q7 Львів-2", "type": "SF6_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "ПС Львів-2", "riskScore": ""},
    {"id": "CB_Q8_Lviv2", "label": "CircuitBreaker", "name": "Вакуумний вимикач 110 кВ Q8 Львів-2", "type": "Vacuum_Breaker", "voltageKV": "110.0", "capacityMW": "", "operational": "true", "location": "ПС Львів-2", "riskScore": ""},
    {"id": "CB_Q9_Rivne", "label": "CircuitBreaker", "name": "Елегазовий вимикач 330 кВ Q9 Рівне", "type": "SF6_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "ПС Рівне", "riskScore": ""},
    {"id": "CB_Q10_Ternopil", "label": "CircuitBreaker", "name": "Елегазовий вимикач 330 кВ Q10 Тернопіль", "type": "SF6_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "ПС Тернопіль", "riskScore": ""},
    {"id": "CB_Q11_Dnipro", "label": "CircuitBreaker", "name": "Елегазовий вимикач 330 кВ Q11 Дніпро", "type": "SF6_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "ПС Дніпровська", "riskScore": ""},
    {"id": "CB_Q12_Zaporizhia", "label": "CircuitBreaker", "name": "Елегазовий вимикач 330 кВ Q12 Запоріжжя", "type": "SF6_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "ПС Запорізька", "riskScore": ""},
    {"id": "CB_Q13_Odesa", "label": "CircuitBreaker", "name": "Елегазовий вимикач 330 кВ Q13 Одеса", "type": "SF6_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "ПС Одеса", "riskScore": ""},
    {"id": "CB_Q14_Mykolaiv", "label": "CircuitBreaker", "name": "Елегазовий вимикач 330 кВ Q14 Миколаїв", "type": "SF6_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "ПС Миколаївська", "riskScore": ""},
    {"id": "CB_Q15_Knyazhyi", "label": "CircuitBreaker", "name": "Вакуумний вимикач 110 кВ Q15 Княжий", "type": "Vacuum_Breaker", "voltageKV": "110.0", "capacityMW": "", "operational": "true", "location": "ПС Княжий", "riskScore": ""},
    {"id": "CB_Q16_Sykhiv", "label": "CircuitBreaker", "name": "Вакуумний вимикач 110 кВ Q16 Сихів", "type": "Vacuum_Breaker", "voltageKV": "110.0", "capacityMW": "", "operational": "true", "location": "ПС Сихів", "riskScore": ""},
    {"id": "CB_Q17_DniproHPP", "label": "CircuitBreaker", "name": "Генераторний вимикач Q17 Дніпровська ГЕС", "type": "Generator_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Дніпровська ГЕС", "riskScore": ""},
    {"id": "CB_Q18_Trypillya", "label": "CircuitBreaker", "name": "Генераторний вимикач Q18 Трипільська ТЕС", "type": "Generator_Breaker", "voltageKV": "330.0", "capacityMW": "", "operational": "true", "location": "Трипільська ТЕС", "riskScore": ""},
    {"id": "CB_Q19_RivneNPP", "label": "CircuitBreaker", "name": "Блочний вимикач Q19 Рівненська АЕС", "type": "SF6_Breaker", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "Рівненська АЕС", "riskScore": ""},
    {"id": "CB_Q20_KhmelnytskyiNPP", "label": "CircuitBreaker", "name": "Блочний вимикач Q20 Хмельницька АЕС", "type": "SF6_Breaker", "voltageKV": "750.0", "capacityMW": "", "operational": "true", "location": "Хмельницька АЕС", "riskScore": ""},

    # RelayProtection (13)
    {"id": "RP_SEL421_Zakhidna", "label": "RelayProtection", "name": "Комплект ДЗЛ/ДЗП SEL-421 Західна", "type": "DistanceRelay", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Західноукраїнська", "riskScore": "0.04"},
    {"id": "RP_ABB_REL670_Kyivska", "label": "RelayProtection", "name": "Комплект ДЗЛ ABB REL670 Київська", "type": "DistanceRelay", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Київська", "riskScore": "0.03"},
    {"id": "RP_Siemens7SA522_Vinnytska", "label": "RelayProtection", "name": "Комплект ДЗ Siemens 7SA522 Вінницька", "type": "DistanceRelay", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Вінницька", "riskScore": "0.04"},
    {"id": "RP_SEL311L_Lviv2", "label": "RelayProtection", "name": "Комплект ДЗЛ SEL-311L Львів-2", "type": "DifferentialRelay", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Львів-2", "riskScore": "0.02"},
    {"id": "RP_ABB_RET670_Zakhidna_AT1", "label": "RelayProtection", "name": "Диференційний захист АТ ABB RET670 Західна", "type": "TransformerProtection", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Західноукраїнська", "riskScore": "0.02"},
    {"id": "RP_Siemens7UT612_Kyivska_AT1", "label": "RelayProtection", "name": "Диференційний захист АТ Siemens 7UT612 Київська", "type": "TransformerProtection", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Київська", "riskScore": "0.02"},
    {"id": "RP_SEL487B_Dniprovska", "label": "RelayProtection", "name": "Диференційний захист шин SEL-487B Дніпровська", "type": "BusbarProtection", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Дніпровська", "riskScore": "0.015"},
    {"id": "RP_ABB_REC670_DniproHPP", "label": "RelayProtection", "name": "Блочний захист генератора ABB REC670 ДніпроГЕС", "type": "GeneratorProtection", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "Дніпровська ГЕС", "riskScore": "0.03"},
    {"id": "RP_SEL451_RivneNPP", "label": "RelayProtection", "name": "Захист енергоблока SEL-451 РАЕС", "type": "UnitProtection", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "Рівненська АЕС", "riskScore": "0.02"},
    {"id": "RP_Siemens7SJ82_Knyazhyi", "label": "RelayProtection", "name": "Струмовий захист лінії Siemens 7SJ82 Княжий", "type": "OvercurrentRelay", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Княжий", "riskScore": "0.05"},
    {"id": "RP_SEL351_Sykhiv", "label": "RelayProtection", "name": "Струмовий захист фідера SEL-351 Сихів", "type": "OvercurrentRelay", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Сихів", "riskScore": "0.05"},
    {"id": "RP_ABB_REL650_Odesa", "label": "RelayProtection", "name": "Дистанційний захист ABB REL650 Одеса", "type": "DistanceRelay", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Одеса", "riskScore": "0.04"},
    {"id": "RP_Siemens7SA610_Mykolaiv", "label": "RelayProtection", "name": "Дистанційний захист Siemens 7SA610 Миколаїв", "type": "DistanceRelay", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "ПС Миколаївська", "riskScore": "0.04"},

    # SCADA Systems (6)
    {"id": "SCADA_Central_Ukrenergo", "label": "SCADA_System", "name": "Головний диспетчерський комплекс SCADA/EMS", "type": "NationalSCADA", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "Київ", "riskScore": ""},
    {"id": "SCADA_West_Dispatch", "label": "SCADA_System", "name": "Регіональна SCADA Західного ТУ", "type": "RegionalSCADA", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "Львів", "riskScore": ""},
    {"id": "SCADA_Central_Dispatch", "label": "SCADA_System", "name": "Регіональна SCADA Центрального ТУ", "type": "RegionalSCADA", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "Київ", "riskScore": ""},
    {"id": "SCADA_South_Dispatch", "label": "SCADA_System", "name": "Регіональна SCADA Південного ТУ", "type": "RegionalSCADA", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "Одеса", "riskScore": ""},
    {"id": "SCADA_Dnipro_Dispatch", "label": "SCADA_System", "name": "Регіональна SCADA Дніпровського ТУ", "type": "RegionalSCADA", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "Дніпро", "riskScore": ""},
    {"id": "SCADA_Lvivoblenergo", "label": "SCADA_System", "name": "Диспетчерський пункт ПрАТ Львівобленерго", "type": "DSO_SCADA", "voltageKV": "", "capacityMW": "", "operational": "true", "location": "Львів", "riskScore": ""},

    # ConsumerNodes (13)
    {"id": "Consumer_Lviv_Metropolis", "label": "ConsumerNode", "name": "Львівський міський промисловий вузол", "type": "UrbanIndustrial", "voltageKV": "110.0", "capacityMW": "380.0", "operational": "true", "location": "Львів", "riskScore": ""},
    {"id": "Consumer_Kyiv_Agglomeration", "label": "ConsumerNode", "name": "Київська міська агломерація", "type": "Metropolitan", "voltageKV": "110.0", "capacityMW": "1450.0", "operational": "true", "location": "Київ", "riskScore": ""},
    {"id": "Consumer_Dnipro_Industrial", "label": "ConsumerNode", "name": "Дніпровський металургійний вузол", "type": "HeavyIndustry", "voltageKV": "110.0", "capacityMW": "1100.0", "operational": "true", "location": "Дніпро", "riskScore": ""},
    {"id": "Consumer_KryvyiRih_Mining", "label": "ConsumerNode", "name": "Криворізький залізорудний комбінат", "type": "MiningCluster", "voltageKV": "110.0", "capacityMW": "950.0", "operational": "true", "location": "Кривий Ріг", "riskScore": ""},
    {"id": "Consumer_Zaporizhia_Smelter", "label": "ConsumerNode", "name": "Запорізький алюмінієвий комбінат", "type": "HeavyIndustry", "voltageKV": "110.0", "capacityMW": "720.0", "operational": "true", "location": "Запоріжжя", "riskScore": ""},
    {"id": "Consumer_Odesa_Port", "label": "ConsumerNode", "name": "Одеський морський порт та логістика", "type": "Infrastructure", "voltageKV": "110.0", "capacityMW": "410.0", "operational": "true", "location": "Одеса", "riskScore": ""},
    {"id": "Consumer_Vinnytsia_Municipal", "label": "ConsumerNode", "name": "Вінницький комунальний вузол", "type": "Municipal", "voltageKV": "110.0", "capacityMW": "190.0", "operational": "true", "location": "Вінниця", "riskScore": ""},
    {"id": "Consumer_Rivne_Chemical", "label": "ConsumerNode", "name": "РівнеАзот хімічне виробництво", "type": "ChemicalIndustry", "voltageKV": "110.0", "capacityMW": "220.0", "operational": "true", "location": "Рівне", "riskScore": ""},
    {"id": "Consumer_Ternopil_Municipal", "label": "ConsumerNode", "name": "Тернопільське міське навантаження", "type": "Municipal", "voltageKV": "110.0", "capacityMW": "160.0", "operational": "true", "location": "Тернопіль", "riskScore": ""},
    {"id": "Consumer_Mykolaiv_Shipyard", "label": "ConsumerNode", "name": "Миколаївський суднобудівний кластер", "type": "HeavyIndustry", "voltageKV": "110.0", "capacityMW": "280.0", "operational": "true", "location": "Миколаїв", "riskScore": ""},
    {"id": "Consumer_Cherkasy_Azot", "label": "ConsumerNode", "name": "Черкаський комбінат Азот", "type": "ChemicalIndustry", "voltageKV": "110.0", "capacityMW": "340.0", "operational": "true", "location": "Черкаси", "riskScore": ""},
    {"id": "Consumer_Poltava_OilGas", "label": "ConsumerNode", "name": "Полтавський газовидобувний район", "type": "EnergySector", "voltageKV": "110.0", "capacityMW": "210.0", "operational": "true", "location": "Полтава", "riskScore": ""},
    {"id": "Consumer_IvanoFrankivsk_Municipal", "label": "ConsumerNode", "name": "Івано-Франківський міський вузол", "type": "Municipal", "voltageKV": "110.0", "capacityMW": "180.0", "operational": "true", "location": "Івано-Франківськ", "riskScore": ""},

    # GridEvents (9)
    {"id": "EV_ShortCircuit_Line750_ZK", "label": "GridEvent", "name": "Міжфазне коротке замикання на ПЛ 750 кВ Західна-Київ", "type": "ShortCircuit", "voltageKV": "750.0", "capacityMW": "", "operational": "false", "location": "ПЛ 750 кВ", "riskScore": "0.88"},
    {"id": "EV_TripBreaker_Q1", "label": "GridEvent", "name": "Аварійне розмикання елегазового вимикача Q1", "type": "BreakerTrip", "voltageKV": "750.0", "capacityMW": "", "operational": "false", "location": "ПС Західноукраїнська", "riskScore": "0.72"},
    {"id": "EV_Overload_Line330_ZL", "label": "GridEvent", "name": "Перевантаження транзиту 330 кВ Західна — Львів-2", "type": "LineOverload", "voltageKV": "330.0", "capacityMW": "", "operational": "false", "location": "ПЛ 330 кВ", "riskScore": "0.79"},
    {"id": "EV_VoltageSag_Lviv2", "label": "GridEvent", "name": "Просідання напруги на шинах 330 кВ Львів-2", "type": "VoltageSag", "voltageKV": "330.0", "capacityMW": "", "operational": "false", "location": "ПС Львів-2", "riskScore": "0.65"},
    {"id": "EV_CascadeRisk_WestCluster", "label": "GridEvent", "name": "Ризик каскадного знеструмлення Західного регіону", "type": "CascadeRisk", "voltageKV": "", "capacityMW": "", "operational": "false", "location": "Західний енергорайон", "riskScore": "0.94"},
    {"id": "EV_StormWarning_Carpathians", "label": "GridEvent", "name": "Шквальний вітер та ожеледь у передгір'ї Карпат", "type": "WeatherAlert", "voltageKV": "", "capacityMW": "", "operational": "false", "location": "Прикарпаття", "riskScore": "0.55"},
    {"id": "EV_FrequencyDrop_Central", "label": "GridEvent", "name": "Зниження системної частоти в Центральній зоні до 49.6 Гц", "type": "FrequencyDrop", "voltageKV": "", "capacityMW": "", "operational": "false", "location": "ОЕС України", "riskScore": "0.82"},
    {"id": "EV_UnderFrequencyLoadShedding", "label": "GridEvent", "name": "Спрацювання автоматичного частотного розвантаження (АЧР)", "type": "LoadShedding", "voltageKV": "", "capacityMW": "", "operational": "false", "location": "Розподільчі ПС", "riskScore": "0.86"},
    {"id": "EV_TransformerOilOverheat_AT1", "label": "GridEvent", "name": "Температурний сигнал перегріву мастила АТ-1", "type": "ThermalAlarm", "voltageKV": "750.0", "capacityMW": "", "operational": "false", "location": "ПС Західноукраїнська", "riskScore": "0.60"}
]

# 2. Зв'язки (Relationships) - 280 типізованих зв'язків
relationships = []

def add_rel(start_id, end_id, rel_type, source="Dispatch_Log_2026", confidence="0.98", valid_from="2026-01-01"):
    relationships.append({
        "start_id": start_id,
        "end_id": end_id,
        "type": rel_type,
        "source": source,
        "confidence": confidence,
        "validFrom": valid_from
    })

# SUPPLIES_POWER_TO: PowerPlants -> Substations (20)
add_rel("DniproHPP", "SS_Dniprovska", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("DniproHPP", "SS_Zaporizka", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("DniesterHPP", "SS_Chernivtsi", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("DnistrovskaPSPP", "SS_Chernivtsi", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("DnistrovskaPSPP", "SS_Vinnytska", "SUPPLIES_POWER_TO", "Plant_Passport", "0.98")
add_rel("TrypilskaTPP", "SS_Kyivska", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("TrypilskaTPP", "SS_Cherkaska", "SUPPLIES_POWER_TO", "Plant_Passport", "0.98")
add_rel("BurshtynTPP", "SS_Zakhidna", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("BurshtynTPP", "SS_IvanoFrankivska", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("KryvorizkaTPP", "SS_Kryvorizka", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("KryvorizkaTPP", "SS_Dniprovska", "SUPPLIES_POWER_TO", "Plant_Passport", "0.98")
add_rel("LadyzhynskaTPP", "SS_Vinnytska", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("RivneNPP", "SS_Zakhidna", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("RivneNPP", "SS_Kyivska", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("KhmelnytskyiNPP", "SS_Kyivska", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("KhmelnytskyiNPP", "SS_Vinnytska", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("SouthUkraineNPP", "SS_Vinnytska", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("SouthUkraineNPP", "SS_Dniprovska", "SUPPLIES_POWER_TO", "Plant_Passport", "1.0")
add_rel("PokrovskaSES", "SS_Kryvorizka", "SUPPLIES_POWER_TO", "RES_Registry", "0.95")
add_rel("BotievoVES", "SS_Zaporizka", "SUPPLIES_POWER_TO", "RES_Registry", "0.95")

# CONNECTS_TO: Lines <-> Substations (30 lines * 2 endpoints = 60)
line_endpoints = [
    {"line": "Line_750_Zakhidna_Kyiv", "a": "SS_Zakhidna", "b": "SS_Kyivska"},
    {"line": "Line_750_Zakhidna_Vinnytsia", "a": "SS_Zakhidna", "b": "SS_Vinnytska"},
    {"line": "Line_750_Vinnytsia_Kyiv", "a": "SS_Vinnytska", "b": "SS_Kyivska"},
    {"line": "Line_750_Kyiv_Pivnichna", "a": "SS_Kyivska", "b": "SS_Pivnichna"},
    {"line": "Line_750_Pivnichna_Dnipro", "a": "SS_Pivnichna", "b": "SS_Dniprovska"},
    {"line": "Line_750_Vinnytsia_Dnipro", "a": "SS_Vinnytska", "b": "SS_Dniprovska"},
    {"line": "Line_750_Khmelnytskyi_Kyiv", "a": "SS_Khmelnytska", "b": "SS_Kyivska"},
    {"line": "Line_750_Rivne_Kyiv", "a": "SS_Rivne330", "b": "SS_Kyivska"},
    {"line": "Line_750_SouthUkraine_Vinnytsia", "a": "SS_Mykolaivska", "b": "SS_Vinnytska"},
    {"line": "Line_750_SouthUkraine_Dnipro", "a": "SS_Mykolaivska", "b": "SS_Dniprovska"},

    {"line": "Line_330_Zakhidna_Lviv2", "a": "SS_Zakhidna", "b": "SS_Lviv2"},
    {"line": "Line_330_Lviv2_Rivne", "a": "SS_Lviv2", "b": "SS_Rivne330"},
    {"line": "Line_330_Lviv2_IvanoFrankivsk", "a": "SS_Lviv2", "b": "SS_IvanoFrankivska"},
    {"line": "Line_330_Zakhidna_Ternopil", "a": "SS_Zakhidna", "b": "SS_Ternopilska"},
    {"line": "Line_330_Ternopil_Khmelnytskyi", "a": "SS_Ternopilska", "b": "SS_Khmelnytska"},
    {"line": "Line_330_Dniester_Chernivtsi", "a": "SS_Vinnytska", "b": "SS_Chernivtsi"},
    {"line": "Line_330_Chernivtsi_IvanoFrankivsk", "a": "SS_Chernivtsi", "b": "SS_IvanoFrankivska"},
    {"line": "Line_330_Kyiv_Zhytomyr", "a": "SS_Kyivska", "b": "SS_Zhytomyrska"},
    {"line": "Line_330_Kyiv_Cherkasy", "a": "SS_Kyivska", "b": "SS_Cherkaska"},
    {"line": "Line_330_Kyiv_Brovary", "a": "SS_Kyivska", "b": "SS_Brovary"},
    {"line": "Line_330_Dnipro_Zaporizhia", "a": "SS_Dniprovska", "b": "SS_Zaporizka"},
    {"line": "Line_330_Dnipro_KryvyiRih", "a": "SS_Dniprovska", "b": "SS_Kryvorizka"},
    {"line": "Line_330_Zaporizhia_DniproHPP", "a": "SS_Zaporizka", "b": "SS_Dniprovska"},
    {"line": "Line_330_SouthUkraine_Mykolaiv", "a": "SS_Vinnytska", "b": "SS_Mykolaivska"},
    {"line": "Line_330_Mykolaiv_Odesa", "a": "SS_Mykolaivska", "b": "SS_Odeska"},

    {"line": "Line_110_Lviv2_Knyazhyi", "a": "SS_Lviv2", "b": "SS_LvivKnyazhyi"},
    {"line": "Line_110_Lviv2_Sykhiv", "a": "SS_Lviv2", "b": "SS_Sykhiv"},
    {"line": "Line_110_Zakhidna_Brody", "a": "SS_Zakhidna", "b": "SS_Brody"},
    {"line": "Line_110_Kyiv_Boryspil", "a": "SS_Kyivska", "b": "SS_Boryspil"},
    {"line": "Line_110_Kyiv_Fastiv", "a": "SS_Kyivska", "b": "SS_Fastiv"}
]

for ep in line_endpoints:
    add_rel(ep["line"], ep["a"], "CONNECTS_TO", "Grid_Topology_DB", "1.0")
    add_rel(ep["line"], ep["b"], "CONNECTS_TO", "Grid_Topology_DB", "1.0")

# CONTAINS_EQUIPMENT: Substations -> Transformers & Breakers (33)
sub_equipment = [
    {"sub": "SS_Zakhidna", "eq": ["AT_Zakhidna_1", "AT_Zakhidna_2", "CB_Q1_Zakhidna", "CB_Q2_Zakhidna"]},
    {"sub": "SS_Kyivska", "eq": ["AT_Kyivska_1", "AT_Kyivska_2", "TR_Kyiv_T3", "CB_Q3_Kyivska", "CB_Q4_Kyivska"]},
    {"sub": "SS_Vinnytska", "eq": ["AT_Vinnytska_1", "CB_Q5_Vinnytska"]},
    {"sub": "SS_Dniprovska", "eq": ["AT_Dniprovska_1", "TR_Dnipro_T2", "CB_Q6_Dniprovska", "CB_Q11_Dnipro"]},
    {"sub": "SS_Lviv2", "eq": ["TR_Lviv2_T1", "TR_Lviv2_T2", "CB_Q7_Lviv2", "CB_Q8_Lviv2"]},
    {"sub": "SS_Rivne330", "eq": ["TR_Rivne_T1", "CB_Q9_Rivne"]},
    {"sub": "SS_Ternopilska", "eq": ["TR_Ternopil_T1", "CB_Q10_Ternopil"]},
    {"sub": "SS_Zaporizka", "eq": ["TR_Zaporizhia_T1", "CB_Q12_Zaporizhia"]},
    {"sub": "SS_Odeska", "eq": ["TR_Odesa_T1", "CB_Q13_Odesa"]},
    {"sub": "SS_Mykolaivska", "eq": ["TR_Mykolaiv_T1", "CB_Q14_Mykolaiv"]},
    {"sub": "SS_LvivKnyazhyi", "eq": ["TR_Knyazhyi_T1", "CB_Q15_Knyazhyi"]},
    {"sub": "SS_Sykhiv", "eq": ["TR_Sykhiv_T1", "CB_Q16_Sykhiv"]}
]

for item in sub_equipment:
    for e in item["eq"]:
        add_rel(item["sub"], e, "CONTAINS_EQUIPMENT", "Substation_Asset_Passport", "1.0")

# Power plant generator breakers
add_rel("DniproHPP", "CB_Q17_DniproHPP", "CONTAINS_EQUIPMENT", "Plant_Asset_Register", "1.0")
add_rel("TrypilskaTPP", "CB_Q18_Trypillya", "CONTAINS_EQUIPMENT", "Plant_Asset_Register", "1.0")
add_rel("RivneNPP", "CB_Q19_RivneNPP", "CONTAINS_EQUIPMENT", "Plant_Asset_Register", "1.0")
add_rel("KhmelnytskyiNPP", "CB_Q20_KhmelnytskyiNPP", "CONTAINS_EQUIPMENT", "Plant_Asset_Register", "1.0")

# PROTECTS: Relays -> Lines, Transformers, Plants (20)
add_rel("RP_SEL421_Zakhidna", "Line_750_Zakhidna_Kyiv", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_SEL421_Zakhidna", "Line_750_Zakhidna_Vinnytsia", "PROTECTS", "Relay_Coordination_Sheet", "0.98")
add_rel("RP_ABB_REL670_Kyivska", "Line_750_Zakhidna_Kyiv", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_ABB_REL670_Kyivska", "Line_750_Vinnytsia_Kyiv", "PROTECTS", "Relay_Coordination_Sheet", "0.98")
add_rel("RP_Siemens7SA522_Vinnytska", "Line_750_Vinnytsia_Kyiv", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_Siemens7SA522_Vinnytska", "Line_750_Vinnytsia_Dnipro", "PROTECTS", "Relay_Coordination_Sheet", "0.98")
add_rel("RP_SEL311L_Lviv2", "Line_330_Zakhidna_Lviv2", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_SEL311L_Lviv2", "Line_330_Lviv2_Rivne", "PROTECTS", "Relay_Coordination_Sheet", "0.98")
add_rel("RP_ABB_RET670_Zakhidna_AT1", "AT_Zakhidna_1", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_ABB_RET670_Zakhidna_AT1", "AT_Zakhidna_2", "PROTECTS", "Relay_Coordination_Sheet", "0.95")
add_rel("RP_Siemens7UT612_Kyivska_AT1", "AT_Kyivska_1", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_SEL487B_Dniprovska", "SS_Dniprovska", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_ABB_REC670_DniproHPP", "DniproHPP", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_SEL451_RivneNPP", "RivneNPP", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_Siemens7SJ82_Knyazhyi", "Line_110_Lviv2_Knyazhyi", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_SEL351_Sykhiv", "Line_110_Lviv2_Sykhiv", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_ABB_REL650_Odesa", "Line_330_Mykolaiv_Odesa", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_Siemens7SA610_Mykolaiv", "Line_330_SouthUkraine_Mykolaiv", "PROTECTS", "Relay_Coordination_Sheet", "1.0")
add_rel("RP_SEL311L_Lviv2", "Line_330_Lviv2_IvanoFrankivsk", "PROTECTS", "Relay_Coordination_Sheet", "0.95")
add_rel("RP_SEL421_Zakhidna", "CB_Q1_Zakhidna", "PROTECTS", "Relay_Coordination_Sheet", "0.95")

# TRIPS_BREAKER: Relays -> Breakers (14)
add_rel("RP_SEL421_Zakhidna", "CB_Q1_Zakhidna", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_ABB_REL670_Kyivska", "CB_Q3_Kyivska", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_Siemens7SA522_Vinnytska", "CB_Q5_Vinnytska", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_SEL311L_Lviv2", "CB_Q7_Lviv2", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_ABB_RET670_Zakhidna_AT1", "CB_Q1_Zakhidna", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_ABB_RET670_Zakhidna_AT1", "CB_Q2_Zakhidna", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_Siemens7UT612_Kyivska_AT1", "CB_Q3_Kyivska", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_Siemens7UT612_Kyivska_AT1", "CB_Q4_Kyivska", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_SEL487B_Dniprovska", "CB_Q6_Dniprovska", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_ABB_REC670_DniproHPP", "CB_Q17_DniproHPP", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_SEL451_RivneNPP", "CB_Q19_RivneNPP", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_Siemens7SJ82_Knyazhyi", "CB_Q15_Knyazhyi", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_SEL351_Sykhiv", "CB_Q16_Sykhiv", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")
add_rel("RP_ABB_REL650_Odesa", "CB_Q13_Odesa", "TRIPS_BREAKER", "Trip_Matrix_2026", "1.0")

# MONITORED_BY: Substations & Plants -> SCADA (65+)
west_substations = ["SS_Zakhidna", "SS_Lviv2", "SS_Rivne330", "SS_Ternopilska", "SS_IvanoFrankivska", "SS_Chernivtsi", "SS_LvivKnyazhyi", "SS_Sykhiv", "SS_Brody"]
for s in west_substations:
    add_rel(s, "SCADA_West_Dispatch", "MONITORED_BY", "SCADA_Channel_Cfg", "0.99")
    add_rel(s, "SCADA_Central_Ukrenergo", "MONITORED_BY", "EMS_ICC_Protocol", "0.98")

central_substations = ["SS_Kyivska", "SS_Vinnytska", "SS_Zhytomyrska", "SS_Cherkaska", "SS_Boryspil", "SS_Brovary", "SS_Fastiv"]
for s in central_substations:
    add_rel(s, "SCADA_Central_Dispatch", "MONITORED_BY", "SCADA_Channel_Cfg", "0.99")
    add_rel(s, "SCADA_Central_Ukrenergo", "MONITORED_BY", "EMS_ICC_Protocol", "0.98")

dnipro_substations = ["SS_Dniprovska", "SS_Pivnichna", "SS_Donbaska", "SS_Poltavska", "SS_Kryvorizka", "SS_Zaporizka"]
for s in dnipro_substations:
    add_rel(s, "SCADA_Dnipro_Dispatch", "MONITORED_BY", "SCADA_Channel_Cfg", "0.99")
    add_rel(s, "SCADA_Central_Ukrenergo", "MONITORED_BY", "EMS_ICC_Protocol", "0.98")

south_substations = ["SS_Odeska", "SS_Mykolaivska", "SS_Khmelnytska"]
for s in south_substations:
    add_rel(s, "SCADA_South_Dispatch", "MONITORED_BY", "SCADA_Channel_Cfg", "0.99")
    add_rel(s, "SCADA_Central_Ukrenergo", "MONITORED_BY", "EMS_ICC_Protocol", "0.98")

all_plants = [
    "DniproHPP", "DniesterHPP", "DnistrovskaPSPP", "TrypilskaTPP", "BurshtynTPP", 
    "KryvorizkaTPP", "LadyzhynskaTPP", "RivneNPP", "KhmelnytskyiNPP", "SouthUkraineNPP", 
    "PokrovskaSES", "BotievoVES"
]
for p in all_plants:
    add_rel(p, "SCADA_Central_Ukrenergo", "MONITORED_BY", "Telemetry_Gateway", "0.99")

# FEEDS_CONSUMER: Substations -> Consumers (18)
add_rel("SS_Lviv2", "Consumer_Lviv_Metropolis", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_LvivKnyazhyi", "Consumer_Lviv_Metropolis", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Sykhiv", "Consumer_Lviv_Metropolis", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Kyivska", "Consumer_Kyiv_Agglomeration", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Boryspil", "Consumer_Kyiv_Agglomeration", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Brovary", "Consumer_Kyiv_Agglomeration", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Dniprovska", "Consumer_Dnipro_Industrial", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Kryvorizka", "Consumer_KryvyiRih_Mining", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Zaporizka", "Consumer_Zaporizhia_Smelter", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Odeska", "Consumer_Odesa_Port", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Vinnytska", "Consumer_Vinnytsia_Municipal", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Rivne330", "Consumer_Rivne_Chemical", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Ternopilska", "Consumer_Ternopil_Municipal", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Mykolaivska", "Consumer_Mykolaiv_Shipyard", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Cherkaska", "Consumer_Cherkasy_Azot", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Poltavska", "Consumer_Poltava_OilGas", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_IvanoFrankivska", "Consumer_IvanoFrankivsk_Municipal", "FEEDS_CONSUMER", "Distribution_Contract", "1.0")
add_rel("SS_Brody", "Consumer_Lviv_Metropolis", "FEEDS_CONSUMER", "Distribution_Contract", "0.9")

# TRIGGERS_EVENT: Cascade Event chains (12)
add_rel("EV_StormWarning_Carpathians", "EV_ShortCircuit_Line750_ZK", "TRIGGERS_EVENT", "Incident_Report_Log", "0.85")
add_rel("EV_ShortCircuit_Line750_ZK", "EV_TripBreaker_Q1", "TRIGGERS_EVENT", "Relay_Operation_Log", "1.0")
add_rel("EV_TripBreaker_Q1", "EV_Overload_Line330_ZL", "TRIGGERS_EVENT", "PowerFlow_Analysis", "0.92")
add_rel("EV_Overload_Line330_ZL", "EV_VoltageSag_Lviv2", "TRIGGERS_EVENT", "SCADA_Alarm_Log", "0.88")
add_rel("EV_VoltageSag_Lviv2", "EV_CascadeRisk_WestCluster", "TRIGGERS_EVENT", "Risk_Assessment_Model", "0.94")
add_rel("EV_CascadeRisk_WestCluster", "EV_FrequencyDrop_Central", "TRIGGERS_EVENT", "Dynamic_Stability_Sim", "0.86")
add_rel("EV_FrequencyDrop_Central", "EV_UnderFrequencyLoadShedding", "TRIGGERS_EVENT", "Emergency_Control_Log", "0.95")
add_rel("EV_TransformerOilOverheat_AT1", "EV_TripBreaker_Q1", "TRIGGERS_EVENT", "Thermal_Trip_Curve", "0.80")
add_rel("EV_ShortCircuit_Line750_ZK", "EV_VoltageSag_Lviv2", "TRIGGERS_EVENT", "Fault_Transient_Analysis", "0.90")
add_rel("EV_Overload_Line330_ZL", "EV_CascadeRisk_WestCluster", "TRIGGERS_EVENT", "N_Minus_1_Contingency", "0.89")
add_rel("EV_FrequencyDrop_Central", "EV_CascadeRisk_WestCluster", "TRIGGERS_EVENT", "System_Interconnection_Model", "0.87")
add_rel("EV_ShortCircuit_Line750_ZK", "EV_FrequencyDrop_Central", "TRIGGERS_EVENT", "Disturbance_Recorder", "0.84")

# MANAGED_BY: Plants & Substations -> Operator (37)
for p in all_plants:
    add_rel(p, "Operator_Ukrenergo", "MANAGED_BY", "Licensing_Register", "1.0")

all_substations = [
    "SS_Zakhidna", "SS_Kyivska", "SS_Vinnytska", "SS_Dniprovska", "SS_Pivnichna", "SS_Donbaska",
    "SS_Lviv2", "SS_Rivne330", "SS_Ternopilska", "SS_IvanoFrankivska", "SS_Zhytomyrska", "SS_Cherkaska",
    "SS_Poltavska", "SS_Kryvorizka", "SS_Zaporizka", "SS_Odeska", "SS_Mykolaivska", "SS_Khmelnytska",
    "SS_Chernivtsi", "SS_LvivKnyazhyi", "SS_Sykhiv", "SS_Brody", "SS_Boryspil", "SS_Brovary", "SS_Fastiv"
]
for s in all_substations:
    add_rel(s, "Operator_Ukrenergo", "MANAGED_BY", "Transmission_Code_2026", "1.0")


def generate_csv():
    # Save nodes.csv
    nodes_csv_path = DATA_DIR / "nodes.csv"
    with open(nodes_csv_path, mode="w", encoding="utf-8", newline="") as f:
        fieldnames = ["id", "label", "name", "type", "voltageKV", "capacityMW", "operational", "location", "riskScore"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(nodes)

    # Save relationships.csv
    rels_csv_path = DATA_DIR / "relationships.csv"
    with open(rels_csv_path, mode="w", encoding="utf-8", newline="") as f:
        fieldnames = ["start_id", "end_id", "type", "source", "confidence", "validFrom"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(relationships)

    print(f"[SUCCESS] Згенеровано дані графа (Python):")
    print(f" - Вузлів (nodes.csv): {len(nodes)} (Вимога методички: >= 100)")
    print(f" - Зв'язків (relationships.csv): {len(relationships)} (Вимога методички: >= 200)")
    print(f" - Каталог збереження: {DATA_DIR}")

if __name__ == "__main__":
    generate_csv()
