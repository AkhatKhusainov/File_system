import requests
import re


def fetch_pdb_sequence(pdb_id: str) -> str | None:
    """
      Загружает FASTA-последовательность из PDB
    """
    try:
        url = f"https://www.rcsb.org/fasta/entry/{pdb_id}"
        r = requests.get(url, timeout=7)
        r.raise_for_status()

        lines = r.text.strip().split("\n")
        seq = "".join(l for l in lines if not l.startswith(">"))

        return seq
    except Exception as e:
        print(f'PDB error for{pdb_id}:{e}')
        return None


def fetch_alphafold_sequence(af_id: str) -> str | None:
    """
    Загружает последовательность AlphaFold (через UniProt)
    """
    m = re.match(r"AF-([A-Za-z0-9]+)-F1", af_id)
    if not m:
        return None
    uniprot = m.group(1)

    url = f"https://rest.uniprot.org/uniprotkb/{uniprot}.fasta"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    lines = r.text.strip().split("\n")
    seq = "".join(l for l in lines if not l.startswith(">"))

    return seq
