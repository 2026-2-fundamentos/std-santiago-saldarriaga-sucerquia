import gzip
import os


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    counts = {}
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("\t") if "\t" in line else line.strip().split(",")
            if len(row) >= 3:
                date = row[2]
                month = date.split("-")[1]
                counts[month] = counts.get(month, 0) + 1

    return sorted(counts.items())


if __name__ == "__main__":
    print(pregunta_04())