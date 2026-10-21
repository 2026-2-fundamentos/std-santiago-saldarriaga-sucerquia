import os


def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "tbl0.tsv")

    with open(file_path, "r", encoding="utf-8") as f:
        # Leemos todas las líneas y restamos 1 para ignorar el encabezado
        return len(f.readlines()) - 1


if __name__ == "__main__":
    print(pregunta_01())