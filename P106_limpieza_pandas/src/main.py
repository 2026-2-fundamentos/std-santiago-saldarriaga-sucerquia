from pathlib import Path
import re
import numpy as np
import pandas as pd

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = ACTIVITY_DIR / "data" / "ventas.csv"
OUTPUT_FILE = ACTIVITY_DIR / "submission" / "ventas.csv"

EXPECTED_COLUMNS = [
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

SUPPLIER_REPLACEMENTS = {
    "amazon web services colombia": "Amazon Web Services Colombia",
    "BANCOLOMBIA S.A.": "Bancolombia S.A.",
    "Cementos Argos SA": "Cementos Argos S.A.",
    "cementos argos s.a.": "Cementos Argos S.A.",
    "Corona SAS": "Corona S.A.S.",
    "Ecopetrol  S.A.": "Ecopetrol S.A.",
    "GOOGLE COLOMBIA LTDA.": "Google Colombia Ltda.",
    "Grupo  Éxito  S.A.": "Grupo Éxito S.A.",
    "IBM Colombia SAS.": "IBM Colombia S.A.S.",
    "ibm colombia s.a.s.": "IBM Colombia S.A.S.",
    "MICROSOFT COLOMBIA INC.": "Microsoft Colombia Inc.",
    "Nutresa SA": "Nutresa S.A.",
    "nutresa s.a.": "Nutresa S.A.",
    "oracle colombia ltda.": "Oracle Colombia Ltda.",
    "POSTOBÓN S.A.": "Postobon S.A.",
    "SAP Colombia SAS": "SAP Colombia S.A.S.",
    "Schneider  Electric": "Schneider Electric",
    "SIEMENS S.A.S.": "Siemens S.A.S.",
    "siemens s.a.s.": "Siemens S.A.S.",
    "Sura  S.A.": "Sura S.A.",
    "Telefónica  Colombia": "Telefónica Colombia",
}

COUNTRY_REPLACEMENTS = {
    "CO": "COL",
    "COLOMBIA": "COL",
    "Colombia": "COL",
    "colombia": "COL",
}

CITY_REPLACEMENTS = {
    "bogota": "Bogotá",
    "bogotá": "Bogotá",
    "BOGOTÁ": "Bogotá",
    "BOGOTA": "Bogotá",
    "medellin": "Medellín",
    "Medellin": "Medellín",
    "medellín": "Medellín",
    "MEDELLÍN": "Medellín",
    "MEDELLIN": "Medellín",
    "sopo": "Sopó",
    "SOPO": "Sopó",
    "Sopó": "Sopó",
    "Sopo": "Sopó",
    "tenjo": "Tenjo",
    "TENJO": "Tenjo",
    "Tenjo": "Tenjo",
}


def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def clean_supplier_id_column(df):
    if "supplier_id" in df.columns:
        df["supplier_id"] = (
            df["supplier_id"]
            .astype(str)
            .str.replace(r"\D", "", regex=True)
            .astype(int)
        )
    return df


def clean_supplier_column(df):
    df["supplier"] = df["supplier"].astype(str).str.strip()
    df["supplier"] = df["supplier"].replace(SUPPLIER_REPLACEMENTS)
    # Elimina espacios dobles o múltiples
    df["supplier"] = df["supplier"].str.replace(r"\s+", " ", regex=True)
    return df


def clean_country_column(df):
    df["country"] = df["country"].astype(str).str.strip()
    df["country"] = df["country"].replace(COUNTRY_REPLACEMENTS)
    return df


def clean_city_column(df):
    df["city"] = df["city"].astype(str).str.strip()
    df["city"] = df["city"].replace(CITY_REPLACEMENTS)
    return df


def clean_purchase_date_column(df):
    def convert_yyyy_s_mm_s_dd_to_yyyy_mm_dd(series):
        return series.str.replace(r"(\d{4})/(\d{2})/(\d{2})", r"\1-\2-\3", regex=True)

    def convert_mmddyyyy_to_yyyy_mm_dd(series):
        def convert_date(match):
            g1, g2, g3 = match.groups()
            if int(g2) > 12:
                return f"{g3}-{g1}-{g2}"
            return f"{g3}-{g2}-{g1}"

        return series.str.replace(r"(\d{2})/(\d{2})/(\d{4})", convert_date, regex=True)

    def convert_dd_mm_yyyy_to_yyyy_mm_dd_separated_with_dots(series):
        return series.str.replace(r"(\d{2})\.(\d{2})\.(\d{4})", r"\3-\2-\1", regex=True)

    def convert_dd_mm_yy_to_yyyy_mm_dd_separated_with_hyphens(series):
        return series.str.replace(
            r"^(\d{2})-(\d{2})-(\d{2})$", r"20\3-\2-\1", regex=True
        )

    df["purchase_date"] = df["purchase_date"].astype(str).str.strip()
    df["purchase_date"] = convert_yyyy_s_mm_s_dd_to_yyyy_mm_dd(df["purchase_date"])
    df["purchase_date"] = convert_mmddyyyy_to_yyyy_mm_dd(df["purchase_date"])
    df["purchase_date"] = convert_dd_mm_yyyy_to_yyyy_mm_dd_separated_with_dots(
        df["purchase_date"]
    )
    df["purchase_date"] = convert_dd_mm_yy_to_yyyy_mm_dd_separated_with_hyphens(
        df["purchase_date"]
    )
    return df


def clean_amount_column(df):
    def parse_amount(val):
        if pd.isna(val):
            return 0
        val = str(val).strip()
        if val.endswith("K") or val.endswith("k"):
            try:
                return int(float(val[:-1]) * 1000)
            except ValueError:
                pass
        if val.startswith("COP"):
            val = val[3:].strip()
        if val.startswith("$"):
            val = val[1:].strip()
        val = val.replace(".", "").replace(",", "").strip()
        try:
            return int(float(val))
        except ValueError:
            return 0

    df["amount"] = df["amount"].apply(parse_amount).astype(int)
    return df


def clean_discount_column(df):
    def parse_discount(val):
        if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
            return np.nan
        val = str(val).strip().replace("%", "")
        try:
            num = float(val)
            if num > 1.0:
                num = num / 100.0
            return num
        except ValueError:
            return np.nan

    df["discount"] = df["discount"].apply(parse_discount)
    return df


def clean_weight_column(df):
    # Convierte a float y limpia sufijos como 'kg', 'g', etc.
    def parse_weight(val):
        if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
            return np.nan
        val = str(val).strip().lower()
        if val.endswith("kg"):
            val = val[:-2].strip()
        elif val.endswith("g"):
            try:
                return float(val[:-1].strip()) / 1000.0
            except ValueError:
                pass
        val = val.replace(",", ".")
        try:
            return float(val)
        except ValueError:
            return np.nan

    if "weight" in df.columns:
        df["weight"] = df["weight"].apply(parse_weight)
    return df


def clean_units_column(df):
    if "units" in df.columns:
        df["units"] = (
            df["units"]
            .astype(str)
            .str.replace(r"[^\d]", "", regex=True)
        )
        df["units"] = pd.to_numeric(df["units"], errors="coerce")
    return df


def clean_unit_price_column(df):
    if "unit_price" in df.columns:
        df["unit_price"] = (
            df["unit_price"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    return df


def clean_contact_email_column(df):
    if "contact_email" in df.columns:
        df["contact_email"] = df["contact_email"].astype(str).str.strip().str.lower()
    return df


def main():
    df = pd.read_csv(INPUT_FILE)
    df = clean_column_names(df)
    df = clean_supplier_id_column(df)
    df = clean_supplier_column(df)
    df = clean_country_column(df)
    df = clean_city_column(df)
    df = clean_purchase_date_column(df)
    df = clean_amount_column(df)
    df = clean_discount_column(df)
    df = clean_weight_column(df)
    df = clean_units_column(df)
    df = clean_unit_price_column(df)
    df = clean_contact_email_column(df)

    # Asegura orden exacto requerido por el test
    available_cols = [c for c in EXPECTED_COLUMNS if c in df.columns]
    df = df[available_cols]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()