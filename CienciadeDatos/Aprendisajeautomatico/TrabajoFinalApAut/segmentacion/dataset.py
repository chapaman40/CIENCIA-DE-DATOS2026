"""Carga y limpieza del dataset transaccional de e-commerce.

Maneja las imperfecciones del dataset sintético descritas en el README:
- Duplicados intencionales (15)
- Nulos en monto_total, medio_pago, localidad, categoria_producto
- Variantes ortográficas en localidad ("RÍO GRANDE", "Tohluin", etc.)
- Abreviaturas en medio_pago ("transf.", "T. crédito")
- Outliers B2B legítimos (no se eliminan)
- Devoluciones (monto_total < 0): se filtran del análisis RFM
"""
from pathlib import Path

import pandas as pd
from loguru import logger

from segmentacion.config import INTERIM_DATA_DIR, RAW_DATA_DIR


# Mapeos canónicos (se aplican antes de los fillna)
MAPEO_LOCALIDAD = {
    "Tohluin": "Tolhuin",
    "Rio Grande": "Río Grande",
}

MAPEO_MEDIO_PAGO = {
    "transf.": "Transferencia",
    "T. crédito": "Tarjeta de crédito",
    "T. débito": "Tarjeta de débito",
}


def cargar_transacciones(path: Path | str | None = None) -> pd.DataFrame:
    """Carga el CSV crudo parseando la columna `fecha`."""
    if path is None:
        path = RAW_DATA_DIR / "transacciones_ecommerce.csv"
    df = pd.read_csv(path, parse_dates=["fecha"])
    logger.info(f"Cargadas {len(df):,} transacciones desde {path}")
    return df


def _normalizar_localidad(s: pd.Series) -> pd.Series:
    """Strip + Title Case + correccion de typos + imputacion de nulos."""
    return (
        s.str.strip()
        .str.title()
        .replace(MAPEO_LOCALIDAD)
        .fillna("Desconocido")
    )


def _normalizar_medio_pago(s: pd.Series) -> pd.Series:
    """Mapeo de abreviaturas a forma canonica + imputacion de nulos."""
    return s.replace(MAPEO_MEDIO_PAGO).fillna("Desconocido")


def _normalizar_categoria(s: pd.Series) -> pd.Series:
    """Imputacion de nulos. Las 12 categorias canonicas estan bien formadas."""
    return s.fillna("Desconocido")


def limpiar_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica los pasos de limpieza definidos en el plan."""
    n_inicial = len(df)
    df_limpio = df.copy()

    n_dup = df_limpio.duplicated().sum()
    df_limpio = df_limpio.drop_duplicates()

    n_null_monto = df_limpio["monto_total"].isnull().sum()
    df_limpio = df_limpio.dropna(subset=["monto_total"])

    n_loc = df_limpio["localidad"].isnull().sum()
    df_limpio["localidad"] = _normalizar_localidad(df_limpio["localidad"])

    n_pago = df_limpio["medio_pago"].isnull().sum()
    df_limpio["medio_pago"] = _normalizar_medio_pago(df_limpio["medio_pago"])

    n_cat = df_limpio["categoria_producto"].isnull().sum()
    df_limpio["categoria_producto"] = _normalizar_categoria(df_limpio["categoria_producto"])

    n_no_pos = (
        (df_limpio["monto_total"] <= 0) | (df_limpio["cantidad_items"] <= 0)
    ).sum()
    df_limpio = df_limpio[
        (df_limpio["monto_total"] > 0) & (df_limpio["cantidad_items"] > 0)
    ]

    logger.info(
        f"Limpieza: {n_inicial:,} -> {len(df_limpio):,} filas. "
        f"Duplicados eliminados: {n_dup}, nulos monto eliminados: {n_null_monto}, "
        f"nulos localidad imputados: {n_loc}, nulos pago imputados: {n_pago}, "
        f"nulos categoria imputados: {n_cat}, no positivos filtrados: {n_no_pos}"
    )
    return df_limpio.reset_index(drop=True)


def guardar_intermedio(df: pd.DataFrame, nombre: str = "transacciones_limpias.parquet") -> Path:
    """Persiste el DataFrame en data/interim/."""
    path = INTERIM_DATA_DIR / nombre
    df.to_parquet(path, index=False)
    logger.success(f"Guardado intermedio: {path}")
    return path
