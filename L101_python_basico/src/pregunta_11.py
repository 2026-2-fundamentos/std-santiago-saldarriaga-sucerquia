import gzip
import os


def pregunta_11():
    """
        La cuarta columna (`codes`) contiene letras minúsculas separadas por
        comas. Para cada una de esas letras, sume los valores de la segunda
        columna (`value`) de los registros en los que aparece. Retorne un
        diccionario `{letra: suma}` con las letras en orden alfabético.
    
        Ejemplo del formato de la respuesta:
    
            {"a": 122, "b": 49, "c": 91, ...}
        """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    totals = {}
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("\t") if "\t" in line else line.strip().split(",")
            if len(row) >= 4:
                val = int(row[1])
                # Separamos los códigos minúsculos de la cuarta columna por comas
                codes = row[3].split(",")
                for code in codes:
                    totals[code] = totals.get(code, 0) + val

    # Retornamos un diccionario ordenado alfabéticamente por sus claves
    return dict(sorted(totals.items()))


if __name__ == "__main__":
    print(pregunta_11())