"""Ingeniería de features RFM y complementarias."""
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.preprocessing import StandardScaler

from segmentacion.config import PROCESSED_DATA_DIR

# Conjuntos de features (definidos en el plan)
FEATURES_CLUSTERING = ["recency", "frequency", "monetary_log"]
FEATURES_CARACTERIZACION = [
    "recency",
    "frequency",
    "monetary",
    "ticket_promedio",
    "diversidad_categorias",
    "antiguedad",
]


def construir_tabla_clientes(
    df: pd.DataFrame,
    fecha_corte: pd.Timestamp | str | None = None,
) -> pd.DataFrame:
    """Agrega el DataFrame transaccional a nivel cliente.

    Columnas generadas:
      - recency: días desde la última compra hasta `fecha_corte`
      - frequency: cantidad de transacciones del cliente
      - monetary: suma de monto_total del cliente
      - ticket_promedio: monetary / frequency  (caracterización)
      - diversidad_categorias: nunique de categoria_producto  (caracterización)
      - antiguedad: días desde la primera compra hasta `fecha_corte`  (caracterización)

    Si `fecha_corte is None`, usa `df['fecha'].max()` y lo logea.
    """
    if fecha_corte is None:
        fecha_corte = df["fecha"].max()
    fecha_corte = pd.Timestamp(fecha_corte)
    logger.info(f"Fecha de corte usada para RFM: {fecha_corte.date()}")

    # Si el dataset trae monto_total_real (deflactado), lo usamos para el Monetary.
    # Mantenemos monetary_nominal para auditoria/comparacion en el EDA.
    if "monto_total_real" in df.columns:
        col_monetary = "monto_total_real"
        agrupado = df.groupby("id_cliente").agg(
            ultima_compra=("fecha", "max"),
            primera_compra=("fecha", "min"),
            frequency=("id_transaccion", "nunique"),
            monetary=(col_monetary, "sum"),
            monetary_nominal=("monto_total", "sum"),
            diversidad_categorias=("categoria_producto", "nunique"),
        )
    else:
        agrupado = df.groupby("id_cliente").agg(
            ultima_compra=("fecha", "max"),
            primera_compra=("fecha", "min"),
            frequency=("id_transaccion", "nunique"),
            monetary=("monto_total", "sum"),
            diversidad_categorias=("categoria_producto", "nunique"),
        )
        agrupado["monetary_nominal"] = agrupado["monetary"]

    agrupado["recency"] = (fecha_corte - agrupado["ultima_compra"]).dt.days
    agrupado["antiguedad"] = (fecha_corte - agrupado["primera_compra"]).dt.days
    agrupado["ticket_promedio"] = agrupado["monetary"] / agrupado["frequency"]

    columnas_finales = [
        "recency",
        "frequency",
        "monetary",
        "monetary_nominal",
        "ticket_promedio",
        "diversidad_categorias",
        "antiguedad",
    ]
    tabla = agrupado[columnas_finales].reset_index()
    logger.info(f"Tabla de clientes: {len(tabla):,} filas x {tabla.shape[1]} columnas")
    return tabla


def aplicar_log_monetary(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega `monetary_log = log1p(monetary)`.

    No transforma recency ni frequency (contadores discretos con distribuciones
    razonables; el log no aporta).
    """
    out = df.copy()
    out["monetary_log"] = np.log1p(out["monetary"])
    return out


def escalar_features(
    df: pd.DataFrame,
    features_clustering: list[str] = FEATURES_CLUSTERING,
) -> tuple[np.ndarray, StandardScaler]:
    """Ajusta StandardScaler sobre `features_clustering` y devuelve (X_escalado, scaler)."""
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features_clustering].values)
    logger.info(f"Features escaladas: {features_clustering} -> shape {X.shape}")
    return X, scaler


def guardar_clientes(df: pd.DataFrame, nombre: str = "clientes_rfm.parquet") -> Path:
    """Persiste la tabla de clientes en data/processed/."""
    path = PROCESSED_DATA_DIR / nombre
    df.to_parquet(path, index=False)
    logger.success(f"Guardado processed: {path}")
    return path
