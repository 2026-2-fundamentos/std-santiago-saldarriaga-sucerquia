import gzip
import os


def pregunta_10():
    """
        Para cada registro del archivo, en el mismo orden en que aparecen,
        retorne una tupla con la letra de la primera columna (`letter`), la
        cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
        pares de la quinta columna (`metrics`). El resultado es una lista con una
        tupla por registro.
    
        Ejemplo del formato de la respuesta:
    
            [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
        """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    result = []
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("\t") if "\t" in line else line.strip().split(",")
            if len(row) >= 5:
                letter = row[0]
                # Cuarta columna: elementos separados por comas (codes)
                codes_count = len(row[3].split(","))
                # Quinta columna: pares clave:valor separados por comas (metrics)
                metrics_count = len(row[4].split(","))

                result.append((letter, codes_count, metrics_count))

    return result


if __name__ == "__main__":
    print(pregunta_10())