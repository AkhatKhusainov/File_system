import pandas as pd
import re
import time
from .pdb import fetch_pdb_sequence, fetch_alphafold_sequence
from .uniprot import fetch_uniprot_sequence


def add_sequences(
        df: pd.DataFrame,
        pdb_mutation_col: str = "PDB_Chain_Mutation",
        pdb_col: str = "PDB_wild",
        uniprot_col: str = "UniProt_ID",
        seq_col: str = "sequence",
        sleep_time: float = 0.5,
) -> pd.DataFrame:
    """
    Добавляет аминокислотные последовательности в таблицу.

    Логика:
    - если в PDB_Chain_Mutation нет пропусков → используем PDB_wild
    - иначе → используем UniProt_ID

    """

    #  1. Определяем источник для ВСЕЙ таблицы
    total_rows = len(df)

    if df[pdb_mutation_col].isna().any():
        source = "UniProt"
    else:
        source = "PDB"

    print(f"Источник последовательностей: {source}")

    #  2. Словарь для кэширования
    sequence_cache: dict[str, str | None] = {}

    sequences = []

    #  3. Основной цикл
    for _, row in df.iterrows():

        seq = None
        cache_key = None

        if source == "PDB":
            pdb_raw = row.get(pdb_col)

            if pd.notna(pdb_raw):
                pdb_raw = str(pdb_raw)

                if re.match(r"^[0-9][A-Za-z0-9]{3}$", pdb_raw):
                    cache_key = f"PDB:{pdb_raw}"

                    if cache_key not in sequence_cache:
                        sequence_cache[cache_key] = fetch_pdb_sequence(pdb_raw)
                        time.sleep(sleep_time)

                elif pdb_raw.startswith("AF-"):
                    cache_key = f"AF:{pdb_raw}"

                    if cache_key not in sequence_cache:
                        sequence_cache[cache_key] = fetch_alphafold_sequence(pdb_raw)
                        time.sleep(sleep_time)

        else:  # UniProt
            uniprot_id = row.get(uniprot_col)

            if pd.notna(uniprot_id):
                uniprot_id = str(uniprot_id)
                cache_key = f"UniProt:{uniprot_id}"

                if cache_key not in sequence_cache:
                    sequence_cache[cache_key] = fetch_uniprot_sequence(uniprot_id)
                    time.sleep(sleep_time)

        if cache_key is not None:
            seq = sequence_cache.get(cache_key)

        sequences.append(seq)

    #  4. Добавляем колонку
    df[seq_col] = sequences

    #  5. Статистика пропусков
    n_missing = df[seq_col].isna().sum()
    print(f"Пропусков в колонке '{seq_col}': {n_missing} из {len(df)}")

    df[seq_col] = sequences

    #  3. Считаем пропуски
    n_missing = df[seq_col].isna().sum()
    print(f"Количество пропусков в '{seq_col}': {n_missing}")

    return df
