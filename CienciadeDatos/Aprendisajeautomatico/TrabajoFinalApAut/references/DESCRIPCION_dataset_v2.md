# Dataset `transacciones_ecommerce.csv` — versión realista (v2)

Registro transaccional **sintético** de un e-commerce de ferretería / materiales de
construcción en Tierra del Fuego (Río Grande, Ushuaia, Tolhuin), generado con fines
académicos. Reemplaza a la versión anterior incorporando dinámicas observables en datos
reales argentinos del período **2024-06 a 2026-05**.

- **Filas:** 10.321 transacciones (incluye 15 duplicados exactos)
- **Clientes:** 1.000
- **Columnas:** 9 (mismo esquema que la versión original)
- **Período:** 2024-06-07 → 2026-05-31

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
   IPC argentino en desinflación. El ticket mediano pasa de ~$80.000 (2024Q2) a
   ~$170.000 (2026Q2), ≈2,1×. *(Esto antes no existía: la v1 tenía precios estacionarios.)*
2. **Estacionalidad de construcción austral.** Pico en verano (dic–mar) y pozo profundo
   en invierno (jun–ago): junio tiene ~330 transacciones contra ~1.180 de diciembre.
3. **Patrón semanal.** Domingos muy bajos (~400) frente a días hábiles (~1.700–1.880).
4. **Concentración Pareto.** El 20 % de los clientes genera el 83 % de la facturación;
   el top 5 %, el 46 %.
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
| Nulos en `monto_total` | 84 (~0,8 %), **concentrados en canal Telefónico** (falla de pasarela) | drop |
| Nulos en `medio_pago` | 119 (~1,1 %) | imputar `"Desconocido"` |
| Nulos en `localidad` | 35 (~0,3 %) | imputar `"Desconocido"` o moda |
| Nulos en `categoria_producto` | 35 (~0,25 %) | imputar `"Sin categoría"` o drop |
| **Montos negativos** | 90 devoluciones / notas de crédito | filtrar (o netear, según criterio RFM) |
| **Outliers extremos** | 60 compras de obra muy grandes (hasta ~$33 M) | conservar y documentar, o winsorizar |
| **Texto inconsistente en `localidad`** | `RÍO GRANDE`, `río grande`, `Rio Grande`, espacios sobrantes, typo `Tohluin` | normalizar (`.str.strip().str.title()` + corrección de acentos/typos) |
| **Texto inconsistente en `medio_pago`** | `transf.`, `T. débito`, `T. crédito` | mapear a forma canónica |
| Duplicados exactos | 15 | `drop_duplicates` |

> **Nota:** el filtro de `monto ≤ 0` que tenías ahora **sí** encuentra registros (las
> devoluciones), a diferencia de la v1. Y la normalización de texto en `localidad` /
> `medio_pago` es nueva y necesaria — antes esas columnas estaban limpias.

## Reproducibilidad

Generado con `numpy.random.default_rng(42)`. El script `generar_dataset.py` documenta
todas las tasas de inflación, factores estacionales, perfiles de categoría y de segmento.
