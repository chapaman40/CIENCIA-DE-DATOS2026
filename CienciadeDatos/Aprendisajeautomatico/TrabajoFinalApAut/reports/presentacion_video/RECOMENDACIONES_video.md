# 📋 Recomendaciones para grabar el video (≤ 7 min)

## 1. Gestión del tiempo (lo más importante)
La consigna exige cubrir 6 puntos en 7 minutos. El guion ya está cronometrado por bloque:

| Bloque | Tiempo | Slides |
|--------|--------|--------|
| Introducción + organización (Git/CookieCutter) | 1:00 | 1–3 |
| Descripción del dataset y su origen | 1:30 | 4–5 |
| Desarrollo del modelo + métricas | 2:00 | 6–7 |
| Análisis exploratorio + resultados | 1:30 | 8–9 |
| Conclusiones y recomendaciones | 1:00 | 10 |

- **Ensayá con cronómetro al menos una vez.** Si te pasás, recortá el bloque del modelo (slide 6), que es el más denso.
- Hablá pausado (~145 palabras/min). El guion está calibrado para ~6:40; te deja margen.
- No leas literal de corrido: usá el guion como apoyo, mirá a cámara cuando puedas.

## 2. Qué resaltar (para diferenciarte)
- **El hallazgo estrella:** "15 % de clientes = 77 % de la facturación". Decilo con énfasis en el slide 9.
- **Justificación de K=4 vs K=2:** demuestra criterio (elegiste utilidad de negocio sobre la métrica pura).
- **La deflactación por inflación:** detalle técnico propio que casi nadie hace; mencionalo.
- **Validación cruzada (ARI):** "tres algoritmos encuentran lo mismo → la segmentación es real".
- **El porqué del dataset sintético:** confidencialidad, pero replicando dinámicas reales del rubro.

## 3. Aspectos técnicos de grabación
- **Audio > video.** Un micrófono decente (o auriculares con mic) importa más que la cámara. Grabá en lugar silencioso.
- **Resolución 1080p**, slides en pantalla completa (F5 en PowerPoint).
- Si grabás tu pantalla con OBS / Loom / Zoom, mostrá las **figuras reales** (Pareto, perfiles, métricas) — ya están en los slides.
- Opcional pero suma: una pequeña **cámara tuya en esquina** (webcam) da cercanía.
- Hacé una **toma de prueba de 20 s** y revisá audio/nivel antes de grabar todo.

## 4. Errores comunes a evitar
- ❌ Quedarte sin tiempo y apurar las conclusiones (es lo que más pesa en la nota).
- ❌ Leer tablas número por número: contá la *lectura* del dato, no el dato crudo.
- ❌ Explicar el código línea por línea: el foco es **proceso y resultados**, no implementación.
- ❌ Dejar slides con texto que no nombrás: si está en pantalla, mencionalo aunque sea al pasar.

## 5. Entregables de esta carpeta
| Archivo | Qué es |
|---------|--------|
| `Presentacion_TrabajoFinal_AA.pptx` | Las 10 diapositivas, listas para presentar (F5). |
| `GUION_video_7min.md` | Guion cronometrado, slide por slide, en primera persona. |
| `RECOMENDACIONES_video.md` | Este documento. |
| `build.js` | Script que genera el PPTX (por si querés editar y regenerar con `node build.js`). |
