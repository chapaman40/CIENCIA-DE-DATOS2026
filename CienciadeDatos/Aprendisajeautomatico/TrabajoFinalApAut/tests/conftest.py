"""Configuración compartida de pytest: fixtures con datos sintéticos.

Los tests NO dependen del CSV real: construyen DataFrames mínimos que ejercitan
cada función de forma aislada y reproducible.
"""
import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def df_crudo():
    """DataFrame transaccional crudo con las imperfecciones típicas del dataset.

    Incluye a propósito: 1 duplicado exacto, 1 nulo en monto_total, variantes de
    texto en localidad y medio_pago, 1 devolución (monto negativo) y 1 cantidad 0.
    """
    filas = [
        # id_transaccion, id_cliente, fecha, categoria, cantidad, monto, canal, pago, localidad
        ("TX-0001", "CLI-1", "2024-06-10", "Cemento y áridos", 10, 100000.0, "Web", "Transferencia", "Río Grande"),
        ("TX-0002", "CLI-1", "2024-07-15", "Pinturas", 2, 50000.0, "App", "transf.", "río grande"),
        ("TX-0003", "CLI-2", "2024-08-20", "Herramientas manuales", 1, 30000.0, "Web", "T. crédito", "USHUAIA"),
        ("TX-0004", "CLI-2", "2024-09-01", "Plomería", 3, 80000.0, "Telefónico", "Cuenta corriente", "Tohluin"),
        ("TX-0005", "CLI-3", "2025-01-10", "Aberturas", 1, 500000.0, "Web", None, "Ushuaia"),
        # Duplicado exacto de TX-0001
        ("TX-0001", "CLI-1", "2024-06-10", "Cemento y áridos", 10, 100000.0, "Web", "Transferencia", "Río Grande"),
        # Nulo en monto_total (debe dropearse)
        ("TX-0006", "CLI-4", "2025-02-01", "Pisos", 5, None, "Telefónico", "Transferencia", "Río Grande"),
        # Devolución (monto negativo -> filtrar)
        ("TX-0007", "CLI-3", "2025-03-01", "Aberturas", 1, -50000.0, "Web", "Tarjeta de débito", "Ushuaia"),
        # Cantidad cero (-> filtrar)
        ("TX-0008", "CLI-2", "2025-03-05", "Pinturas", 0, 10000.0, "App", "Transferencia", "Río Grande"),
        # Nulo en categoria y localidad
        ("TX-0009", "CLI-5", "2025-04-01", None, 4, 60000.0, "Web", "Transferencia", None),
    ]
    cols = ["id_transaccion", "id_cliente", "fecha", "categoria_producto",
            "cantidad_items", "monto_total", "canal_venta", "medio_pago", "localidad"]
    df = pd.DataFrame(filas, columns=cols)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df


@pytest.fixture
def df_limpio_min():
    """DataFrame ya limpio, para testear la construcción de la tabla de clientes."""
    filas = [
        ("TX-1", "CLI-1", "2024-06-01", "Cemento", 10, 100000.0),
        ("TX-2", "CLI-1", "2024-12-01", "Pinturas", 2, 50000.0),
        ("TX-3", "CLI-1", "2025-06-01", "Plomería", 3, 30000.0),
        ("TX-4", "CLI-2", "2025-05-01", "Aberturas", 1, 900000.0),
    ]
    cols = ["id_transaccion", "id_cliente", "fecha", "categoria_producto",
            "cantidad_items", "monto_total"]
    df = pd.DataFrame(filas, columns=cols)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df


@pytest.fixture
def df_inflacion():
    """Transacciones con inflación exponencial sintética conocida (~5%/mes)."""
    rng = np.random.default_rng(0)
    registros = []
    base = 100000.0
    for mes in range(12):
        fecha = pd.Timestamp("2024-06-01") + pd.DateOffset(months=mes)
        precio_mes = base * (1.05 ** mes)
        for _ in range(30):
            registros.append((fecha, precio_mes * rng.uniform(0.9, 1.1)))
    return pd.DataFrame(registros, columns=["fecha", "monto_total"])


@pytest.fixture
def X_clusters():
    """Datos 2D con 3 grupos bien separados, para testear los entrenadores."""
    rng = np.random.default_rng(42)
    g1 = rng.normal([0, 0], 0.3, size=(50, 2))
    g2 = rng.normal([5, 5], 0.3, size=(50, 2))
    g3 = rng.normal([0, 5], 0.3, size=(50, 2))
    return np.vstack([g1, g2, g3])
