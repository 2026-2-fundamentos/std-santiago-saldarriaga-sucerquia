import gzip
import os


def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    totals = {}
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("\t") if "\t" in line else line.strip().split(",")
            if len(row) >= 2:
                letter = row[0]
                value = int(row[1])
                totals[letter] = totals.get(letter, 0) + value

    return sorted(totals.items())


if __name__ == "__main__":
    print(pregunta_03())