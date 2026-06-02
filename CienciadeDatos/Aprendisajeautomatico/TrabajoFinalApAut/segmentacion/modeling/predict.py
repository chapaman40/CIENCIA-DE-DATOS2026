"""Asignación de segmento a clientes nuevos y caracterización de segmentos.

NOTA: La asignación predictiva de este módulo usa K-Means, el modelo de
produccion del proyecto. DBSCAN y AgglomerativeClustering no tienen .predict()
nativo; se usan en el notebook 4 con fines comparativos. GMM sí soporta
.predict(), pero K-Means se prefiere para producción por su simplicidad e
interpretabilidad (estándar en la literatura RFM).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def asignar_segmento(
    modelo_kmeans: KMeans,
    scaler: StandardScaler,
    df_clientes_nuevos: pd.DataFrame,
    features_clustering: list[str],
) -> np.ndarray:
    """Predice el cluster K-Means de clientes nuevos.

    El DataFrame debe traer las columnas listadas en `features_clustering`
    (incluyendo monetary_log si fue una de las features de entrenamiento).
    Solo K-Means es soportado.
    """
    X = scaler.transform(df_clientes_nuevos[features_clustering].values)
    labels = modelo_kmeans.predict(X)
    logger.info(f"Asignados segmentos a {len(labels):,} clientes nuevos")
    return labels


def caracterizar_segmentos(
    df_clientes_originales: pd.DataFrame,
    labels: np.ndarray,
    columna_cluster: str = "cluster",
    columnas_perfil: list[str] | None = None,
) -> pd.DataFrame:
    """Resume cada segmento en unidades originales (no escaladas, no log).

    Hace `merge` (concat por orden) entre la tabla cruda de clientes y las
    etiquetas. Devuelve una tabla con n, %, y media de cada columna de perfil.
    """
    if len(df_clientes_originales) != len(labels):
        raise ValueError(
            f"Tamaños no coinciden: df={len(df_clientes_originales)} "
            f"vs labels={len(labels)}"
        )

    df = df_clientes_originales.copy().reset_index(drop=True)
    df[columna_cluster] = labels

    if columnas_perfil is None:
        columnas_perfil = [
            "recency", "frequency", "monetary", "ticket_promedio",
            "diversidad_categorias", "antiguedad",
        ]
        columnas_perfil = [c for c in columnas_perfil if c in df.columns]

    agregados = df.groupby(columna_cluster)[columnas_perfil].agg(["mean", "median"])
    agregados.columns = [f"{c}_{stat}" for c, stat in agregados.columns]

    tamanos = df.groupby(columna_cluster).size().rename("n_clientes")
    pct = (tamanos / len(df) * 100).round(2).rename("pct_clientes")

    resumen = pd.concat([tamanos, pct, agregados.round(2)], axis=1).reset_index()
    return resumen


def calcular_impacto_monetario(
    df_clientes_originales: pd.DataFrame,
    labels: np.ndarray,
    columna_cluster: str = "cluster",
    columna_monetary: str = "monetary",
) -> pd.DataFrame:
    """% del Monetary total por segmento — input para la estrategia comercial."""
    df = df_clientes_originales.copy().reset_index(drop=True)
    df[columna_cluster] = labels
    total = df[columna_monetary].sum()
    por_segmento = df.groupby(columna_cluster)[columna_monetary].sum()
    pct = (por_segmento / total * 100).round(2)
    return pd.DataFrame({
        "monetary_total": por_segmento.round(2),
        "pct_monetary": pct,
        "n_clientes": df.groupby(columna_cluster).size(),
        "pct_clientes": (df.groupby(columna_cluster).size() / len(df) * 100).round(2),
    }).reset_index()
