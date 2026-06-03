# Dataset `transacciones_ecommerce.csv` — versión realista (v2, escalada a 5.000 clientes)

Registro transaccional **sintético** de un e-commerce de ferretería / materiales de
construcción en Tierra del Fuego (Río Grande, Ushuaia, Tolhuin), generado con fines
académicos. Reemplaza a la versión anterior incorporando dinámicas observables en datos
reales argentinos del período **2024-06 a 2026-05**. Esta versión escala el padrón a
**5.000 clientes** (mismo esquema y mismas dinámicas; se regenera con `generar_dataset.py`).

- **Filas:** 50.730 transacciones (incluye 75 duplicados exactos)
- **Clientes:** 5.000
- **Columnas:** 9 (mismo esquema que la versión original)
- **Período:** 2024-06-02 → 2026-05-31

## Diccionario de datos (sin cambios de esquema)

| Columna | Tipo | Descripción |
|---|---|---|
| `id_transaccion` | str | Código único `TX-XXXXXX` (numeración con huecos) |
| `id_cliente` | str | Código `CLI-XXXXX` (numeración con huecos) |
| `fecha` | date | Fecha de la transacción (`YYYY-MM-DD`) |
| `categoria_producto` | str | 12 rubros de ferretería |
| `cantidad_items` | int | Unidades (1–300) |
| `monto_total` | float | Importe en ARS (puede ser negativo = devolución) |
| `canal_venta` | str | Web / App / Telefónico |
| `medio_pago` | str | 5 medios + variantes de texto |
| `localidad` | str | Río Grande / Ushuaia / Tolhuin (+ variantes de texto) |

## Dinámicas reales modeladas

1. **Inflación nominal en pesos.** Los precios crecen mes a mes siguiendo un índice de
   IPC argentino en desinflación. El ticket mediano nominal crece ≈2,7× a lo largo de los
   24 meses. *(Esto antes no existía: la v1 tenía precios estacionarios.)*
2. **Estacionalidad de construcción austral.** Pico en verano (dic–mar) y pozo profundo
   en invierno (jun–ago): junio concentra ~⅕ de las transacciones de diciembre.
3. **Patrón semanal.** Domingos muy bajos (caen a ~¼ de un día hábil), sábados a la baja.
4. **Concentración Pareto.** El 20 % de los clientes genera el 81 % de la facturación.
5. **Segmentos latentes B2B/B2C.** Clientes B2B (constructoras, contratistas) con alta
   frecuencia, tickets altos, cuenta corriente y canal telefónico; B2C con baja
   frecuencia, tarjetas y canal web. *Los segmentos NO están etiquetados* (hay que
   descubrirlos: es el objetivo del clustering).
6. **Acople categoría–precio–cantidad.** Cemento y áridos: barato y a granel.
   Herramientas eléctricas: caro y de a una. Aberturas: muy caro, baja frecuencia.
7. **Mix de categorías desbalanceado.** Ferretería general 15 % vs. Herramientas
   eléctricas 3 %. *(La v1 estaba casi perfectamente balanceada — un delator clásico.)*
8. **Correlación canal ↔ medio de pago.** "Efectivo en sucursal" casi no aparece en Web.

## Imperfecciones introducidas (actualizar `limpiar_dataset`)

A diferencia de la v1, los problemas de calidad son **correlacionados** y de varios tipos.
Tu módulo de limpieza necesita cubrir:

| Problema | Detalle | Acción sugerida |
|---|---|---|
| Nulos en `monto_total` | 355 (~0,7 %), **concentrados en canal Telefónico** (falla de pasarela) | drop |
| Nulos en `medio_pago` | 585 (~1,2 %) | imputar `"Desconocido"` |
| Nulos en `localidad` | 204 (~0,4 %) | imputar `"Desconocido"` o moda |
| Nulos en `categoria_producto` | 131 (~0,26 %) | imputar `"Sin categoría"` o drop |
| **Montos negativos** | 392 devoluciones / notas de crédito | filtrar (o netear, según criterio RFM) |
| **Outliers extremos** | ~150 compras de obra muy grandes (hasta ~$37 M) | conservar y documentar, o winsorizar |
| **Texto inconsistente en `localidad`** | `RÍO GRANDE`, `río grande`, `Rio Grande`, espacios sobrantes, typo `Tohluin` | normalizar (`.str.strip().str.title()` + corrección de acentos/typos) |
| **Texto inconsistente en `medio_pago`** | `transf.`, `T. débito`, `T. crédito` | mapear a forma canónica |
| Duplicados exactos | 75 | `drop_duplicates` |

> **Nota:** el filtro de `monto ≤ 0` que tenías ahora **sí** encuentra registros (las
> devoluciones), a diferencia de la v1. Y la normalización de texto en `localidad` /
> `medio_pago` es nueva y necesaria — antes esas columnas estaban limpias.

## Reproducibilidad

Generado con `numpy.random.default_rng(42)`. El script `generar_dataset.py` documenta
todas las tasas de inflación, factores estacionales, perfiles de categoría y de segmento.
