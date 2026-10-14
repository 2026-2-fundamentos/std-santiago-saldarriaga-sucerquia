import gzip
import os

def pregunta_07():
    """
        Para cada valor distinto de la segunda columna (`value`), construya la
        lista de letras de la primera columna (`letter`) que aparecen con ese
        valor. Conserve las letras repetidas y el orden en que aparecen en el
        archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
        valor.
    
        Ejemplo del formato de la respuesta:
    
            [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
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
                    val_dict[val] = []
                val_dict[val].append(letter)

    return sorted(val_dict.items(), key=lambda x: x[0])


if __name__ == "__main__":
    print(pregunta_07())