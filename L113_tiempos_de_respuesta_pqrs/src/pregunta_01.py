"""
Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
(PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
hábiles para responder cada una. Su tarea es medir si la entidad cumple
ese plazo.

Los archivos `data/historical_requests_web.csv.gz` y
`data/historical_requests_letter.csv.gz` tienen una fila por solicitud
recibida entre 2016 y 2021 por cada canal, con su identificador
(`record_id`), la fecha de entrada (`in_date`), el día de la semana de
entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
está vacía, la solicitud todavía no ha sido respondida.

Tenga en cuenta lo siguiente:

- Algunas solicitudes aparecen repetidas: elimine las filas idénticas
  dentro de cada canal, para contar cada solicitud una sola vez. Las
  filas sin `record_id` son solicitudes válidas.
- Llame `letter` al canal de las cartas y `web` al de la página web.
- Los días hábiles de respuesta son los días de lunes a viernes
  posteriores a la fecha de entrada, hasta la fecha de respuesta
  incluida. Por ejemplo, una solicitud que entra un viernes y se responde
  el lunes siguiente tardó 1 día hábil. No considere los festivos.
- Los días calendario de respuesta son la diferencia entre la fecha de
  respuesta y la de entrada.
- Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
  menos. Una solicitud pendiente no ha cumplido el plazo.
- `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
  sobre el total de solicitudes, incluidas las pendientes.
- Las medianas de días se calculan solamente con las solicitudes
  respondidas.

Genere tres archivos en `submission/`, sin el índice de Pandas y con las
columnas en el orden indicado:

1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
    `channel`, `requests`, `answered`, `pending`,
    `median_business_days` y `on_time_rate`.

2. `yearly_summary.csv`, con una fila por año de entrada y canal,
    ordenada por año y luego por canal: `year`, `channel`, `requests`,
    `pending` y `on_time_rate`.

3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
    domingo, con los dos canales juntos: `day_name`, `requests`,
    `median_calendar_days` y `median_business_days`.

Observe en el tercer archivo cómo cambia la lectura del tiempo de
respuesta según se cuenten días calendario o días hábiles.

La función también debe retornar las tres tablas, en el mismo orden.

Ejemplo del formato de `channel_summary.csv`:

    channel,requests,answered,pending,median_business_days,on_time_rate
    letter,28138,...
    ...
"""

  


import os
import numpy as np
import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    submission_dir = os.path.join(base_dir, "submission")
    os.makedirs(submission_dir, exist_ok=True)

    channels = {
        "letter": "historical_requests_letter.csv.gz",
        "web": "historical_requests_web.csv.gz",
    }

    frames = []
    for channel_name, filename in channels.items():
        file_path = os.path.join(data_dir, filename)
        df_ch = pd.read_csv(
            file_path,
            compression="gzip",
            sep=None,
            engine="python",
            dtype=str,
        )
        df_ch.columns = df_ch.columns.str.strip()

        for col in df_ch.columns:
            df_ch[col] = df_ch[col].where(df_ch[col].isna(), df_ch[col].str.strip())
            df_ch[col] = df_ch[col].replace("", np.nan)

        df_ch = df_ch.drop_duplicates().copy()
        df_ch["channel"] = channel_name
        frames.append(df_ch)

    df = pd.concat(frames, ignore_index=True)

    df["in_dt"] = pd.to_datetime(df["in_date"])
    df["out_dt"] = pd.to_datetime(df["out_date"], errors="coerce")

    df["is_answered"] = df["out_dt"].notna()
    df["is_pending"] = ~df["is_answered"]
    df["year"] = df["in_dt"].dt.year

    df["calendar_days"] = (df["out_dt"] - df["in_dt"]).dt.days

    df["business_days"] = np.nan
    answered_mask = df["is_answered"]
    in_dates_arr = (df.loc[answered_mask, "in_dt"] + pd.Timedelta(days=1)).values.astype("datetime64[D]")
    out_dates_arr = (df.loc[answered_mask, "out_dt"] + pd.Timedelta(days=1)).values.astype("datetime64[D]")
    df.loc[answered_mask, "business_days"] = np.busday_count(in_dates_arr, out_dates_arr)

    df["on_time"] = df["is_answered"] & (df["business_days"] <= 15)

    channel_summary = (
        df.groupby("channel", as_index=False)
        .agg(
            requests=("channel", "size"),
            answered=("is_answered", "sum"),
            pending=("is_pending", "sum"),
            median_business_days=("business_days", "median"),
            on_time_count=("on_time", "sum"),
        )
        .sort_values("channel")
        .reset_index(drop=True)
    )
    channel_summary["on_time_rate"] = (
        channel_summary["on_time_count"] / channel_summary["requests"]
    )
    channel_summary = channel_summary[
        [
            "channel",
            "requests",
            "answered",
            "pending",
            "median_business_days",
            "on_time_rate",
        ]
    ]

    yearly_summary = (
        df.groupby(["year", "channel"], as_index=False)
        .agg(
            requests=("channel", "size"),
            pending=("is_pending", "sum"),
            on_time_count=("on_time", "sum"),
        )
        .sort_values(["year", "channel"])
        .reset_index(drop=True)
    )
    yearly_summary["on_time_rate"] = (
        yearly_summary["on_time_count"] / yearly_summary["requests"]
    )
    yearly_summary = yearly_summary[
        ["year", "channel", "requests", "pending", "on_time_rate"]
    ]

    df["dow_num"] = df["in_dt"].dt.dayofweek
    entry_day_summary = (
        df.groupby(["dow_num", "day_name"], as_index=False)
        .agg(
            requests=("channel", "size"),
            median_calendar_days=("calendar_days", "median"),
            median_business_days=("business_days", "median"),
        )
        .sort_values("dow_num")
        .reset_index(drop=True)
    )
    entry_day_summary = entry_day_summary[
        ["day_name", "requests", "median_calendar_days", "median_business_days"]
    ]

    channel_summary.to_csv(
        os.path.join(submission_dir, "channel_summary.csv"), index=False
    )
    yearly_summary.to_csv(
        os.path.join(submission_dir, "yearly_summary.csv"), index=False
    )
    entry_day_summary.to_csv(
        os.path.join(submission_dir, "entry_day_summary.csv"), index=False
    )

    return channel_summary, yearly_summary, entry_day_summary


if __name__ == "__main__":
    print(pregunta_01())