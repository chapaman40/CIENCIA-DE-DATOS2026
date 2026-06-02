# Makefile para TrabajoFinalApAut
# Ejecuta el pipeline de segmentacion en orden.

.PHONY: help all clean data features train report

help:
	@echo "Targets disponibles:"
	@echo "  make data       - Ejecuta NB1 (EDA + limpieza)"
	@echo "  make features   - Ejecuta NB2 (features RFM + deflactacion)"
	@echo "  make eda        - Ejecuta NB3 (EDA del dataset RFM)"
	@echo "  make train      - Ejecuta NB4 (clustering: K-Means, DBSCAN, Jerarquico, GMM)"
	@echo "  make interpret  - Ejecuta NB5 (interpretacion + estrategias)"
	@echo "  make report     - Genera el PDF del notebook 4"
	@echo "  make all        - Ejecuta el pipeline completo (NB0..NB5)"
	@echo "  make clean      - Borra outputs intermedios"

NBCONV = jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300

resume:
	$(NBCONV) notebooks/0.0-ig-resumen-ejecutivo.ipynb

data:
	$(NBCONV) notebooks/1.0-ig-eda-y-limpieza.ipynb

features:
	$(NBCONV) notebooks/2.0-ig-features-rfm.ipynb

eda:
	$(NBCONV) notebooks/3.0-ig-eda-rfm.ipynb

train:
	$(NBCONV) notebooks/4.0-ig-clustering.ipynb

interpret:
	$(NBCONV) notebooks/5.0-ig-interpretacion-y-estrategias.ipynb

all: data features eda train interpret resume

report:
	jupyter nbconvert --to html notebooks/4.0-ig-clustering.ipynb
	@echo "Generando PDF con Chrome headless..."
	@"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu --no-pdf-header-footer \
		--print-to-pdf="$(CURDIR)/reports/4.0-ig-clustering.pdf" \
		"file:///$(subst \,/,$(CURDIR))/notebooks/4.0-ig-clustering.html"
	rm -f notebooks/4.0-ig-clustering.html

clean:
	rm -f data/interim/*.parquet
	rm -f data/processed/*.parquet
	rm -f models/*.joblib
	rm -f models/comparativos/*.joblib
	rm -f reports/figures/*.png
	rm -f reports/*.pdf
