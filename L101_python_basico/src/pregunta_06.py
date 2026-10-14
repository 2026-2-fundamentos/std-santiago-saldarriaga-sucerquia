import gzip
import os


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    dict_metrics = {}
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("\t") if "\t" in line else line.strip().split(",")
            if len(row) >= 5:
                # La quinta columna tiene formato: aaa:1,bbb:2,ccc:3
                pairs = row[4].split(",")
                for pair in pairs:
                    if ":" in pair:
                        key, val_str = pair.split(":")
                        val = int(val_str)

                        if key not in dict_metrics:
                            dict_metrics[key] = [val, val]  # [mínimo, máximo]
                        else:
                            if val < dict_metrics[key][0]:
                                dict_metrics[key][0] = val
                            if val > dict_metrics[key][1]:
                                dict_metrics[key][1] = val

    # Convertimos a tuplas (clave, mínimo, máximo)
    result = [(key, min_val, max_val) for key, (min_val, max_val) in dict_metrics.items()]

    return sorted(result, key=lambda x: x[0])


if __name__ == "__main__":
    print(pregunta_06())