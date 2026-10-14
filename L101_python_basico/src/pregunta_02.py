import gzip
import os


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    counts = {}
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("\t") if "\t" in line else line.strip().split(",")
            if row:
                letter = row[0]
                counts[letter] = counts.get(letter, 0) + 1

    return sorted(counts.items())


if __name__ == "__main__":
    print(pregunta_02())