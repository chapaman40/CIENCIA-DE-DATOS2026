"""Helpers de visualización reutilizables por los notebooks."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from loguru import logger
from scipy.cluster.hierarchy import dendrogram as _scipy_dendrogram
from scipy.cluster.hierarchy import linkage
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.neighbors import NearestNeighbors


def _save(fig: plt.Figure, output: Path | str | None) -> None:
    if output is not None:
        fig.savefig(output, dpi=120, bbox_inches="tight")
        logger.info(f"Figura guardada: {output}")


def histograma_features(
    df: pd.DataFrame, cols: list[str], output: Path | str | None = None
) -> plt.Figure:
    n = len(cols)
    ncols = min(3, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 3.5 * nrows))
    axes = np.atleast_1d(axes).flatten()
    for ax, col in zip(axes, cols):
        ax.hist(df[col].dropna(), bins=30, color="steelblue", edgecolor="white")
        ax.set_title(f"Distribución de {col}", fontsize=11, fontweight="bold")
        ax.grid(alpha=0.3)
    for ax in axes[n:]:
        ax.set_visible(False)
    plt.tight_layout()
    _save(fig, output)
    return fig


def boxplots_features(
    df: pd.DataFrame, cols: list[str], output: Path | str | None = None
) -> plt.Figure:
    n = len(cols)
    ncols = min(3, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 3.5 * nrows))
    axes = np.atleast_1d(axes).flatten()
    for ax, col in zip(axes, cols):
        ax.boxplot(df[col].dropna(), vert=True, patch_artist=True,
                   boxprops=dict(facecolor="steelblue", alpha=0.6))
        ax.set_title(f"Boxplot {col}", fontsize=11, fontweight="bold")
        ax.grid(alpha=0.3)
    for ax in axes[n:]:
        ax.set_visible(False)
    plt.tight_layout()
    _save(fig, output)
    return fig


def heatmap_correlacion(
    df: pd.DataFrame, cols: list[str], output: Path | str | None = None
) -> plt.Figure:
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                square=True, linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title("Heatmap de correlación", fontsize=12, fontweight="bold")
    plt.tight_layout()
    _save(fig, output)
    return fig


def scatter_clusters_2d(
    X_pca: np.ndarray,
    labels: np.ndarray,
    varianza_explicada: tuple[float, float],
    titulo: str = "Clusters en espacio PCA 2D",
    output: Path | str | None = None,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 6))
    # Outliers en gris si hay -1
    mask_out = labels == -1
    if mask_out.any():
        ax.scatter(X_pca[mask_out, 0], X_pca[mask_out, 1], c="#cccccc",
                   s=15, alpha=0.5, label="Outlier", edgecolors="none")
    sc = ax.scatter(X_pca[~mask_out, 0], X_pca[~mask_out, 1],
                    c=labels[~mask_out], cmap="viridis", s=18,
                    alpha=0.75, edgecolors="none")
    plt.colorbar(sc, ax=ax, label="Cluster")
    pc1, pc2 = varianza_explicada
    ax.set_xlabel(f"PC1 ({pc1*100:.1f}% var)")
    ax.set_ylabel(f"PC2 ({pc2*100:.1f}% var)")
    ax.set_title(
        f"{titulo}\n(varianza explicada PC1+PC2 = {(pc1+pc2)*100:.1f}%)",
        fontsize=12, fontweight="bold",
    )
    if mask_out.any():
        ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    _save(fig, output)
    return fig


def metodo_codo(
    X: np.ndarray,
    k_range: range = range(2, 11),
    output: Path | str | None = None,
) -> tuple[plt.Figure, list[float], list[float]]:
    """Grafica inercia y Silhouette por K (ejes dobles)."""
    inercias, silhouettes = [], []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)
        inercias.append(km.inertia_)
        silhouettes.append(silhouette_score(X, km.labels_))

    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    ax1.plot(list(k_range), inercias, marker="o", color="steelblue",
             linewidth=2, label="Inercia")
    ax1.set_xlabel("Número de clusters (K)")
    ax1.set_ylabel("Inercia", color="steelblue")
    ax1.tick_params(axis="y", labelcolor="steelblue")
    ax1.grid(alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(list(k_range), silhouettes, marker="s", color="tomato",
             linewidth=2, label="Silhouette")
    ax2.set_ylabel("Silhouette score", color="tomato")
    ax2.tick_params(axis="y", labelcolor="tomato")

    ax1.set_title("Método del codo (inercia) + Silhouette por K",
                  fontsize=12, fontweight="bold")
    plt.tight_layout()
    _save(fig, output)
    return fig, inercias, silhouettes


def dendrograma(
    X: np.ndarray,
    output: Path | str | None = None,
    truncate_p: int = 30,
    metodo: str = "ward",
) -> plt.Figure:
    Z = linkage(X, method=metodo)
    fig, ax = plt.subplots(figsize=(10, 5))
    _scipy_dendrogram(Z, truncate_mode="lastp", p=truncate_p, ax=ax,
                      show_leaf_counts=True, leaf_rotation=45,
                      leaf_font_size=9, color_threshold=None)
    ax.set_title(
        f"Dendrograma jerárquico (Ward, truncado a {truncate_p} ramas)",
        fontsize=12, fontweight="bold",
    )
    ax.set_xlabel("Cluster index (n° de muestras agrupadas)")
    ax.set_ylabel("Distancia de fusión")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    _save(fig, output)
    return fig


def grafico_k_distancia(
    X: np.ndarray, k: int = 5, output: Path | str | None = None,
) -> tuple[plt.Figure, np.ndarray]:
    """Ordena la distancia al k-ésimo vecino para elegir eps de DBSCAN."""
    nbrs = NearestNeighbors(n_neighbors=k).fit(X)
    distancias, _ = nbrs.kneighbors(X)
    dist_ordenadas = np.sort(distancias[:, k - 1])[::-1]

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(dist_ordenadas, color="steelblue", linewidth=1.5)
    ax.set_title(f"Gráfico k-distancia (k={k}) — selección de eps para DBSCAN",
                 fontsize=12, fontweight="bold")
    ax.set_xlabel("Puntos ordenados")
    ax.set_ylabel(f"Distancia al {k}° vecino")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    _save(fig, output)
    return fig, dist_ordenadas


def comparar_metricas(
    resultados: dict[str, dict[str, float]],
    output: Path | str | None = None,
) -> plt.Figure:
    """resultados: {'K-Means': {'silhouette': .., 'davies_bouldin': .., 'calinski_harabasz': ..}, ...}"""
    metricas = ["silhouette", "davies_bouldin", "calinski_harabasz"]
    titulos = {
        "silhouette": "Silhouette\n(mayor es mejor)",
        "davies_bouldin": "Davies-Bouldin\n(menor es mejor)",
        "calinski_harabasz": "Calinski-Harabasz\n(mayor es mejor)",
    }
    algoritmos = list(resultados.keys())
    colores = ["steelblue", "tomato", "seagreen", "orange"][:len(algoritmos)]

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    for ax, metr in zip(axes, metricas):
        valores = [resultados[alg].get(metr, np.nan) for alg in algoritmos]
        bars = ax.bar(algoritmos, valores, color=colores, edgecolor="white")
        ax.set_title(titulos[metr], fontsize=11, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        for bar, v in zip(bars, valores):
            if not np.isnan(v):
                # Coloca dentro de la barra si es alta, encima si es chica
                ymax = max(valores) if max(valores) > 0 else 1
                y_pos = v / 2 if v > 0.3 * ymax else v + 0.02 * ymax
                color_text = "white" if v > 0.3 * ymax else "black"
                ax.text(bar.get_x() + bar.get_width()/2, y_pos,
                        f"{v:.3f}", ha="center", va="center",
                        fontsize=10, fontweight="bold", color=color_text)
    fig.suptitle(
        "Comparación de métricas internas (DBSCAN excluye outliers, los otros no)",
        fontsize=12, fontweight="bold",
    )
    plt.tight_layout()
    _save(fig, output)
    return fig


def perfiles_segmentos(
    df_caracterizado: pd.DataFrame,
    columna_cluster: str,
    cols_perfil: list[str],
    output: Path | str | None = None,
) -> plt.Figure:
    """Barras agrupadas: una por feature, barras por cluster (escala original)."""
    perfil = df_caracterizado.groupby(columna_cluster)[cols_perfil].mean()
    n = len(cols_perfil)
    ncols = min(3, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 3.5*nrows))
    axes = np.atleast_1d(axes).flatten()
    for ax, col in zip(axes, cols_perfil):
        perfil[col].plot(kind="bar", ax=ax, color="steelblue", edgecolor="white")
        ax.set_title(f"Media de {col} por segmento", fontsize=10, fontweight="bold")
        ax.set_xlabel("Cluster")
        ax.set_ylabel(col)
        ax.grid(axis="y", alpha=0.3)
        ax.tick_params(axis="x", rotation=0)
    for ax in axes[n:]:
        ax.set_visible(False)
    plt.suptitle("Perfiles de segmentos en unidades originales",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    _save(fig, output)
    return fig


def heatmap_concordancia(
    matriz_ari: pd.DataFrame,
    output: Path | str | None = None,
) -> plt.Figure:
    """Heatmap del Adjusted Rand Index (ARI) entre pares de algoritmos.

    El ARI mide la concordancia entre dos asignaciones de cluster:
    1.0 = particiones idénticas, ~0.0 = coincidencia al azar. Cuantifica
    la afirmación de que los algoritmos encuentran estructuras similares.
    """
    fig, ax = plt.subplots(figsize=(6.5, 5))
    sns.heatmap(matriz_ari, annot=True, fmt=".3f", cmap="YlGnBu",
                vmin=0, vmax=1, square=True, linewidths=0.5, ax=ax,
                cbar_kws={"shrink": 0.8, "label": "Adjusted Rand Index"})
    ax.set_title(
        "Concordancia entre algoritmos (Adjusted Rand Index)\n"
        "1.0 = particiones idénticas | 0.0 = azar",
        fontsize=12, fontweight="bold",
    )
    plt.tight_layout()
    _save(fig, output)
    return fig


def silhouette_plot(
    X: np.ndarray,
    labels: np.ndarray,
    titulo: str = "Silhouette por muestra (K-Means)",
    output: Path | str | None = None,
) -> plt.Figure:
    """Grafica la silueta de cada muestra agrupada por cluster (las 'cuchillas').

    A diferencia del Silhouette promedio (un solo número), este gráfico revela
    si algún cluster tiene muchos puntos con silueta baja o negativa (mal
    asignados). La línea roja marca el Silhouette promedio global.
    """
    sil_values = silhouette_samples(X, labels)
    sil_promedio = silhouette_score(X, labels)
    clusters = sorted(set(labels))

    fig, ax = plt.subplots(figsize=(8, 5))
    y_lower = 10
    cmap = plt.cm.viridis
    for i, c in enumerate(clusters):
        valores_c = np.sort(sil_values[labels == c])
        n_c = len(valores_c)
        y_upper = y_lower + n_c
        color = cmap(i / max(len(clusters) - 1, 1))
        ax.fill_betweenx(np.arange(y_lower, y_upper), 0, valores_c,
                         facecolor=color, edgecolor=color, alpha=0.8)
        ax.text(-0.05, y_lower + 0.5 * n_c, str(c), fontweight="bold")
        y_lower = y_upper + 10

    ax.axvline(x=sil_promedio, color="red", linestyle="--", linewidth=1.5,
               label=f"Promedio = {sil_promedio:.3f}")
    ax.set_title(titulo, fontsize=12, fontweight="bold")
    ax.set_xlabel("Coeficiente de silueta")
    ax.set_ylabel("Muestras agrupadas por cluster")
    ax.legend(loc="lower right")
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    _save(fig, output)
    return fig
