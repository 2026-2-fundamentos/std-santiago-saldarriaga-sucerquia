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
    """Limpieza y procesamiento del archivo de solicitudes de crédito."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "solicitudes_de_credito.csv.gz")
    output_dir = os.path.join(base_dir, "submission")
    output_file = os.path.join(output_dir, "solicitudes_de_credito.csv")

    # 1. Lectura del archivo (el original está delimitado por punto y coma ';')
    df = pd.read_csv(file_path, sep=";", index_col=0)

    # 2. Definir y ordenar las 9 columnas solicitadas
    target_columns = [
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

    # Homogeneizar nombre de columna en caso de que venga sin tilde
    if "linea_credito" in df.columns and "línea_credito" not in df.columns:
        df = df.rename(columns={"linea_credito": "línea_credito"})

    df = df[target_columns]

    # 3. Eliminar filas incompletas (excepto comuna_ciudadano)
    cols_check_na = [col for col in target_columns if col != "comuna_ciudadano"]
    df = df.dropna(subset=cols_check_na)

    # 4. Limpieza de campos de texto (minúsculas, sin guiones/guiones bajos y espacios limpios)
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
            .str.replace("_", " ", regex=False)
            .str.replace("-", " ", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    # 5. Convertir estrato a número entero
    df["estrato"] = df["estrato"].astype(int)

    # 6. Limpieza y conversión de monto_del_credito a entero
    def clean_monto(val):
        if pd.isna(val):
            return val
        if isinstance(val, (int, float)):
            return int(val)
        s = str(val).strip().replace("$", "").strip()
        # Manejo de decimales y separadores de miles
        if "." in s and "," in s:
            if s.rfind(".") < s.rfind(","):
                s = s.replace(".", "").replace(",", ".")
            else:
                s = s.replace(",", "")
        elif "," in s:
            parts = s.split(",")
            if len(parts) == 2 and len(parts[1]) == 2:
                s = parts[0] + "." + parts[1]
            else:
                s = s.replace(",", "")
        elif "." in s:
            if s.count(".") > 1:
                s = s.replace(".", "")
            else:
                parts = s.split(".")
                if len(parts[1]) == 3:
                    s = parts[0] + parts[1]
        return int(float(s))

    df["monto_del_credito"] = df["monto_del_credito"].apply(clean_monto).astype(int)

    # 7. Unificar formato de fecha a AAAA-MM-DD
    def fix_date(val):
        if pd.isna(val):
            return val
        parts = str(val).strip().replace("-", "/").split("/")
        if len(parts) == 3:
            # Si el año viene al principio (AAAA/MM/DD)
            if len(parts[0]) == 4:
                year, month, day = parts[0], parts[1], parts[2]
            # Si el año viene al final (DD/MM/AAAA)
            else:
                day, month, year = parts[0], parts[1], parts[2]
            return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
        return val

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(fix_date)

    # 8. Eliminar duplicados luego de estandarizar todos los datos
    df = df.drop_duplicates()

    # 9. Guardar el archivo limpio sin el índice de Pandas
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_file, sep=";", index=False)

    return df


if __name__ == "__main__":
    print(pregunta_01())