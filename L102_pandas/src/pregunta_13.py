import os
import pandas as pd


def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file0_path = os.path.join(base_dir, "data", "tbl0.tsv")
    file2_path = os.path.join(base_dir, "data", "tbl2.tsv")

    tbl0 = pd.read_csv(file0_path, sep="\t")
    tbl2 = pd.read_csv(file2_path, sep="\t")

    # Unir ambas tablas por la columna común 'c0'
    merged = pd.merge(tbl0, tbl2, on="c0")

    # Agrupar por 'c1' y calcular la suma de 'c5b'
    return merged.groupby("c1")["c5b"].sum()


if __name__ == "__main__":
    print(pregunta_13())