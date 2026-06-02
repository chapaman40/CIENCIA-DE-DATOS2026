# Glosario de términos técnicos

> Lista alfabética de términos usados a lo largo del proyecto. Pensado para lectores que vienen
> del mundo del negocio o que no son expertos en ciencia de datos.

| Término | Definición breve |
|---------|------------------|
| **AIC** | Akaike Information Criterion. Criterio para comparar modelos: penaliza la complejidad. **Menor es mejor**. Usado en GMM para elegir n° de componentes. |
| **B2B / B2C** | Business-to-Business / Business-to-Consumer. En este proyecto: empresas constructoras (B2B) vs. clientes particulares (B2C). |
| **BIC** | Bayesian Information Criterion. Similar al AIC pero con penalización más fuerte por complejidad. **Menor es mejor**. Preferido sobre AIC cuando la muestra es grande. |
| **Calinski-Harabasz Index** | Métrica de calidad de clustering: razón entre dispersión inter-cluster e intra-cluster. **Mayor es mejor**. |
| **Clustering** | Familia de algoritmos no supervisados que agrupan datos por similitud sin etiquetas previas. |
| **CCDS** | Cookiecutter Data Science — plantilla estándar de proyecto de ciencia de datos. |
| **CRISP-DM** | Cross-Industry Standard Process for Data Mining. Metodología de 6 fases. |
| **Davies-Bouldin Index** | Métrica de clustering: promedio de la similitud entre pares de clusters. **Menor es mejor** (mín = 0). |
| **DBSCAN** | Density-Based Spatial Clustering. Encuentra clusters como regiones densas; etiqueta puntos aislados como ruido (-1). |
| **Deflactación** | Ajuste de valores monetarios para descontar el efecto de la inflación. Lleva todos los pesos a un mismo poder adquisitivo. |
| **Dendrograma** | Diagrama de árbol que muestra cómo se van fusionando los clusters en el clustering jerárquico aglomerativo. |
| **EDA** | Exploratory Data Analysis. Análisis exploratorio de datos. |
| **Feature** | Variable o columna usada como entrada de un modelo. |
| **Gaussian Mixture Model (GMM)** | Algoritmo de clustering probabilístico. Asigna a cada punto una probabilidad de pertenencia a cada cluster (soft clustering), a diferencia de K-Means que asigna de forma determinista. Soporta clusters elípticos. |
| **Frequency** | F del RFM. Cantidad de transacciones distintas del cliente en el período. |
| **K-Means** | Algoritmo de clustering basado en centroides. Requiere fijar K (n° de clusters) a priori. |
| **Jerárquico Aglomerativo (HC)** | Algoritmo de clustering que empieza con cada punto como cluster individual y los va fusionando por proximidad. |
| **log1p** | `log(1+x)`. Transformación que comprime valores grandes y maneja ceros sin error. Útil para variables sesgadas como `monetary`. |
| **Método del codo** | Heurística para elegir K en K-Means: graficar la inercia por K y buscar el "codo" donde la mejora marginal se aplana. |
| **Monetary** | M del RFM. Suma de gasto del cliente en el período. |
| **Outlier** | Observación atípica, muy alejada del resto. Puede ser un error o un caso legítimo extremo (ej. cliente B2B mayorista). |
| **Pareto comercial** | Patrón empírico donde un grupo minoritario de clientes explica la mayor parte de la facturación (regla 80/20). |
| **PCA** | Principal Component Analysis. Reduce dimensionalidad proyectando a las direcciones de máxima varianza. |
| **Parquet** | Formato de archivo columnar. Más rápido y compacto que CSV para datasets tabulares. |
| **Random state / seed** | Semilla de aleatoriedad. Fijarla (`random_state=42`) hace los experimentos reproducibles. |
| **Recency** | R del RFM. Días desde la última compra del cliente hasta la fecha de corte. |
| **RFM** | Recency, Frequency, Monetary. Marco clásico de segmentación de clientes basado en 3 dimensiones de comportamiento de compra. |
| **Silhouette Score** | Métrica de clustering: qué tan parecido es un punto a su cluster vs a otros clusters. Rango [-1, 1]. **Mayor es mejor**. |
| **StandardScaler** | Transformador que centra cada feature (media=0) y la escala a desviación estándar 1. Necesario antes de K-Means/DBSCAN. |
| **Winsorización** | Truncar outliers al percentil 95 (o 99). En este proyecto NO se aplica: los outliers B2B son legítimos. |
