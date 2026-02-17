import re
import pandas as pd

def apply_mutations(
        df,
        seq_col="sequence",
        uni_mut_col="MUTATION",
        pdb_mut_col="PDB_Chain_Mutation"
):

    if df[pdb_mut_col].isna().any():
        source = "UniProt"
    else:
        source = "PDB"

    if source == "PDB":
        mutation_col = pdb_mut_col
    else:
        mutation_col = uni_mut_col

    print(f"Источник мутаций: {mutation_col}")

    def mutate_row(row):

        seq = row[seq_col]
        mut_field = str(row[mutation_col]).strip()

        if pd.isna(seq):
            return None

        if mut_field.lower() in ["wild-type", "none", "", "nan"]:
            return seq

        mutations = [m.strip() for m in mut_field.split(",")]

        mutated_seq = seq

        for mut in mutations:

            match = re.match(r"([A-Za-z])(\d+)([A-Za-z])", mut)
            if not match:
                return None

            wt_aa, pos, mut_aa = match.groups()
            pos = int(pos)

            if pos < 1 or pos > len(mutated_seq):
                return None

            if mutated_seq[pos - 1] != wt_aa:
                return None

            mutated_seq = (
                mutated_seq[:pos - 1] +
                mut_aa +
                mutated_seq[pos:]
            )

        return mutated_seq

    df["mutation_seq"] = df.apply(mutate_row, axis=1)

    return df
