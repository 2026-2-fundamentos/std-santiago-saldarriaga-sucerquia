import json
import os
import re
import pandas as pd


def main():
    """
        Antes de limpiar o analizar un conjunto de datos, un analista debe
        documentar qué problemas tiene. En este laboratorio usted no va a limpiar
        `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
        de sus problemas, tal como están en el archivo.
    
        Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
        encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
        inicio y al final (y cualquier marca BOM) y reemplace los espacios
        internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
        `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
        `units`, `unit_price` y `contact_email`.
    
        Escriba el reporte en `submission/data_quality_report.json` con estas
        claves:
    
        - `row_count`: cantidad de filas de datos.
        - `column_count`: cantidad de columnas.
        - `missing_required_columns`: lista ordenada de columnas requeridas que no
          están en el archivo.
        - `unexpected_columns`: lista ordenada de columnas del archivo que no son
          requeridas.
        - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
        - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
          aparece más de una vez (cuente todas esas filas, no solo las
          repetidas).
        - `missing_value_count_by_column`: diccionario con la cantidad de valores
          faltantes de cada columna. Considere faltantes las celdas vacías y las
          que contienen `N/A`.
        - `invalid_email_count`: cantidad de valores de `contact_email` que no
          tienen la forma `usuario@dominio.extension`.
        - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
          enteros positivos. Los valores faltantes no se cuentan aquí.
        - `country_values`: lista ordenada de los valores distintos de `country`,
          escritos exactamente como aparecen en el archivo.
    
        La función también debe retornar el reporte como un diccionario.
    
        Ejemplo del formato del reporte:
    
            {
              "row_count": 103,
              "column_count": 11,
              "missing_required_columns": [],
              ...
              "country_values": [" Colombia ", "CO", ...]
            }
        """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "ventas.csv.gz")
    output_dir = os.path.join(base_dir, "submission")
    output_file = os.path.join(output_dir, "data_quality_report.json")

    required_columns = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email",
    ]

    df = pd.read_csv(
        file_path,
        compression="gzip",
        dtype=str,
        keep_default_na=True,
        na_values=["N/A"],
    )

    def normalize_col(col):
        col = str(col).lstrip("\ufeff").strip().lower()
        return re.sub(r"\s+", "_", col)

    df.columns = [normalize_col(c) for c in df.columns]

    actual_columns = list(df.columns)

    row_count = int(len(df))
    column_count = int(len(actual_columns))

    missing_required_columns = sorted(
        [col for col in required_columns if col not in actual_columns]
    )
    unexpected_columns = sorted(
        [col for col in actual_columns if col not in required_columns]
    )

    duplicate_row_count = int(df.duplicated().sum())

    if "supplier_id" in df.columns:
        supplier_id_clean = df["supplier_id"].dropna()
        duplicate_supplier_id_row_count = int(
            df["supplier_id"].isin(
                supplier_id_clean[supplier_id_clean.duplicated()].unique()
            ).sum()
        )
    else:
        duplicate_supplier_id_row_count = 0

    missing_value_count_by_column = {
        col: int(df[col].isna().sum()) for col in actual_columns
    }

    invalid_email_count = 0
    if "contact_email" in df.columns:
        email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        for val in df["contact_email"].dropna():
            if not email_regex.match(str(val)):
                invalid_email_count += 1

    invalid_unit_count = 0
    if "units" in df.columns:
        for val in df["units"].dropna():
            try:
                num = float(val)
                if not (num.is_integer() and num > 0):
                    invalid_unit_count += 1
            except (ValueError, TypeError):
                invalid_unit_count += 1

    if "country" in df.columns:
        country_values = sorted(df["country"].dropna().unique().tolist())
    else:
        country_values = []

    report = {
        "row_count": row_count,
        "column_count": column_count,
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values,
    }

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report


if __name__ == "__main__":
    print(main())