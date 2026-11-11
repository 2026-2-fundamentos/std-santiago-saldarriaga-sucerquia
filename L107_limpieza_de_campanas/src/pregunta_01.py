import glob
import os
import numpy as np
import pandas as pd


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """
    # 1. Leer y concatenar todos los archivos comprimidos
    files = sorted(glob.glob("data/bank-marketing-campaing-*.csv.gz"))
    if not files:
        # Alternativa de ruta en caso de ejecutarse desde otra carpeta
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files = sorted(glob.glob(os.path.join(base_dir, "data", "bank-marketing-campaing-*.csv.gz")))

    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)

    # ==========================================
    # 2. Construcción y limpieza de CLIENT
    # ==========================================
    # Columnas: client_id, age, job, marital, education, credit_default, mortgage
    client = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()

    # En job: eliminar puntos y cambiar guiones por guiones bajos
    client["job"] = (
        client["job"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # En education: cambiar puntos por guiones bajos y 'unknown' a valor faltante (NaN)
    client["education"] = (
        client["education"]
        .astype(str)
        .str.replace(".", "_", regex=False)
        .replace("unknown", np.nan)
    )

    # En credit_default y mortgage: 1 si es 'yes', 0 en cualquier otro caso
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    # ==========================================
    # 3. Construcción y limpieza de CAMPAIGN
    # ==========================================
    # Columnas: client_id, number_contacts, contact_duration,
    # previous_campaign_contacts, previous_outcome, campaign_outcome, last_contact_date
    campaign = df[[
        "client_id",
        "number_contacts",
        "contact_duration",
        "previous_campaign_contacts",
        "previous_outcome",
        "campaign_outcome",
    ]].copy()

    # En previous_outcome: 1 si es 'success', 0 en cualquier otro caso
    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)

    # En campaign_outcome: 1 si es 'yes', 0 en cualquier otro caso
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)

    # Construir last_contact_date con año 2022 y formato AAAA-MM-DD
    # Mapeo de meses abreviados en inglés a número de dos dígitos
    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    month_str = df["month"].astype(str).str.lower().str.strip().map(month_map)
    day_str = df["day"].astype(str).str.strip().str.zfill(2)
    campaign["last_contact_date"] = "2022-" + month_str + "-" + day_str

    # ==========================================
    # 4. Construcción y limpieza de ECONOMICS
    # ==========================================
    # Columnas: client_id, cons_price_idx, euribor_three_months
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()

    # ==========================================
    # 5. Guardar archivos CSV en `submission/`
    # ==========================================
    output_dir = "submission"
    os.makedirs(output_dir, exist_ok=True)

    client.to_csv(os.path.join(output_dir, "client.csv"), index=False)
    campaign.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)
    economics.to_csv(os.path.join(output_dir, "economics.csv"), index=False)

    return client, campaign, economics


if __name__ == "__main__":
    print(clean_campaign_data())