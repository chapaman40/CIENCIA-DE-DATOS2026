# 🎬 Guion del video — Segmentación de Clientes (deck HTML)
### Trabajo Final de Aprendizaje Automático · Ian Gallego

> **Duración objetivo:** 6:30 – 7:00 min · **Ritmo:** ~145 palabras/min (hablar pausado).
> Avanzá los slides con **→ / espacio**. `F` = pantalla completa. Cada bloque indica el **slide**,
> el **tiempo acumulado** y el **texto a leer**. Los `[ ]` son acotaciones, no se leen.

| Bloque (consigna) | Slides | Tiempo | Acum. |
|---|---|---|---|
| Introducción + organización | 1 · 2 · 3 | 1:00 | 1:00 |
| Descripción del dataset | 4 · 5 | 1:30 | 2:30 |
| Desarrollo del modelo | 6 · 7 | 2:00 | 4:30 |
| Análisis de resultados | 8 · 9 | 1:30 | 6:00 |
| Conclusiones y recomendaciones | 10 · 11 | 1:00 | 7:00 |

---

## 🟧 BLOQUE 1 — Introducción y organización · `0:00 → 1:00`

**[Slide 1 · Portada] (0:00–0:12)**
> Hola, soy Ian Gallego. Les presento mi trabajo final de Aprendizaje Automático: la
> **segmentación de clientes** de un e-commerce de ferretería de Tierra del Fuego, usando
> la metodología RFM combinada con clustering no supervisado.

**[Slide 2 · El problema] (0:12–0:38)**
> El negocio tiene una cartera muy diversa: conviven **constructoras y contratistas B2B** de
> alto volumen con **particulares B2C** que compran para una refacción puntual. Hoy el
> marketing se envía masivo y uniforme a todos por igual, y eso provoca presupuesto
> desperdiciado, baja conversión, fuga de clientes valiosos y un segmento B2B subaprovechado.

**[Slide 3 · Objetivo y organización] (0:38–1:00)**
> El objetivo es **segmentar a los clientes en grupos homogéneos** según su comportamiento de
> compra, para diseñar acciones personalizadas. El proyecto es **100% reproducible**: versionado
> en Git, estructurado con Cookiecutter Data Science, con un pipeline que se ejecuta en un solo
> comando y código modular con tests.

---

## 🟧 BLOQUE 2 — Descripción del dataset · `1:00 → 2:30`

**[Slide 4 · El dataset] (1:00–1:45)**
> El dataset tiene **50.730 transacciones de 5.000 clientes**, 9 variables, a lo largo de 24
> meses. Es **sintético**: por confidencialidad de la empresa real lo generé en Python con
> semilla fija, para que sea reproducible. Pero no es aleatorio: **replica dinámicas reales** del
> rubro —la inflación en pesos que multiplica el ticket por más de dos en dos años, la
> estacionalidad austral, y la concentración Pareto donde el 20% de clientes hace el 81% de la
> facturación. Las variables RFM no vienen en el archivo: se derivan agrupando por cliente.

**[Slide 5 · Del dato crudo al perfil RFM] (1:45–2:30)**
> El preprocesamiento tuvo cinco pasos: **limpieza** de nulos y devoluciones, **normalización**
> de textos, manejo de **outliers B2B** —que se conservan porque son compras de obra legítimas—,
> cálculo de las **features RFM**, y un paso clave, la **deflactación por inflación**, para que un
> cliente nuevo y uno antiguo sean comparables. El análisis exploratorio confirmó el Pareto,
> mostró que el RFM puro alcanza, y que B2B y B2C difieren en varios órdenes de magnitud.
> Terminamos con **4.992 clientes**, cada uno con su Recencia, Frecuencia y Monto.

---

## 🟧 BLOQUE 3 — Desarrollo del modelo · `2:30 → 4:30`

**[Slide 6 · ¿Cuántos grupos?] (2:30–3:25)**
> Como es un problema no supervisado, comparé cuatro algoritmos: **K-Means, jerárquico, DBSCAN y
> GMM**. Para elegir el número de grupos usé el **método del codo y el coeficiente de silueta**,
> que ven en el gráfico. Acá tomé una decisión importante: la silueta se maximiza con **pocos
> grupos —dos o tres—**, pero esas particiones son demasiado gruesas, separan poco más que activos
> de inactivos. Elegí **K igual a cuatro**: es el estándar RFM, mantiene una silueta sólida y
> entrega cuatro segmentos accionables.

**[Slide 7 · Evaluación y validación] (3:25–4:30)**
> Para evaluar usé tres métricas internas: silueta, Davies-Bouldin y Calinski-Harabasz. K-Means y
> el jerárquico lideran; GMM da valores parecidos; DBSCAN queda bajo porque los datos son un
> gradiente continuo y forma un cluster dominante más ruido. El dato más fuerte es la
> **validación cruzada**: medí la concordancia entre algoritmos con el índice ARI, y K-Means,
> jerárquico y GMM **coinciden en la misma estructura**. Que varios métodos lleguen a lo mismo
> confirma que la segmentación es **real, no un artefacto**. Como modelo de producción elegí
> **K-Means**: simple, interpretable y con predict para clasificar clientes nuevos.

---

## 🟧 BLOQUE 4 — Análisis de resultados · `4:30 → 6:00`

**[Slide 8 · Los 4 segmentos] (4:30–5:15)**
> Este es el resultado. Cada punto es uno de los 4.992 clientes, ubicado por su recencia y su
> frecuencia, y el color es el segmento que encontró el modelo. Se ven claramente separados: los
> **Campeones B2B** arriba a la izquierda —compran seguido y mucho—; los **Activos Recientes**;
> los **Esporádicos o en riesgo**, que se están enfriando; y los **Perdidos**, inactivos hace más
> de 500 días, a la derecha.

**[Slide 9 · El hallazgo] (5:15–6:00)**
> Y acá está el hallazgo central. Miren el contraste: el **14% de los clientes —los Campeones
> B2B— explica el 73% de la facturación real**. Un Pareto comercial muy marcado. Esto responde
> directamente la pregunta de negocio inicial y **justifica tratar a cada segmento de forma
> diferente** en lugar de seguir con campañas masivas.

---

## 🟧 BLOQUE 5 — Conclusiones y recomendaciones · `6:00 → 7:00`

**[Slide 10 · Estrategias por segmento] (6:00–6:35)**
> De ahí salen las recomendaciones, una por segmento. A los **Campeones**, un programa premium con
> cuenta corriente y gestor dedicado, para **retenerlos**. A los **Activos**, up-sell y puntos para
> **crecer**. A los **Esporádicos**, una campaña de **reactivación** con descuento personalizado. Y
> a los **Perdidos**, un win-back de bajo costo. Cada acción con su KPI.

**[Slide 11 · Conclusiones y cierre] (6:35–7:00)**
> Para cerrar: K igual a cuatro entrega segmentos coherentes, validados por tres algoritmos; el
> modelo cuantifica el Pareto; y cada grupo tiene una acción concreta. Como **trabajo futuro**, los
> clusters pueden usarse como etiquetas para entrenar un clasificador supervisado y segmentar
> clientes nuevos en tiempo real. Y como todo el pipeline es reproducible, **cualquier empresa del
> rubro podría aplicarlo con sus propios datos**. Muchas gracias.

---

## ✅ Checklist antes de grabar
- [ ] Abrí `index.html` en el navegador y apretá **`F`** (pantalla completa). Navegá con **→ / espacio**.
- [ ] Ensayá una vez con cronómetro. Si te pasás de 7:00, recortá el bloque del modelo (slides 6–7).
- [ ] Hablá pausado: mejor llegar a 6:40 con todo claro que correr. El guion está calibrado para ~6:40.
- [ ] Grabá en lugar silencioso; el audio importa más que la cámara. Resolución 1080p.
