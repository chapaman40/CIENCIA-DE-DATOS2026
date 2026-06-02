"""Deflactacion por inflacion del campo monto_total.

El README documenta que el dataset tiene inflacion modelada a lo largo de
24 meses (2024-06 a 2026-05). Para que los clientes recientes y antiguos sean
comparables en terminos monetarios reales, se estima un deflactor por mes a
partir de la mediana de monto_total y se ajusta una curva exponencial.

La mediana se prefiere sobre la media porque la distribucion es muy sesgada
por los outliers B2B; la media daria un deflactor inestable.
"""
import numpy as np
import pandas as pd
from loguru import logger
from scipy.optimize import curve_fit


def _modelo_exponencial(t: np.ndarray, a: float, b: float) -> np.ndarray:
    return a * np.exp(b * t)


def estimar_deflactor(df: pd.DataFrame) -> pd.Series:
    """Estima un deflactor mensual a partir de la mediana de monto_total.

    Devuelve una Series indexada por periodo mensual ('YYYY-MM') con el
    deflactor de cada mes (mes base = primer mes del dataset, deflactor = 1).
    """
    df_aux = df[["fecha", "monto_total"]].dropna().copy()
    df_aux = df_aux[df_aux["monto_total"] > 0]
    df_aux["periodo"] = df_aux["fecha"].dt.to_period("M")

    mediana_mes = (
        df_aux.groupby("periodo")["monto_total"]
        .median()
        .sort_index()
    )

    t = np.arange(len(mediana_mes))
    y = mediana_mes.values

    # Ajuste exponencial: log(y) ~ log(a) + b*t (lineal en log)
    log_y = np.log(y)
    b, log_a = np.polyfit(t, log_y, 1)
    a = float(np.exp(log_a))

    # Refinamiento opcional con curve_fit (mas robusto si hay ruido)
    try:
        popt, _ = curve_fit(_modelo_exponencial, t, y, p0=[a, b], maxfev=10000)
        a, b = float(popt[0]), float(popt[1])
    except Exception as exc:
        logger.warning(f"curve_fit fallo, usando polyfit: {exc}")

    valores_ajustados = _modelo_exponencial(t, a, b)
    # Deflactor: cuanto vale 1 ARS del mes t en pesos del mes base (t=0)
    deflactor = valores_ajustados / valores_ajustados[0]

    serie = pd.Series(deflactor, index=mediana_mes.index, name="deflactor")
    logger.info(
        f"Deflactor estimado: a={a:.2f}, b={b:.4f}/mes "
        f"(inflacion mensual ~{(np.exp(b)-1)*100:.2f}%, "
        f"acumulada {(deflactor[-1]-1)*100:.1f}% en {len(serie)} meses)"
    )
    return serie


def deflactar(df: pd.DataFrame, deflactor: pd.Series) -> pd.DataFrame:
    """Agrega columna `monto_total_real` = monto_total / deflactor[mes]."""
    out = df.copy()
    out["periodo"] = out["fecha"].dt.to_period("M")
    out["monto_total_real"] = out["monto_total"] / out["periodo"].map(deflactor)
    out = out.drop(columns=["periodo"])
    logger.info(
        f"Deflactacion aplicada. "
        f"monto_total max nominal: {out['monto_total'].max():,.0f} ARS  ->  "
        f"max real (2024-06): {out['monto_total_real'].max():,.0f} ARS"
    )
    return out
