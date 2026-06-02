"""Tests de segmentacion.dataset (carga y limpieza)."""
from segmentacion.dataset import (
    limpiar_dataset,
    _normalizar_localidad,
    _normalizar_medio_pago,
)
import pandas as pd


def test_limpiar_elimina_duplicados(df_crudo):
    limpio = limpiar_dataset(df_crudo)
    assert limpio.duplicated().sum() == 0


def test_limpiar_dropea_nulos_de_monto(df_crudo):
    limpio = limpiar_dataset(df_crudo)
    assert limpio["monto_total"].isnull().sum() == 0


def test_limpiar_filtra_no_positivos(df_crudo):
    """Devoluciones (monto<0) y cantidad<=0 deben quedar fuera."""
    limpio = limpiar_dataset(df_crudo)
    assert (limpio["monto_total"] > 0).all()
    assert (limpio["cantidad_items"] > 0).all()


def test_limpiar_normaliza_localidad(df_crudo):
    limpio = limpiar_dataset(df_crudo)
    # No deben quedar variantes: todo en Title Case canónico o 'Desconocido'
    validas = {"Río Grande", "Ushuaia", "Tolhuin", "Desconocido"}
    assert set(limpio["localidad"].unique()).issubset(validas)


def test_limpiar_no_deja_nulos_en_categoricas(df_crudo):
    limpio = limpiar_dataset(df_crudo)
    for col in ["medio_pago", "localidad", "categoria_producto"]:
        assert limpio[col].isnull().sum() == 0


def test_normalizar_localidad_corrige_typo():
    s = pd.Series(["Tohluin", "RÍO GRANDE", "  ushuaia "])
    out = _normalizar_localidad(s)
    assert list(out) == ["Tolhuin", "Río Grande", "Ushuaia"]


def test_normalizar_medio_pago_mapea_abreviaturas():
    s = pd.Series(["transf.", "T. crédito", "T. débito", None])
    out = _normalizar_medio_pago(s)
    assert list(out) == [
        "Transferencia", "Tarjeta de crédito", "Tarjeta de débito", "Desconocido",
    ]


def test_limpiar_reduce_filas(df_crudo):
    """La limpieza nunca debe agregar filas."""
    limpio = limpiar_dataset(df_crudo)
    assert len(limpio) < len(df_crudo)
