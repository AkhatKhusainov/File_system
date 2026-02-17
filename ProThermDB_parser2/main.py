# scripts/run_parser.py
import pandas as pd
from src.parser.parser_protherm import pars_data
from src.cleaning.data_clean import data_clean
from src.sequences.add_sequences import add_sequences
from src.utils.paths import RAW_DATA_DIR, FINAL_DATA_DIR
from src.mutations.mutation_add import apply_mutations


def main():
    while True:
        print("Введите")
        org_name = input("Название организма или None (пример - Bacillus licheniformis): ")
        prot_name = input("Название фермента или None (пример - Alpha-amylase): ")
        if org_name != "" and org_name != "None" or prot_name != "" and prot_name != "None":
            break
        else:
            print('Нужно ввести хотя бы одно значение!')

    # 1. Парсинг данных
    print("Парсинг данных из ProThermDB...")
    df_raw = pars_data(org_name=org_name, prot_name=prot_name)  # ваша текущая функция
    raw_path = RAW_DATA_DIR
    print(f"Сырые данные сохранены: {raw_path}")

    # удаление дубликатов и замена пропусков
    df_raw = data_clean(df_raw)

    # 2. Добавление последовательностей
    print("\nДобавление последовательностей...")
    df_with_seq = add_sequences(
        df_raw,
        pdb_mutation_col="PDB_Chain_Mutation",
        pdb_col="PDB_wild",
        uniprot_col="UniProt_ID",
        seq_col="sequence",
        sleep_time=0.5
    )

    # Сохраняем обогащённые данные
    enriched_path = RAW_DATA_DIR / "protherm_with_sequences.csv"

    df_with_seq.to_csv(enriched_path, index=False)
    print(f"Данные с последовательностями сохранены: {enriched_path}")

    df_with_mut = apply_mutations(
        df_with_seq,
        seq_col="sequence",
        uni_mut_col="MUTATION",
        pdb_mut_col="PDB_Chain_Mutation"
    )

    # Сохраняем обогащённые данные
    enriched_path = FINAL_DATA_DIR / "protherm_with_mutation.csv"
    df_with_mut.to_csv(enriched_path, index=False)
    print(f"Данные с мутациями сохранены: {enriched_path}")


if __name__ == "__main__":
    main()
