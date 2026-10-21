import os
import re
import pandas as pd


def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "clusters_report.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = lines[4:]

    clusters = []
    current_cluster = None

    for line in lines:
        match = re.match(
            r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$", line
        )

        if match:
            if current_cluster:
                clusters.append(current_cluster)

            cluster_num = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = float(match.group(3).replace(",", "."))
            palabras = match.group(4).strip()

            current_cluster = [cluster_num, cantidad, porcentaje, palabras]
        else:
            text = line.strip()
            if text and current_cluster:
                current_cluster[3] += " " + text

    if current_cluster:
        clusters.append(current_cluster)

    for c in clusters:
        palabras_texto = c[3].rstrip(".")
        palabras_texto = re.sub(r"\s+", " ", palabras_texto)
        palabras_lista = [p.strip() for p in palabras_texto.split(",")]
        c[3] = ", ".join(palabras_lista)

    columns = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]

    return pd.DataFrame(clusters, columns=columns)


if __name__ == "__main__":
    print(pregunta_01())