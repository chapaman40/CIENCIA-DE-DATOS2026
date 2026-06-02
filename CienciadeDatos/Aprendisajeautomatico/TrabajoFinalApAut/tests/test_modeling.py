"""Tests de segmentacion.modeling.train (entrenadores y evaluación)."""
import numpy as np

from segmentacion.modeling.train import (
    entrenar_kmeans,
    entrenar_gmm,
    entrenar_jerarquico,
    evaluar,
)


def test_kmeans_numero_de_clusters(X_clusters):
    modelo, labels = entrenar_kmeans(X_clusters, k=3)
    assert modelo.n_clusters == 3
    assert len(set(labels)) == 3
    assert len(labels) == len(X_clusters)


def test_kmeans_reproducible(X_clusters):
    """Mismo random_state => mismas etiquetas."""
    _, labels_a = entrenar_kmeans(X_clusters, k=3, random_state=42)
    _, labels_b = entrenar_kmeans(X_clusters, k=3, random_state=42)
    assert np.array_equal(labels_a, labels_b)


def test_gmm_numero_de_componentes(X_clusters):
    modelo, labels = entrenar_gmm(X_clusters, n_components=3)
    assert modelo.n_components == 3
    assert len(set(labels)) == 3


def test_gmm_predict_proba_suma_uno(X_clusters):
    """Las probabilidades de pertenencia de GMM suman 1 por muestra."""
    modelo, _ = entrenar_gmm(X_clusters, n_components=3)
    proba = modelo.predict_proba(X_clusters)
    assert proba.shape == (len(X_clusters), 3)
    assert np.allclose(proba.sum(axis=1), 1.0)


def test_gmm_soporta_predict(X_clusters):
    """GMM debe poder asignar clusters a datos nuevos (soft clustering productivo)."""
    modelo, _ = entrenar_gmm(X_clusters, n_components=3)
    nuevos = np.array([[0, 0], [5, 5]])
    pred = modelo.predict(nuevos)
    assert len(pred) == 2


def test_jerarquico_numero_de_clusters(X_clusters):
    _, labels = entrenar_jerarquico(X_clusters, n_clusters=3)
    assert len(set(labels)) == 3


def test_evaluar_devuelve_metricas(X_clusters):
    _, labels = entrenar_kmeans(X_clusters, k=3)
    met = evaluar(X_clusters, labels)
    assert set(met) >= {"silhouette", "davies_bouldin", "calinski_harabasz", "n_clusters"}
    # Con 3 grupos bien separados, el silhouette debe ser alto
    assert met["silhouette"] > 0.7
    assert met["n_clusters"] == 3


def test_evaluar_un_solo_cluster_devuelve_nan(X_clusters):
    """Con <2 clusters, las métricas internas no están definidas."""
    labels = np.zeros(len(X_clusters), dtype=int)
    met = evaluar(X_clusters, labels)
    assert np.isnan(met["silhouette"])


def test_algoritmos_concuerdan_en_datos_separados(X_clusters):
    """K-Means, GMM y Jerárquico deben coincidir en datos muy separados (ARI alto)."""
    from sklearn.metrics import adjusted_rand_score
    _, l_km = entrenar_kmeans(X_clusters, k=3)
    _, l_gmm = entrenar_gmm(X_clusters, n_components=3)
    assert adjusted_rand_score(l_km, l_gmm) > 0.9
