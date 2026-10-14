import gzip
import os


def pregunta_12():
    """
        Para cada letra de la primera columna (`letter`), sume todos los valores
        numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
        Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.
    
        Ejemplo del formato de la respuesta:
    
            {"A": 177, "B": 187, "C": 114, ...}
        """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    totals = {}
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("\t") if "\t" in line else line.strip().split(",")
            if len(row) >= 5:
                letter = row[0]
                pairs = row[4].split(",")
                line_sum = 0
                for pair in pairs:
                    if ":" in pair:
                        _, val_str = pair.split(":")
                        line_sum += int(val_str)

                totals[letter] = totals.get(letter, 0) + line_sum

    return dict(sorted(totals.items()))


if __name__ == "__main__":
    print(pregunta_12())