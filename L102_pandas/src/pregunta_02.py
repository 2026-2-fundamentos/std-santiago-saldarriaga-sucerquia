import os


def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "tbl0.tsv")

    with open(file_path, "r", encoding="utf-8") as f:
        primera_linea = f.readline()
        columnas = primera_linea.strip("\n").split("\t")
        return len(columnas)


if __name__ == "__main__":
    print(pregunta_02())