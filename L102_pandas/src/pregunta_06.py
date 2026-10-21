import os
import pandas as pd


def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "tbl1.tsv")

    df = pd.read_csv(file_path, sep="\t")
    valores_unicos = df["c4"].str.upper().unique()
    return sorted(list(valores_unicos))


if __name__ == "__main__":
    print(pregunta_06())