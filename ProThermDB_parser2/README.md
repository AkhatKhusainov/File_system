# ProThermDB Parser

Парсер и пост-обработка данных из **ProThermDB**:
- загрузка экспериментальных записей по белку/организму;
- очистка таблицы;
- добавление аминокислотных последовательностей (PDB / AlphaFold / UniProt);
- применение мутаций к последовательности;
- сохранение итоговых CSV.

## Стек

- Python 3.10+
- pandas
- selenium
- requests

## Структура проекта

```text
ProThermDB_parser/
├─ main.py
├─ requirements.txt
└─ src/
   ├─ parser/parser_protherm.py     # парсинг и скачивание из ProThermDB
   ├─ cleaning/data_clean.py        # базовая очистка
   ├─ sequences/
   │  ├─ add_sequences.py           # обогащение последовательностями
   │  ├─ pdb.py                     # загрузка из PDB / AlphaFold
   │  └─ uniprot.py                 # загрузка из UniProt
   ├─ mutations/mutation_add.py     # применение мутаций к sequence
   └─ utils/paths.py                # пути до data/raw и data/final
```

## Быстрый старт

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/Eda-sha/ProThermDB_parser.git
   cd ProThermDB_parser
   ```

2. Создать виртуальное окружение и установить зависимости:
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. Убедиться, что установлен Google Chrome и совместимый ChromeDriver (Selenium использует `webdriver.Chrome()`).

4. Подготовить директории для данных:
   ```bash
   mkdir data\\raw data\\final
   ```

5. Запустить пайплайн:
   ```bash
   python main.py
   ```

## Как работает пайплайн

1. `pars_data(...)` открывает ProThermDB и скачивает TSV.
2. `data_clean(...)` удаляет дубликаты и заменяет `-` на `None`.
3. `add_sequences(...)` добавляет колонку `sequence`.
4. `apply_mutations(...)` строит колонку `mutation_seq`.
5. Результаты сохраняются в:
   - `data/raw/protherm_with_sequences.csv`
   - `data/final/protherm_with_mutation.csv`
