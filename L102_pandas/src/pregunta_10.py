import os
import pandas as pd


def pregunta_10():
    """
    Usando `data/tbl0.tsv`, construya para cada categoría de la columna `c1`
    un texto con todos sus valores de la columna `c2`, ordenados de menor a
    mayor y separados por `:`. Retorne un DataFrame cuyo índice son las
    categorías, en orden alfabético, con una única columna llamada `c2`.

    Ejemplo del formato de la respuesta:

                            c2
        c1
        A     1:1:2:3:6:7:8:9
        B       1:3:4:5:6:8:9
        C           0:5:6:7:9
        ...
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "tbl0.tsv")

    df = pd.read_csv(file_path, sep="\t")

    # Agrupar por c1, ordenar los valores numéricos de c2, convertirlos a string y unirlos con ':'
    res = df.groupby("c1")["c2"].apply(
        lambda x: ":".join(map(str, sorted(x)))
    )

    # Convertir la Serie resultante a DataFrame con la columna llamada 'c2'
    return pd.DataFrame(res)


if __name__ == "__main__":
    print(pregunta_10())