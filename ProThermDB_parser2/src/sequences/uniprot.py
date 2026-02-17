import requests
import re

def fetch_uniprot_sequence(uniprot_id: str) -> str | None:
    """
    Загружает FASTA-последовательность из UniProt
    """
    # Загружаем последовательность
    try:
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
        response = requests.get(url, timeout=2)
        response.raise_for_status()

        fasta_data = response.text.strip().split('\n')
        seq = ''.join(fasta_data[1:])

        return seq

    except Exception as e:
        print(f"Ошибка для {uniprot_id}: {e}")
        return None
