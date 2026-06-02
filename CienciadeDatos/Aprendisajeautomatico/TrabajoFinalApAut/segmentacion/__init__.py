"""segmentacion - Paquete de segmentacion de clientes mediante RFM + clustering.

API publica del paquete: las funciones mas comunmente usadas se exportan aqui para
permitir imports directos como `from segmentacion import construir_tabla_clientes`.
"""

from segmentacion.dataset import (
    cargar_transacciones,
    limpiar_dataset,
    guardar_intermedio,
)
from segmentacion.features import (
    FEATURES_CLUSTERING,
    FEATURES_CARACTERIZACION,
    construir_tabla_clientes,
    aplicar_log_monetary,
    escalar_features,
    guardar_clientes,
)
from segmentacion.inflacion import (
    estimar_deflactor,
    deflactar,
)
from segmentacion.modeling.train import (
    entrenar_kmeans,
    entrenar_dbscan,
    entrenar_jerarquico,
    entrenar_gmm,
    evaluar,
    sanity_check_tamanos,
    guardar_modelo,
    cargar_modelo,
)
from segmentacion.modeling.predict import (
    asignar_segmento,
    caracterizar_segmentos,
    calcular_impacto_monetario,
)

__all__ = [
    "FEATURES_CLUSTERING",
    "FEATURES_CARACTERIZACION",
    "cargar_transacciones", "limpiar_dataset", "guardar_intermedio",
    "construir_tabla_clientes", "aplicar_log_monetary", "escalar_features", "guardar_clientes",
    "estimar_deflactor", "deflactar",
    "entrenar_kmeans", "entrenar_dbscan", "entrenar_jerarquico", "entrenar_gmm",
    "evaluar", "sanity_check_tamanos", "guardar_modelo", "cargar_modelo",
    "asignar_segmento", "caracterizar_segmentos", "calcular_impacto_monetario",
]
