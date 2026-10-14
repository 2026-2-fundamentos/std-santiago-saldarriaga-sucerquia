import gzip
import os


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    ranges = {}
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("\t") if "\t" in line else line.strip().split(",")
            if len(row) >= 2:
                letter = row[0]
                value = int(row[1])

                if letter not in ranges:
                    ranges[letter] = [value, value]  # [máximo, mínimo]
                else:
                    if value > ranges[letter][0]:
                        ranges[letter][0] = value
                    if value < ranges[letter][1]:
                        ranges[letter][1] = value

    result = [(letter, max_val, min_val) for letter, (max_val, min_val) in ranges.items()]

    return sorted(result, key=lambda x: x[0])


if __name__ == "__main__":
    print(pregunta_05())