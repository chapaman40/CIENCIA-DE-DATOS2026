"""
Generador de dataset transaccional realista — e-commerce de ferretería en Tierra del Fuego.

Versión v3: 5.000 clientes (escala del original de 1.000). Mismas 9 columnas y mismas
dinámicas; solo cambia la cantidad de clientes (N_CLIENTES).

Dinámicas reales modeladas (lo que separa datos reales de sintéticos "planos"):
  1. INFLACIÓN nominal en pesos (Argentina 2024-06 -> 2026-05): los precios suben mes a mes.
  2. ESTACIONALIDAD de construcción austral: pico en verano (nov-mar), pozo en invierno (jun-ago).
  3. PATRÓN SEMANAL: caída fuerte los domingos, baja los sábados.
  4. SEGMENTOS LATENTES B2B/B2C con Pareto (pocos clientes = mucha facturación).
  5. ACOPLE categoría <-> precio <-> cantidad (el cemento es barato y a granel; las
     herramientas eléctricas caras y de a una).
  6. CORRELACIÓN canal <-> medio de pago <-> segmento (B2B usa cuenta corriente y teléfono).
  7. CICLO DE VIDA del cliente: cohortes de alta, churn, compradores de una sola vez.
  8. IMPERFECCIONES correlacionadas y realistas (no aleatorias uniformes).

Uso:
    python generar_dataset.py                # 5.000 clientes -> data/raw/transacciones_ecommerce.csv
    python generar_dataset.py --n 8000       # otra escala
    python generar_dataset.py --seed 7       # otra semilla
"""

import argparse
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Parámetros (CLI)
# ----------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Genera el dataset sintético de transacciones.")
parser.add_argument("--n", type=int, default=5000, help="Cantidad de clientes (default 5000).")
parser.add_argument("--seed", type=int, default=42, help="Semilla del RNG (default 42).")
parser.add_argument(
    "--out",
    type=str,
    default=str(Path(__file__).resolve().parent / "data" / "raw" / "transacciones_ecommerce.csv"),
    help="Ruta de salida del CSV.",
)
args = parser.parse_args()

rng = np.random.default_rng(args.seed)

FECHA_INI = date(2024, 6, 1)
FECHA_FIN = date(2026, 5, 31)
N_CLIENTES = args.n

# ----------------------------------------------------------------------------
# 1. ÍNDICE DE INFLACIÓN MENSUAL (cumulativo, base jun-2024 = 1.0)
#    Tasas mensuales aproximadas del IPC argentino en desinflación (Milei).
#    De 2025-09 en adelante son estimaciones de continuidad del sendero.
# ----------------------------------------------------------------------------
tasas_mensuales = {
    (2024, 6): 0.046, (2024, 7): 0.040, (2024, 8): 0.042, (2024, 9): 0.035,
    (2024,10): 0.027, (2024,11): 0.024, (2024,12): 0.027,
    (2025, 1): 0.022, (2025, 2): 0.024, (2025, 3): 0.037, (2025, 4): 0.028,
    (2025, 5): 0.015, (2025, 6): 0.016, (2025, 7): 0.019, (2025, 8): 0.019,
    (2025, 9): 0.021, (2025,10): 0.023, (2025,11): 0.020, (2025,12): 0.020,
    (2026, 1): 0.020, (2026, 2): 0.018, (2026, 3): 0.018, (2026, 4): 0.017,
    (2026, 5): 0.016,
}
indice = {}
acum = 1.0
for (y, m), t in tasas_mensuales.items():
    indice[(y, m)] = acum
    acum *= (1 + t)  # el siguiente mes arranca más caro

# ----------------------------------------------------------------------------
# 2. ESTACIONALIDAD (mes) y patrón semanal (día) — hemisferio sur, construcción
# ----------------------------------------------------------------------------
factor_mes = {1:1.30, 2:1.28, 3:1.18, 4:1.00, 5:0.82, 6:0.62,
              7:0.58, 8:0.70, 9:0.92, 10:1.12, 11:1.26, 12:1.34}
factor_dow = {0:1.00, 1:1.05, 2:1.05, 3:1.00, 4:0.95, 5:0.68, 6:0.22}  # lun..dom

# ----------------------------------------------------------------------------
# 3. CATEGORÍAS: precio unitario base (ARS jun-2024), qty lognormal, popularidad
# ----------------------------------------------------------------------------
# (precio_base, mu_log_qty, sigma_log_qty, peso_popularidad_base, sesgo_b2b)
CATS = {
    "Ferretería general":          (3200,  1.6, 0.9, 0.16, 1.0),
    "Herramientas manuales":       (13000, 0.9, 0.8, 0.12, 0.9),
    "Electricidad e iluminación":  (9500,  1.2, 0.9, 0.11, 1.1),
    "Plomería y caños":            (6500,  1.5, 0.9, 0.10, 1.2),
    "Pinturas y revestimientos":   (19000, 1.0, 0.8, 0.09, 1.1),
    "Sanitarios y grifería":       (38000, 0.6, 0.7, 0.08, 1.0),
    "Pisos y cerámicos":           (13000, 2.0, 0.8, 0.08, 1.6),
    "Cemento y áridos":            (8500,  2.6, 0.8, 0.08, 2.4),
    "Seguridad e indumentaria":    (26000, 0.8, 0.7, 0.06, 1.2),
    "Maderas y tableros":          (16000, 1.7, 0.9, 0.05, 2.0),
    "Aberturas":                   (95000, 0.5, 0.7, 0.04, 1.5),
    "Herramientas eléctricas":     (130000,0.2, 0.6, 0.03, 1.1),
}
cat_nombres = list(CATS.keys())
peso_base = np.array([CATS[c][3] for c in cat_nombres])
sesgo_b2b = np.array([CATS[c][4] for c in cat_nombres])

# ----------------------------------------------------------------------------
# 4. SEGMENTOS LATENTES (se usan para generar y luego se "ocultan")
# ----------------------------------------------------------------------------
# nombre: (proporcion, media_n_tx, escala_monto, es_b2b, ventana_dias_tipica)
SEGMENTOS = {
    "B2B_grande":   (0.03, 50, 2.6, True,  720),
    "B2B_pequeno":  (0.12, 24, 1.6, True,  640),
    "B2C_activo":   (0.25, 13, 1.0, False, 600),
    "B2C_ocasional":(0.40, 5.5,0.8, False, 380),
    "B2C_unica":    (0.20, 1.3,0.7, False, 90),
}

# Canal y medio de pago condicionados al segmento (B2B vs B2C)
def perfil_canal_pago(es_b2b):
    if es_b2b:
        canales = ["Telefónico", "App", "Web"]
        p_canal = [0.46, 0.34, 0.20]
        pagos = ["Cuenta corriente", "Transferencia", "Tarjeta de crédito",
                 "Tarjeta de débito", "Efectivo en sucursal"]
        p_pago = [0.55, 0.27, 0.10, 0.05, 0.03]
    else:
        canales = ["Web", "App", "Telefónico"]
        p_canal = [0.66, 0.27, 0.07]
        pagos = ["Tarjeta de débito", "Tarjeta de crédito", "Transferencia",
                 "Efectivo en sucursal", "Cuenta corriente"]
        p_pago = [0.32, 0.28, 0.22, 0.16, 0.02]
    return canales, p_canal, pagos, p_pago

# Localidad por cliente (peso poblacional real de TDF)
LOCS = ["Río Grande", "Ushuaia", "Tolhuin"]
P_LOC = [0.54, 0.38, 0.08]

# ----------------------------------------------------------------------------
# 5. GENERAR CLIENTES (IDs con huecos, cohortes de alta, churn)
# ----------------------------------------------------------------------------
dias_totales = (FECHA_FIN - FECHA_INI).days
fechas_periodo = [FECHA_INI + timedelta(d) for d in range(dias_totales + 1)]

# pesos de fecha (estacionalidad x semana) para muestrear transacciones
peso_fecha = np.array([factor_mes[f.month] * factor_dow[f.weekday()] for f in fechas_periodo])

segs = list(SEGMENTOS.keys())
props = np.array([SEGMENTOS[s][0] for s in segs])
asign = rng.choice(segs, size=N_CLIENTES, p=props/props.sum())

# IDs de cliente con huecos (no perfectamente secuenciales)
ids_disponibles = rng.choice(np.arange(1, int(N_CLIENTES * 1.35)),
                             size=N_CLIENTES, replace=False)
ids_disponibles.sort()
cli_ids = [f"CLI-{i:05d}" for i in ids_disponibles]

clientes = []
for cli_id, seg in zip(cli_ids, asign):
    prop, media_n, escala, es_b2b, ventana = SEGMENTOS[seg]
    # n de transacciones (Poisson, mínimo 1)
    n_tx = max(1, int(rng.poisson(media_n)))
    # alta del cliente: 55% en los primeros 6 meses (base instalada), resto disperso
    if rng.random() < 0.55:
        alta_off = int(rng.integers(0, 183))
    else:
        alta_off = int(rng.integers(0, dias_totales - 30))
    fecha_alta = FECHA_INI + timedelta(alta_off)
    # ventana activa (churn): se corta antes del fin para segmentos ocasionales/únicos
    span = int(min(ventana * rng.uniform(0.6, 1.3), (FECHA_FIN - fecha_alta).days))
    span = max(span, 1)
    fecha_baja = fecha_alta + timedelta(span)
    if fecha_baja > FECHA_FIN:
        fecha_baja = FECHA_FIN
    localidad = rng.choice(LOCS, p=P_LOC)
    clientes.append(dict(id_cliente=cli_id, seg=seg, n_tx=n_tx, escala=escala,
                         es_b2b=es_b2b, fecha_alta=fecha_alta, fecha_baja=fecha_baja,
                         localidad=localidad))

# ----------------------------------------------------------------------------
# 6. GENERAR TRANSACCIONES
# ----------------------------------------------------------------------------
filas = []
idx_fecha = {f: i for i, f in enumerate(fechas_periodo)}

for c in clientes:
    # ventana activa del cliente
    i0 = idx_fecha[c["fecha_alta"]]
    i1 = idx_fecha[c["fecha_baja"]]
    if i1 <= i0:
        i1 = min(i0 + 1, len(fechas_periodo) - 1)
    w = peso_fecha[i0:i1 + 1].copy()
    w = w / w.sum()
    # fechas de las transacciones del cliente
    elegidas = rng.choice(np.arange(i0, i1 + 1), size=c["n_tx"], p=w, replace=True)

    # mezcla de categorías del cliente (sesgada por B2B)
    pesos_cat = peso_base * (sesgo_b2b if c["es_b2b"] else 1/np.sqrt(sesgo_b2b))
    pesos_cat = pesos_cat / pesos_cat.sum()

    for di in elegidas:
        f = fechas_periodo[di]
        cat_i = rng.choice(len(cat_nombres), p=pesos_cat)
        cat = cat_nombres[cat_i]
        precio_base, mu_q, sg_q, _, _ = CATS[cat]
        # cantidad lognormal; B2B compra a mayor escala
        qty = int(np.ceil(rng.lognormal(mu_q, sg_q) * (1.8 if c["es_b2b"] else 1.0)))
        qty = max(1, min(qty, 300))
        infl = indice[(f.year, f.month)]
        ruido = rng.lognormal(0, 0.18)
        monto = precio_base * infl * qty * ruido * c["escala"]
        monto = round(float(monto), 2)

        canales, p_canal, pagos, p_pago = perfil_canal_pago(c["es_b2b"])
        canal = rng.choice(canales, p=p_canal)
        # "Efectivo en sucursal" es incoherente con compra web -> reasignar
        pago = rng.choice(pagos, p=p_pago)
        if canal == "Web" and pago == "Efectivo en sucursal" and rng.random() < 0.85:
            pago = "Transferencia"

        filas.append([None, c["id_cliente"], f, cat, qty, monto, canal, pago, c["localidad"]])

df = pd.DataFrame(filas, columns=["id_transaccion", "id_cliente", "fecha",
    "categoria_producto", "cantidad_items", "monto_total", "canal_venta",
    "medio_pago", "localidad"])

# Ordenar por fecha y asignar IDs de transacción con huecos (no perfectamente secuenciales)
df = df.sort_values("fecha").reset_index(drop=True)
tx_nums = rng.choice(np.arange(1, int(len(df) * 1.25)), size=len(df), replace=False)
tx_nums.sort()
df["id_transaccion"] = [f"TX-{n:06d}" for n in tx_nums]

print("Transacciones base:", len(df), "| Clientes:", df['id_cliente'].nunique())

# ----------------------------------------------------------------------------
# 7. IMPERFECCIONES REALISTAS Y CORRELACIONADAS
# ----------------------------------------------------------------------------
n = len(df)

# 7a. Devoluciones / notas de crédito: monto negativo (~0.8%)
mask_dev = rng.random(n) < 0.008
df.loc[mask_dev, "monto_total"] = -df.loc[mask_dev, "monto_total"].abs().round(2)

# 7b. Outliers extremos legítimos (compras de obra muy grandes) ~0.3%
mask_out = (rng.random(n) < 0.003) & (df["monto_total"] > 0)
df.loc[mask_out, "monto_total"] = (df.loc[mask_out, "monto_total"] * rng.uniform(6, 14, mask_out.sum())).round(2)

# 7c. Nulos correlacionados (no uniformes):
#     - monto_total nulo cuando falla la pasarela de pago, más en Telefónico (~0.6%)
p_null_monto = np.where(df["canal_venta"] == "Telefónico", 0.018, 0.004)
df.loc[rng.random(n) < p_null_monto, "monto_total"] = np.nan
#     - medio_pago nulo (registro incompleto) ~1.1%
df.loc[rng.random(n) < 0.011, "medio_pago"] = np.nan
#     - localidad nula ~0.4%
df.loc[rng.random(n) < 0.004, "localidad"] = np.nan
#     - categoria nula (carga manual incompleta) ~0.25%
df.loc[rng.random(n) < 0.0025, "categoria_producto"] = np.nan

# 7d. Inconsistencia de texto en localidad (carga libre por distintos operadores)
def ensuciar_loc(v):
    if pd.isna(v):
        return v
    r = rng.random()
    if r < 0.06:   return v.upper()
    if r < 0.11:   return v.lower()
    if r < 0.15:   return v.replace("í", "i").replace("ó", "o")  # sin acento
    if r < 0.17:   return v + " "                                # espacio sobrante
    if r < 0.175 and v.startswith("Tol"): return "Tohluin"       # typo ocasional
    return v
df["localidad"] = df["localidad"].apply(ensuciar_loc)

# 7e. Inconsistencia de texto en medio_pago (abreviaturas)
def ensuciar_pago(v):
    if pd.isna(v):
        return v
    r = rng.random()
    if v == "Transferencia" and r < 0.04:        return "transf."
    if v == "Tarjeta de débito" and r < 0.04:    return "T. débito"
    if v == "Tarjeta de crédito" and r < 0.04:   return "T. crédito"
    return v
df["medio_pago"] = df["medio_pago"].apply(ensuciar_pago)

# 7f. Duplicados exactos (doble submit del formulario) ~0.15%
n_dup = int(n * 0.0015)
dup_idx = rng.choice(df.index, size=n_dup, replace=False)
df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)
df = df.sort_values("fecha").reset_index(drop=True)

# ----------------------------------------------------------------------------
# 8. GUARDAR
# ----------------------------------------------------------------------------
df_out = df[["id_transaccion", "id_cliente", "fecha", "categoria_producto",
             "cantidad_items", "monto_total", "canal_venta", "medio_pago", "localidad"]].copy()
df_out["fecha"] = pd.to_datetime(df_out["fecha"]).dt.strftime("%Y-%m-%d")

out_path = Path(args.out)
out_path.parent.mkdir(parents=True, exist_ok=True)
df_out.to_csv(out_path, index=False)
print("Total filas finales (con dups):", len(df_out))
print("Clientes únicos:", df_out['id_cliente'].nunique())
print("Guardado en:", out_path)
