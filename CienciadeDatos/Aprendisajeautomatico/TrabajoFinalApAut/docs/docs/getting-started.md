# Getting started

Esta guía explica cómo preparar el entorno y reproducir el análisis completo desde cero.

## 1. Requisitos

- Python 3.10 o superior
- Git (para clonar el repositorio)
- Opcional: Google Chrome (solo para regenerar el PDF del notebook principal)

## 2. Preparar el entorno

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd TrabajoFinalApAut

# Crear y activar un entorno virtual
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate         # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## 3. Datos

El dataset crudo ya está versionado en `data/raw/transacciones_ecommerce.csv`
(10.321 transacciones sintéticas, 1.000 clientes, período 2024-06 a 2026-05).
No hay que descargar nada externo.

Los datos intermedios y procesados (`data/interim/`, `data/processed/`) **no** se
versionan: se regeneran al correr el pipeline.

## 4. Reproducir el pipeline

```bash
# Opción A (recomendada): Makefile
make all          # ejecuta NB1..NB5 en orden
make report       # genera el PDF del notebook 4 (requiere Chrome)

# Opción B: nbconvert manual
jupyter nbconvert --to notebook --execute --inplace notebooks/1.0-ig-eda-y-limpieza.ipynb
# ... y así con cada notebook en orden numérico

# Opción C: exploración interactiva
jupyter notebook
```

**Empezar por** `notebooks/0.0-ig-resumen-ejecutivo.ipynb` — el TL;DR del proyecto.

## 5. Ejecutar los tests

```bash
pytest
```

Los tests (en `tests/`) validan la limpieza de datos, la construcción de features RFM,
la deflactación y los entrenadores de clustering. No dependen del CSV real.

## 6. Outputs que se generan

| Path | Contenido |
|------|-----------|
| `data/interim/transacciones_limpias.parquet` | Dataset limpio |
| `data/processed/clientes_rfm.parquet` | Tabla cliente con RFM |
| `data/processed/clientes_segmentados_nombrados.parquet` | + cluster + segmento comercial |
| `models/modelo_final_kmeans.joblib` | Modelo K-Means de producción |
| `models/comparativos/{dbscan,jerarquico,gmm}.joblib` | Modelos comparativos |
| `reports/figures/*.png` | Figuras del análisis |
| `reports/4.0-ig-clustering.pdf` | PDF del notebook principal |
