"""Tests de segmentacion.features (ingeniería RFM) e inflacion."""
import numpy as np

from segmentacion.features import (
    FEATURES_CLUSTERING,
    construir_tabla_clientes,
    aplicar_log_monetary,
    escalar_features,
)
from segmentacion.inflacion import estimar_deflactor, deflactar


def test_construir_tabla_un_cliente_por_fila(df_limpio_min):
    tabla = construir_tabla_clientes(df_limpio_min)
    assert tabla["id_cliente"].nunique() == len(tabla) == 2


def test_construir_tabla_rfm_correcto(df_limpio_min):
    tabla = construir_tabla_clientes(df_limpio_min).set_index("id_cliente")
    # CLI-1 hizo 3 compras; CLI-2 hizo 1
    assert tabla.loc["CLI-1", "frequency"] == 3
    assert tabla.loc["CLI-2", "frequency"] == 1
    # Monetary = suma de montos
    assert tabla.loc["CLI-1", "monetary"] == 180000.0
    # ticket_promedio = monetary / frequency
    assert tabla.loc["CLI-1", "ticket_promedio"] == 60000.0


def test_construir_tabla_recency_no_negativa(df_limpio_min):
    tabla = construir_tabla_clientes(df_limpio_min)
    assert (tabla["recency"] >= 0).all()


def test_recency_menor_que_antiguedad(df_limpio_min):
    """La última compra es siempre >= la primera, así recency <= antiguedad."""
    tabla = construir_tabla_clientes(df_limpio_min)
    assert (tabla["recency"] <= tabla["antiguedad"]).all()


def test_aplicar_log_monetary_monotona(df_limpio_min):
    tabla = aplicar_log_monetary(construir_tabla_clientes(df_limpio_min))
    assert "monetary_log" in tabla.columns
    # log1p es monótona creciente: mayor monetary => mayor monetary_log
    ordenado = tabla.sort_values("monetary")
    assert ordenado["monetary_log"].is_monotonic_increasing


def test_escalar_features_media_cero_std_uno(df_limpio_min):
    tabla = aplicar_log_monetary(construir_tabla_clientes(df_limpio_min))
    # Necesitamos >1 fila; duplicamos artificialmente para el test de escala
    X, scaler = escalar_features(tabla, FEATURES_CLUSTERING)
    assert X.shape == (len(tabla), len(FEATURES_CLUSTERING))
    # media ~ 0 en cada columna
    assert np.allclose(X.mean(axis=0), 0, atol=1e-9)


def test_estimar_deflactor_base_uno(df_inflacion):
    deflactor = estimar_deflactor(df_inflacion)
    # El primer mes es la base: deflactor == 1
    assert abs(deflactor.iloc[0] - 1.0) < 1e-6


def test_estimar_deflactor_creciente(df_inflacion):
    deflactor = estimar_deflactor(df_inflacion)
    # Con inflación positiva, el deflactor crece mes a mes
    assert deflactor.is_monotonic_increasing
    assert deflactor.iloc[-1] > deflactor.iloc[0]


def test_deflactar_reduce_montos_recientes(df_inflacion):
    deflactor = estimar_deflactor(df_inflacion)
    out = deflactar(df_inflacion, deflactor)
    assert "monto_total_real" in out.columns
    # El monto real (en pesos del mes base) es <= nominal salvo en el mes base
    assert (out["monto_total_real"] <= out["monto_total"] + 1e-6).all()
