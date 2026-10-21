import os
import pandas as pd


def pregunta_01():
    """
        El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
        un programa de crédito, pero llegó sucio: tiene una columna de índice que
        no pertenece a los datos, registros duplicados, registros incompletos y
        valores que representan lo mismo escritos de formas distintas en los
        campos de texto, las fechas, el estrato y el monto.
    
        Su tarea es limpiarlo y guardar el resultado en
        `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
        separador y sin el índice de Pandas.
    
        El archivo limpio debe cumplir lo siguiente:
    
        - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
          `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
          `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
          orden.
        - Los campos de texto están en minúsculas y sus palabras separadas por
          espacios.
        - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
          separadores de miles.
        - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
          ejemplo `AAAA-MM-DD`.
        - No hay registros incompletos. La única excepción es
          `comuna_ciudadano`: sus valores faltantes son parte de los datos
          originales y deben conservarse.
        - No hay registros duplicados.
    
        Ejemplo del formato del archivo:
    
            sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
            femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
            ...
        """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "solicitudes_de_credito.csv.gz")
    output_dir = os.path.join(base_dir, "submission")
    output_file = os.path.join(output_dir, "solicitudes_de_credito.csv")

    df = pd.read_csv(file_path, compression="gzip", sep=";")

    if "Unnamed: 0" in df.columns or "" in df.columns:
        df = df.drop(df.columns[0], axis=1)

    text_cols = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for col in text_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.lower()
            .str.replace("_", " ")
            .str.replace("-", " ")
            .str.strip()
        )

    df["barrio"] = df["barrio"].str.replace("_", " ").str.replace("-", " ")

    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
        .str.strip()
    )
    df["monto_del_credito"] = df["monto_del_credito"].astype(int)

    df["estrato"] = df["estrato"].astype(int)

    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], format="mixed", dayfirst=True
    ).dt.strftime("%Y-%m-%d")

    subset_cols = [c for c in df.columns if c != "comuna_ciudadano"]
    df = df.dropna(subset=subset_cols)

    df = df.drop_duplicates()

    required_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]
    df = df[required_columns]

    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_file, sep=";", index=False)


if __name__ == "__main__":
    pregunta_01()