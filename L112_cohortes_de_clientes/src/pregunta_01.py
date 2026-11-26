"""
Una tienda quiere saber si sus clientes vuelven a comprar después de su
primera compra. Para responder, agrupe a los clientes en cohortes según
el mes de su primera compra y mida, mes a mes, qué proporción de cada
cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

Use estas definiciones:

- `cohort_month`: el mes de la primera compra del cliente, escrito como
`AAAA-MM`.
- `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
- `active_customers`: la cantidad de clientes distintos de la cohorte que
compraron en ese período.
- `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
clientes activos en el período 0.
- `retention_rate`: `active_customers` sobre `cohort_size`.

Genere dos archivos en `submission/`:

1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
  `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
  `retention_rate`, y una fila por cada combinación cohorte–período
  observada, ordenadas por cohorte y período.

2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
  con una fila por cohorte (eje vertical) y una columna por período
  (eje horizontal). Muestre los valores como porcentajes. Los períodos
  que todavía no se pueden observar para una cohorte no significan
  retención cero: déjelos vacíos en el mapa.

La función también debe retornar la tabla de retención.

Ejemplo del formato de `cohort_retention.csv`:

  cohort_month,period_index,active_customers,cohort_size,retention_rate
  2022-01,0,100,100,1.0
  2022-01,1,26,100,0.26
  ...
    """

import os
import matplotlib.pyplot as plt
import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "sales.csv.gz")
    submission_dir = os.path.join(base_dir, "submission")
    os.makedirs(submission_dir, exist_ok=True)

    df = pd.read_csv(file_path, compression="gzip", sep=None, engine="python")
    df.columns = df.columns.str.strip()

    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df["order_period"] = df["OrderDate"].dt.to_period("M")
    
    df["cohort_period"] = df.groupby("CustomerID")["order_period"].transform("min")

    df["period_index"] = (
        df["order_period"].dt.year - df["cohort_period"].dt.year
    ) * 12 + (df["order_period"].dt.month - df["cohort_period"].dt.month)

    df["cohort_month"] = df["cohort_period"].astype(str)

    cohort_retention = (
        df.groupby(["cohort_month", "period_index"], as_index=False)
        .agg(active_customers=("CustomerID", "nunique"))
        .sort_values(["cohort_month", "period_index"])
        .reset_index(drop=True)
    )

    cohort_sizes = cohort_retention[cohort_retention["period_index"] == 0].set_index(
        "cohort_month"
    )["active_customers"]

    cohort_retention["cohort_size"] = cohort_retention["cohort_month"].map(cohort_sizes)
    cohort_retention["retention_rate"] = (
        cohort_retention["active_customers"] / cohort_retention["cohort_size"]
    )

    cohort_retention = cohort_retention[
        [
            "cohort_month",
            "period_index",
            "active_customers",
            "cohort_size",
            "retention_rate",
        ]
    ]

    cohort_retention.to_csv(
        os.path.join(submission_dir, "cohort_retention.csv"), index=False
    )

    pivot_retention = cohort_retention.pivot(
        index="cohort_month", columns="period_index", values="retention_rate"
    )

    fig, ax = plt.subplots(
        figsize=(
            max(8, len(pivot_retention.columns) * 0.9),
            max(5, len(pivot_retention.index) * 0.5),
        )
    )
    im = ax.imshow(pivot_retention.values * 100, aspect="auto", cmap="Blues", vmin=0, vmax=100)

    ax.set_xticks(range(len(pivot_retention.columns)))
    ax.set_xticklabels(pivot_retention.columns)
    ax.set_yticks(range(len(pivot_retention.index)))
    ax.set_yticklabels(pivot_retention.index)

    ax.set_xlabel("Período (meses desde la primera compra)")
    ax.set_ylabel("Cohorte")
    ax.set_title("Tasa de retención por cohorte (%)")

    for i in range(len(pivot_retention.index)):
        for j in range(len(pivot_retention.columns)):
            val = pivot_retention.iloc[i, j]
            if pd.notna(val):
                pct = val * 100
                text_color = "white" if pct > 55 else "black"
                ax.text(j, i, f"{pct:.1f}%", ha="center", va="center", color=text_color, fontsize=8)

    fig.colorbar(im, ax=ax, label="Retención (%)")
    plt.tight_layout()
    plt.savefig(
        os.path.join(submission_dir, "cohort_retention_heatmap.png"),
        bbox_inches="tight",
    )
    plt.close(fig)

    return cohort_retention


if __name__ == "__main__":
    print(build_cohort_analysis())