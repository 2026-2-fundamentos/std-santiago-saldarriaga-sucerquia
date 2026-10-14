import gzip
import os


def pregunta_08():
    """
        Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
        letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
        tuplas `(valor, letras)` ordenada por el valor.
    
        Ejemplo del formato de la respuesta:
    
            [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
        """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    val_dict = {}
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("\t") if "\t" in line else line.strip().split(",")
            if len(row) >= 2:
                letter = row[0]
                val = int(row[1])

                if val not in val_dict:
                    val_dict[val] = set()
                val_dict[val].add(letter)

    # Convertimos los conjuntos (sets) a listas ordenadas alfabéticamente
    result = [(val, sorted(list(letters))) for val, letters in val_dict.items()]

    # Ordenamos el resultado por el valor numérico
    return sorted(result, key=lambda x: x[0])


if __name__ == "__main__":
    print(pregunta_08())