import gzip
import os


def pregunta_09():
    """
        Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
        de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
        claves en orden alfabético.
    
        Ejemplo del formato de la respuesta:
    
            {"aaa": 13, "bbb": 16, "ccc": 23, ...}
        """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    counts = {}
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("\t") if "\t" in line else line.strip().split(",")
            if len(row) >= 5:
                # La quinta columna tiene el formato: aaa:1,bbb:2,ccc:3
                pairs = row[4].split(",")
                for pair in pairs:
                    if ":" in pair:
                        key, _ = pair.split(":")
                        counts[key] = counts.get(key, 0) + 1

    # Retornamos el diccionario ordenado por sus claves
    return dict(sorted(counts.items()))


if __name__ == "__main__":
    print(pregunta_09())