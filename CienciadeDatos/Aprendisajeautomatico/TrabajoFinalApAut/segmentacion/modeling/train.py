"""Entrenamiento y evaluación de algoritmos de clustering."""
from pathlib import Path

import joblib
import numpy as np
from loguru import logger
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)


def entrenar_kmeans(
    X: np.ndarray, k: int, random_state: int = 42, n_init: int = 10,
) -> tuple[KMeans, np.ndarray]:
    """K-Means: único algoritmo con .predict() nativo, es el modelo de produccion."""
    modelo = KMeans(n_clusters=k, random_state=random_state, n_init=n_init)
    labels = modelo.fit_predict(X)
    logger.info(f"K-Means entrenado: K={k}, inercia={modelo.inertia_:.2f}")
    return modelo, labels


def entrenar_dbscan(
    X: np.ndarray, eps: float, min_samples: int = 5,
) -> tuple[DBSCAN, np.ndarray]:
    modelo = DBSCAN(eps=eps, min_samples=min_samples)
    labels = modelo.fit_predict(X)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_outliers = int((labels == -1).sum())
    logger.info(
        f"DBSCAN entrenado: eps={eps}, min_samples={min_samples}, "
        f"clusters={n_clusters}, outliers={n_outliers}"
    )
    return modelo, labels


def entrenar_jerarquico(
    X: np.ndarray, n_clusters: int, linkage: str = "ward",
) -> tuple[AgglomerativeClustering, np.ndarray]:
    modelo = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
    labels = modelo.fit_predict(X)
    logger.info(f"Jerárquico entrenado: n_clusters={n_clusters}, linkage={linkage}")
    return modelo, labels


def entrenar_gmm(
    X: np.ndarray, n_components: int, random_state: int = 42,
    covariance_type: str = "full",
) -> tuple[GaussianMixture, np.ndarray]:
    """GMM: asignación probabilística (soft clustering). Soporta .predict()."""
    modelo = GaussianMixture(
        n_components=n_components,
        covariance_type=covariance_type,
        random_state=random_state,
        n_init=5,
    )
    labels = modelo.fit_predict(X)
    logger.info(
        f"GMM entrenado: n_components={n_components}, "
        f"covariance_type={covariance_type}, "
        f"BIC={modelo.bic(X):.2f}, AIC={modelo.aic(X):.2f}"
    )
    return modelo, labels


def evaluar(
    X: np.ndarray, labels: np.ndarray, excluir_ruido: bool = False,
) -> dict[str, float]:
    """Devuelve diccionario con Silhouette, Davies-Bouldin y Calinski-Harabasz.

    Si `excluir_ruido=True` (caso DBSCAN), filtra label==-1 antes de calcular.
    Si hay menos de 2 clusters validos, devuelve NaN en todas.
    """
    if excluir_ruido:
        mask = labels != -1
        X_eval = X[mask]
        labels_eval = labels[mask]
    else:
        X_eval = X
        labels_eval = labels

    if len(set(labels_eval)) < 2:
        return {
            "silhouette": float("nan"),
            "davies_bouldin": float("nan"),
            "calinski_harabasz": float("nan"),
            "n_clusters": len(set(labels_eval)),
        }

    return {
        "silhouette": silhouette_score(X_eval, labels_eval),
        "davies_bouldin": davies_bouldin_score(X_eval, labels_eval),
        "calinski_harabasz": calinski_harabasz_score(X_eval, labels_eval),
        "n_clusters": len(set(labels_eval)),
    }


def sanity_check_tamanos(labels: np.ndarray, umbral_pct: float = 1.0) -> None:
    """Imprime y advierte si algún cluster es < umbral_pct % del total."""
    total = len(labels)
    valores, conteos = np.unique(labels, return_counts=True)
    logger.info("Tamaños por cluster:")
    for cluster, n in zip(valores, conteos):
        pct = n / total * 100
        marca = "  WARN (cluster trivial)" if pct < umbral_pct and cluster != -1 else ""
        nombre = "Outliers" if cluster == -1 else f"Cluster {cluster}"
        logger.info(f"  {nombre}: {n:,} ({pct:.1f} %){marca}")


def guardar_modelo(modelo, path: Path | str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, path)
    logger.success(f"Modelo guardado: {path}")
    return path


def cargar_modelo(path: Path | str):
    return joblib.load(path)
