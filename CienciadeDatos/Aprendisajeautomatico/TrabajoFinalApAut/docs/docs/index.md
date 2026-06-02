# Segmentación de Clientes — E-commerce de Ferretería (TDF)

Proyecto de aprendizaje automático **no supervisado** que segmenta a los clientes de un
e-commerce de ferretería y materiales de construcción de Tierra del Fuego, combinando la
metodología **RFM** (Recency, Frequency, Monetary) con algoritmos de **clustering**
(K-Means, DBSCAN, Jerárquico Aglomerativo y Gaussian Mixture Models).

## Resultado principal

Se identificaron **4 segmentos** mediante K-Means sobre features RFM deflactadas por
inflación. El hallazgo clave es un **Pareto comercial muy marcado**: el **15 % de los
clientes (Campeones B2B) explica el 77 % de la facturación real**.

| Segmento | % Clientes | % Facturación real | Estrategia |
|----------|-----------|--------------------|------------|
| 🏆 Campeones (B2B) | 15.4 % | **76.7 %** | Programa premium, cuenta corriente |
| 🛒 Activos Recientes | 30.6 % | 16.4 % | Up-sell, programa de puntos |
| ⚠️ Esporádicos / En Riesgo | 32.2 % | 5.6 % | Campaña de re-activación |
| 💤 Perdidos | 21.7 % | 1.2 % | Win-back de bajo costo |

## Estructura de la documentación

- **Getting started** — cómo instalar el entorno y reproducir el pipeline completo.
- **README del repositorio** — descripción extensa del problema, objetivos y metodología.
- `references/glosario.md` — glosario de términos técnicos (RFM, Silhouette, ARI, GMM, etc.).
- `references/DESCRIPCION_dataset_v2.md` — diccionario de datos del CSV crudo.

## El pipeline en 5 notebooks

1. **NB1** — EDA y limpieza del dataset transaccional.
2. **NB2** — Ingeniería de features RFM + deflactación por inflación.
3. **NB3** — EDA del dataset RFM (correlaciones, B2B vs B2C).
4. **NB4** ⭐ — Clustering: K-Means, DBSCAN, Jerárquico y GMM. Comparación y selección.
5. **NB5** — Interpretación comercial, nombramiento de segmentos y estrategias de marketing.
