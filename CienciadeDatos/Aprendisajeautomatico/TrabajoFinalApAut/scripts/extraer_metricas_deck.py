"""Extrae todos los números que consume la presentación desde los parquets/modelos
ya calculados por el pipeline. Reutiliza segmentacion.* para consistencia.

Emite un JSON (stdout + reports/presentacion_html/_metricas_v3.json) con:
counts, fechas, Pareto, perfiles por segmento, ARI, métricas por algoritmo,
arrays del codo (inercia/silueta) y deflactor/ticket.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from segmentacion.features import FEATURES_CLUSTERING, escalar_features  # noqa: E402
from segmentacion.modeling.train import evaluar  # noqa: E402

raw = pd.read_csv(ROOT / "data/raw/transacciones_ecommerce.csv")
interim = pd.read_parquet(ROOT / "data/interim/transacciones_limpias.parquet")
rfm = pd.read_parquet(ROOT / "data/processed/clientes_rfm.parquet")
seg = pd.read_parquet(ROOT / "data/processed/clientes_segmentados_nombrados.parquet")

KEY = {
    "Campeones (B2B)": "champ",
    "Activos Recientes": "active",
    "Esporadicos / En Riesgo": "risk",
    "Perdidos": "lost",
}

out = {}
out["counts"] = dict(
    tx_raw=int(len(raw)),
    tx_clean=int(len(interim)),
    cli_raw=int(raw["id_cliente"].nunique()),
    cli_rfm=int(len(rfm)),
)
raw["fecha"] = pd.to_datetime(raw["fecha"])
nmeses = (raw["fecha"].max().to_period("M") - raw["fecha"].min().to_period("M")).n + 1
out["fechas"] = dict(
    min=str(raw["fecha"].min().date()),
    max=str(raw["fecha"].max().date()),
    meses=int(nmeses),
)

# Pareto a nivel dataset: top 20% de clientes por monetary
m = np.sort(rfm["monetary"].values)[::-1]
out["pareto_top20"] = round(float(m[: int(round(0.2 * len(m)))].sum() / m.sum() * 100), 1)

# Perfiles por segmento
tot = seg["monetary"].sum()
segs = {}
for name, grp in seg.groupby("segmento"):
    segs[KEY[name]] = dict(
        name=name,
        n=int(len(grp)),
        pct=round(len(grp) / len(seg) * 100, 1),
        fact=round(grp["monetary"].sum() / tot * 100, 1),
        R=round(float(grp["recency"].mean()), 1),
        F=round(float(grp["frequency"].mean()), 1),
        M=round(float(grp["monetary"].mean()), 0),
        ticket=round(float(grp["ticket_promedio"].mean()), 0),
        div=round(float(grp["diversidad_categorias"].mean()), 1),
        antig=round(float(grp["antiguedad"].mean()), 0),
    )
out["segments"] = segs

# Métricas por algoritmo (desde las etiquetas guardadas, sobre X escalado)
X, _ = escalar_features(seg, FEATURES_CLUSTERING)
labs = {
    "kmeans": seg["cluster_kmeans"].values,
    "hc": seg["cluster_hc"].values,
    "gmm": seg["cluster_gmm"].values,
    "dbscan": seg["cluster_dbscan"].values,
}
out["metrics"] = {
    "kmeans": evaluar(X, labs["kmeans"]),
    "hc": evaluar(X, labs["hc"]),
    "gmm": evaluar(X, labs["gmm"]),
    "dbscan": evaluar(X, labs["dbscan"], excluir_ruido=True),
}
db_out = int((labs["dbscan"] == -1).sum())
out["dbscan_info"] = dict(outliers=db_out, pct_outliers=round(db_out / len(seg) * 100, 1))

# ARI
out["ari"] = dict(
    kmeans_hc=round(adjusted_rand_score(labs["kmeans"], labs["hc"]), 3),
    kmeans_gmm=round(adjusted_rand_score(labs["kmeans"], labs["gmm"]), 3),
    hc_gmm=round(adjusted_rand_score(labs["hc"], labs["gmm"]), 3),
    kmeans_dbscan=round(adjusted_rand_score(labs["kmeans"], labs["dbscan"]), 3),
)

# Codo + silueta (refit KMeans K=2..10)
iner, sil = [], []
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)
    iner.append(round(float(km.inertia_), 2))
    sil.append(round(float(silhouette_score(X, km.labels_)), 4))
out["elbow"] = dict(
    K=list(range(2, 11)),
    inertia=iner,
    sil=sil,
    k_max_sil=int(np.argmax(sil)) + 2,
    sil_max=round(max(sil), 4),
    inertia_max=round(max(iner), 0),
)

# Crecimiento del ticket nominal (mediana primeros vs últimos 3 meses) → claim "×N"
tmp = interim.copy()
tmp["periodo"] = pd.to_datetime(tmp["fecha"]).dt.to_period("M")
med = tmp.groupby("periodo")["monto_total"].median().sort_index()
out["ticket_growth"] = round(float(med.tail(3).mean() / med.head(3).mean()), 2)

print(json.dumps(out, ensure_ascii=False, indent=2))
dest = ROOT / "reports/presentacion_html/_metricas_v3.json"
json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
