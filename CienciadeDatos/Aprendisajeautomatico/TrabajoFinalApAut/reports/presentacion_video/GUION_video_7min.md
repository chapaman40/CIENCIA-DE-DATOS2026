# 🎬 Guion del video — Trabajo Final de Aprendizaje Automático
### Segmentación de Clientes de un E-commerce de Ferretería · Ian Gallego

> **Duración objetivo:** 6:30 – 7:00 min · **Ritmo:** ~145 palabras/min (hablar pausado).
> Cada bloque indica el **slide**, el **tiempo acumulado** y el **texto a leer** (en primera persona).
> Los `[ ]` son acotaciones para vos, no se leen.

---

## ⏱️ Distribución (según la consigna)

| Bloque | Slides | Tiempo | Acumulado |
|--------|--------|--------|-----------|
| Introducción + organización | 1 · 2 · 3 | 1:00 | 1:00 |
| Descripción del dataset | 4 · 5 | 1:30 | 2:30 |
| Desarrollo del modelo | 6 · 7 | 2:00 | 4:30 |
| Análisis de resultados | 8 · 9 | 1:30 | 6:00 |
| Conclusiones y recomendaciones | 10 | 1:00 | 7:00 |

---

## 🟧 BLOQUE 1 — Introducción y organización · `0:00 → 1:00`

**[Slide 1 — Portada] (0:00–0:12)**
> Hola, soy Ian Gallego. En este video presento mi trabajo final de Aprendizaje Automático:
> la **segmentación de clientes** de un e-commerce de ferretería y materiales de construcción
> de Tierra del Fuego, usando la metodología RFM combinada con clustering no supervisado.

**[Slide 2 — El problema y el objetivo] (0:12–0:42)**
> El negocio tiene una base de clientes muy heterogénea: conviven constructoras y contratistas
> —los clientes B2B— con particulares que compran para una refacción puntual. Hoy el marketing
> se envía masivo y uniforme, y eso genera desperdicio de presupuesto, baja conversión y fuga de
> clientes valiosos. **Mi objetivo fue segmentar a los clientes en grupos homogéneos según su
> comportamiento de compra**, para diseñar acciones de marketing personalizadas. La personalización
> basada en datos puede mejorar la conversión entre un 10 y un 30 por ciento.

**[Slide 3 — Organización] (0:42–1:00)**
> El proyecto está versionado en **Git** y estructurado con la plantilla **Cookiecutter Data Science**,
> que separa datos, código, modelos y reportes. Todo el pipeline es **reproducible**: con un solo comando
> se ejecutan los notebooks en orden, con semilla fija, y la lógica vive en un paquete de Python con tests.

---

## 🟧 BLOQUE 2 — Descripción del dataset · `1:00 → 2:30`

**[Slide 4 — El dataset] (1:00–1:50)**
> El dataset tiene **10.321 transacciones de 1.000 clientes**, con 9 variables de negocio, a lo largo
> de 24 meses, entre 2024 y 2026. Es un dataset **sintético**: por confidencialidad de la empresa real
> lo generé en Python con semilla fija, para que sea reproducible. Pero no son datos aleatorios:
> **replican dinámicas reales del rubro** —la inflación en pesos, que duplica el ticket en dos años;
> la estacionalidad austral, con pico en verano y pozo en invierno; y la concentración de tipo Pareto.
> Un detalle clave: las variables RFM **no vienen en el CSV**, se derivan agrupando por cliente.

**[Slide 5 — Preprocesamiento] (1:50–2:30)**
> El preprocesamiento tuvo cinco pasos. Primero, **limpieza**: descarté nulos críticos, neteé devoluciones
> y eliminé duplicados. Segundo, **normalización de texto**, porque localidad y medio de pago venían con
> errores de tipeo y mayúsculas. Tercero, los **outliers B2B** —compras de obra de hasta 33 millones— los
> conservé, porque son legítimos, no errores. Cuarto, calculé las **features RFM** por cliente. Y quinto,
> un paso importante: **deflacté los montos por inflación**, para que un cliente reciente y uno antiguo
> sean comparables. El resultado son **999 clientes**, cada uno con su perfil de Recencia, Frecuencia y Monto.

---

## 🟧 BLOQUE 3 — Desarrollo del modelo · `2:30 → 4:30`

**[Slide 6 — Algoritmos y decisiones] (2:30–3:35)**
> Como es un problema **no supervisado** —no tengo etiquetas de segmento— comparé **cuatro algoritmos**.
> **K-Means** como modelo base. **Clustering jerárquico**, para validar la estructura sin fijar el número
> de grupos de antemano. **DBSCAN**, robusto a los outliers de los clientes B2B. Y **GMM**, que da una
> asignación probabilística y detecta clientes en la frontera entre segmentos.
> Tomé varias decisiones: usé **RFM puro** como features, escalé con StandardScaler, y elegí **cuatro clusters**.
> Es importante: K igual a dos maximizaba la silueta, pero solo separaba activos de inactivos, algo trivial
> para marketing. **K igual a cuatro es el estándar RFM y da segmentos accionables.** K-Means quedó como
> modelo de producción por ser simple, interpretable y poder predecir el segmento de clientes nuevos.

**[Slide 7 — Métricas] (3:35–4:30)**
> Para evaluar usé tres métricas internas: el **coeficiente de silueta**, el índice de **Davies-Bouldin** y
> el de **Calinski-Harabasz**. K-Means y el jerárquico lideran, con siluetas alrededor de 0,37; GMM da
> valores comparables. DBSCAN queda bajo porque, al ser los datos un gradiente continuo, tiende a formar
> un cluster dominante más ruido —que es un resultado válido en sí mismo. Pero el dato más importante es
> la **validación de robustez**: K-Means, el jerárquico y GMM **convergen a la misma estructura**, con un
> índice de concordancia alto entre ellos. Que tres métodos distintos encuentren los mismos grupos confirma
> que la segmentación es **real y no un artefacto** de un solo algoritmo.

---

## 🟧 BLOQUE 4 — Análisis de resultados · `4:30 → 6:00`

**[Slide 8 — Análisis exploratorio] (4:30–5:15)**
> Antes de modelar, el análisis exploratorio me dio cuatro conclusiones. La primera: el **Pareto** está
> confirmado, la facturación se concentra en muy pocos clientes, lo que justifica segmentar. La segunda:
> el **RFM puro alcanza**, porque el ticket promedio es monto sobre frecuencia y generaba multicolinealidad,
> así que lo dejé fuera del modelo. La tercera: **deflactar era imprescindible**, porque sin ajustar por
> inflación los clientes recientes parecían artificialmente más valiosos. Y la cuarta: la brecha **B2B
> contra B2C** es de varios órdenes de magnitud en monto y frecuencia.

**[Slide 9 — Resultados] (5:15–6:00)**
> El modelo encontró **cuatro segmentos** con un nombre comercial cada uno. Los **Campeones B2B** son el
> 15 por ciento de los clientes. Los **Activos Recientes**, un 31 por ciento. Los **Esporádicos o en riesgo**,
> un 32. Y los **Perdidos**, un 22 por ciento. Pero el hallazgo central está en la facturación:
> **ese 15 por ciento de Campeones explica el 77 por ciento de la facturación real.** Un Pareto muy marcado,
> que responde a la pregunta inicial del negocio y justifica un trato de marketing completamente diferenciado.

---

## 🟧 BLOQUE 5 — Conclusiones y recomendaciones · `6:00 → 7:00`

**[Slide 10 — Conclusiones] (6:00–7:00)**
> Para cerrar. El modelo con cuatro clusters entrega segmentos **coherentes y accionables**, validados por
> tres algoritmos, y cuantifica el Pareto del negocio. Cada segmento tiene una **estrategia concreta**: a los
> **Campeones**, un programa premium con cuenta corriente y gestor dedicado; a los **Activos**, up-sell y un
> programa de puntos; a los **Esporádicos**, una campaña de reactivación con descuento personalizado; y a los
> **Perdidos**, una acción de win-back de bajo costo por email.
> Como **trabajo futuro**, los clusters pueden usarse como etiquetas para entrenar un clasificador supervisado
> —como Random Forest o XGBoost— y así clasificar automáticamente a cada cliente nuevo en tiempo real.
> Y como el pipeline es reproducible, cualquier empresa del rubro podría aplicarlo con sus propios datos.
> Muchas gracias.

---

## ✅ Checklist antes de grabar
- [ ] Ensayar una vez con cronómetro — si te pasás de 7:00, recortá el bloque 3 (es el más denso).
- [ ] Tener el PPTX abierto en **modo presentación** (F5) y avanzar slides al ritmo del guion.
- [ ] Hablar pausado: es mejor llegar a 6:40 con todo claro que correr para meter todo.
