const pptxgen = require("pptxgenjs");
const path = require("path");

const FIG = "F:/CIENCIA DE DATOS2026/CienciadeDatos/Aprendisajeautomatico/TrabajoFinalApAut/reports/figures";
const fig = (name) => path.join(FIG, name);

// ---- Palette (industrial / ferretería) ----
const DARK = "1C2A39";   // charcoal navy
const LIGHT = "F4F1EC";  // concrete cream
const AMBER = "E8833A";  // construction accent
const STEEL = "3D6E8F";  // steel blue
const MUTED = "6B7682";
const WHITE = "FFFFFF";
const INK = "22303C";

// segment colors
const GOLD = "C8911B";
const GREEN = "2E8B57";
const AMBER2 = "E8833A";
const GRAY = "8A97A3";

const HFONT = "Georgia";
const BFONT = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5
const W = 13.3, H = 7.5;
pres.author = "Ian Gallego";
pres.title = "Segmentación de Clientes — Trabajo Final de Aprendizaje Automático";

const shadow = () => ({ type: "outer", color: "000000", blur: 7, offset: 3, angle: 135, opacity: 0.18 });

// ---------- Helpers ----------
function header(slide, kicker, title, num) {
  slide.background = { color: LIGHT };
  // top accent bar
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.14, fill: { color: AMBER } });
  // number badge
  slide.addShape(pres.shapes.OVAL, { x: 0.55, y: 0.55, w: 0.62, h: 0.62, fill: { color: DARK } });
  slide.addText(num, { x: 0.55, y: 0.55, w: 0.62, h: 0.62, align: "center", valign: "middle", color: AMBER, fontFace: HFONT, fontSize: 22, bold: true });
  slide.addText(kicker.toUpperCase(), { x: 1.35, y: 0.55, w: 10, h: 0.3, color: AMBER, fontFace: BFONT, fontSize: 12, bold: true, charSpacing: 3, margin: 0 });
  slide.addText(title, { x: 1.35, y: 0.82, w: 11.4, h: 0.7, color: DARK, fontFace: HFONT, fontSize: 28, bold: true, margin: 0 });
  // footer
  slide.addText("Ian Gallego  ·  Politécnico Malvinas Argentinas  ·  Aprendizaje Automático 2026", { x: 0.55, y: 7.05, w: 9, h: 0.3, color: MUTED, fontFace: BFONT, fontSize: 9, margin: 0 });
}

function card(slide, x, y, w, h, fill) {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill || WHITE }, line: { color: "E2DCD1", width: 1 }, shadow: shadow() });
}

function stat(slide, x, y, w, big, label, color) {
  slide.addText(big, { x, y, w, h: 0.8, align: "center", color: color || AMBER, fontFace: HFONT, fontSize: 40, bold: true, margin: 0 });
  slide.addText(label, { x, y: y + 0.78, w, h: 0.55, align: "center", color: MUTED, fontFace: BFONT, fontSize: 12, margin: 0 });
}

// ============================================================
// SLIDE 1 — TITLE
// ============================================================
let s = pres.addSlide();
s.background = { color: DARK };
s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.22, h: H, fill: { color: AMBER } });
s.addShape(pres.shapes.RECTANGLE, { x: 0.22, y: 0, w: 0.06, h: H, fill: { color: STEEL } });
s.addText("TRABAJO FINAL · APRENDIZAJE AUTOMÁTICO", { x: 0.9, y: 1.5, w: 11, h: 0.4, color: AMBER, fontFace: BFONT, fontSize: 15, bold: true, charSpacing: 4, margin: 0 });
s.addText("Segmentación de Clientes\nde un E-commerce de Ferretería", { x: 0.85, y: 2.0, w: 11.6, h: 1.9, color: WHITE, fontFace: HFONT, fontSize: 42, bold: true, lineSpacingMultiple: 1.0, margin: 0 });
s.addText("Metodología RFM + Clustering no supervisado · Tierra del Fuego", { x: 0.9, y: 4.0, w: 11.5, h: 0.5, color: "CADCFC", fontFace: BFONT, fontSize: 19, italic: true, margin: 0 });
// bottom author bar
s.addShape(pres.shapes.LINE, { x: 0.9, y: 5.55, w: 5.5, h: 0, line: { color: STEEL, width: 1.5 } });
s.addText([
  { text: "Ian Gallego", options: { bold: true, color: WHITE, fontSize: 16, breakLine: true } },
  { text: "Politécnico Malvinas Argentinas · Ciencia de Datos · 2026", options: { color: "9FB3C8", fontSize: 13 } },
], { x: 0.9, y: 5.7, w: 9, h: 1, fontFace: BFONT, margin: 0 });

// ============================================================
// SLIDE 2 — INTRODUCCIÓN / OBJETIVO (1 min)
// ============================================================
s = pres.addSlide();
header(s, "Introducción", "El problema: marketing masivo en una base heterogénea", "1");
// left: problem
card(s, 0.55, 1.7, 6.0, 4.9);
s.addText("Contexto", { x: 0.85, y: 1.9, w: 5.4, h: 0.4, color: STEEL, fontFace: HFONT, fontSize: 18, bold: true, margin: 0 });
s.addText([
  { text: "E-commerce de ferretería y materiales de construcción en Tierra del Fuego.", options: { breakLine: true, bold: true } },
  { text: "", options: { breakLine: true, fontSize: 6 } },
  { text: "La base de clientes es muy heterogénea: conviven constructoras y contratistas (B2B) con particulares que compran para refacciones (B2C).", options: { breakLine: true } },
  { text: "", options: { breakLine: true, fontSize: 6 } },
  { text: "Hoy el marketing (promos, mailing, WhatsApp) se envía masivo y uniforme, lo que genera:", options: { breakLine: true } },
], { x: 0.85, y: 2.35, w: 5.4, h: 2.2, color: INK, fontFace: BFONT, fontSize: 13.5, lineSpacingMultiple: 1.05, margin: 0, valign: "top" });
const pains = ["Desperdicio de presupuesto en descuentos innecesarios", "Baja conversión por mensajes irrelevantes", "Fuga de clientes valiosos sin detección preventiva", "Subutilización del potencial del segmento B2B"];
pains.forEach((p, i) => {
  s.addText(p, { x: 0.95, y: 4.55 + i * 0.5, w: 5.3, h: 0.45, color: INK, fontFace: BFONT, fontSize: 12.5, bullet: { code: "2022", indent: 14 }, margin: 0, valign: "middle" });
});
// right: objective
card(s, 6.85, 1.7, 5.9, 2.55, DARK);
s.addText("OBJETIVO", { x: 7.15, y: 1.9, w: 5.3, h: 0.35, color: AMBER, fontFace: BFONT, fontSize: 13, bold: true, charSpacing: 3, margin: 0 });
s.addText("Segmentar a los clientes en grupos homogéneos según su comportamiento de compra, para diseñar estrategias de marketing personalizadas y accionables.", { x: 7.15, y: 2.3, w: 5.35, h: 1.8, color: WHITE, fontFace: BFONT, fontSize: 15, lineSpacingMultiple: 1.08, margin: 0, valign: "top" });
// relevance stats
card(s, 6.85, 4.45, 5.9, 2.15);
s.addText("Por qué importa", { x: 7.15, y: 4.6, w: 5.3, h: 0.35, color: STEEL, fontFace: HFONT, fontSize: 16, bold: true, margin: 0 });
s.addText([
  { text: "+10 % a +30 %", options: { color: GREEN, bold: true, fontSize: 26, breakLine: true } },
  { text: "de mejora potencial en conversión con personalización basada en datos (marketing digital).", options: { color: MUTED, fontSize: 12.5 } },
], { x: 7.15, y: 5.0, w: 5.35, h: 1.5, fontFace: BFONT, margin: 0, valign: "top" });

// ============================================================
// SLIDE 3 — ORGANIZACIÓN (Git + CookieCutter)
// ============================================================
s = pres.addSlide();
header(s, "Organización del proyecto", "Reproducible: Git + CookieCutter Data Science", "1b");
card(s, 0.55, 1.7, 6.0, 4.9);
s.addText("Estructura CCDS", { x: 0.85, y: 1.9, w: 5.4, h: 0.4, color: STEEL, fontFace: HFONT, fontSize: 18, bold: true, margin: 0 });
s.addText([
  { text: "data/        raw · interim · processed", options: { breakLine: true } },
  { text: "notebooks/   pipeline 0→5 (nº-iniciales-desc)", options: { breakLine: true } },
  { text: "segmentacion/  código fuente (paquete py)", options: { breakLine: true } },
  { text: "models/      .joblib entrenados", options: { breakLine: true } },
  { text: "reports/     figuras y PDF", options: { breakLine: true } },
  { text: "references/  diccionario de datos · glosario", options: { breakLine: true } },
  { text: "tests/       pruebas (pytest)", options: {} },
], { x: 0.85, y: 2.4, w: 5.4, h: 4.0, color: INK, fontFace: "Consolas", fontSize: 13.5, lineSpacingMultiple: 1.35, margin: 0, valign: "top" });
// right: principles
const orgItems = [
  ["Versionado con Git", "Historial de cambios y código reproducible."],
  ["Plantilla CookieCutter DS", "Estructura estándar de la industria: separa datos, código, modelos y reportes."],
  ["Pipeline ejecutable", "make all reproduce los notebooks 1→5 en orden; semilla fija (rng=42)."],
  ["Código modular + tests", "Lógica en segmentacion/ reutilizable, validada con pytest."],
];
orgItems.forEach((it, i) => {
  const y = 1.7 + i * 1.25;
  card(s, 6.85, y, 5.9, 1.1);
  s.addShape(pres.shapes.RECTANGLE, { x: 6.85, y, w: 0.1, h: 1.1, fill: { color: AMBER } });
  s.addText(it[0], { x: 7.1, y: y + 0.13, w: 5.5, h: 0.4, color: DARK, fontFace: HFONT, fontSize: 16, bold: true, margin: 0 });
  s.addText(it[1], { x: 7.1, y: y + 0.55, w: 5.5, h: 0.5, color: MUTED, fontFace: BFONT, fontSize: 12.5, margin: 0, valign: "top" });
});

// ============================================================
// SLIDE 4 — DATASET (1.5 min)
// ============================================================
s = pres.addSlide();
header(s, "Descripción del dataset", "transacciones_ecommerce.csv — sintético y realista", "2");
// stat row
const sb = [["10.321", "transacciones", AMBER], ["1.000", "clientes únicos", STEEL], ["9", "variables de negocio", GREEN], ["24", "meses (2024–2026)", GOLD]];
sb.forEach((b, i) => {
  const x = 0.55 + i * 3.07;
  card(s, x, 1.7, 2.85, 1.5);
  stat(s, x, 1.85, 2.85, b[0], b[1], b[2]);
});
// origin
card(s, 0.55, 3.45, 6.0, 3.15);
s.addText("Origen y recopilación", { x: 0.85, y: 3.6, w: 5.4, h: 0.4, color: STEEL, fontFace: HFONT, fontSize: 18, bold: true, margin: 0 });
s.addText([
  { text: "Sintético", options: { bold: true, color: AMBER } },
  { text: ", generado en Python con numpy.random.default_rng(42) por confidencialidad de la empresa real (Río Grande).", options: {} },
], { x: 0.85, y: 4.05, w: 5.4, h: 0.9, color: INK, fontFace: BFONT, fontSize: 13.5, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
s.addText("Replica dinámicas reales del rubro:", { x: 0.85, y: 4.85, w: 5.4, h: 0.35, color: DARK, fontFace: BFONT, fontSize: 13, bold: true, margin: 0 });
["Inflación en pesos (ticket ×2,1 en 24 meses)", "Estacionalidad austral (pico dic–mar, pozo jun–ago)", "Concentración Pareto (20 % clientes → 83 % facturación)", "Segmentos B2B / B2C latentes (sin etiquetar)"].forEach((p, i) => {
  s.addText(p, { x: 0.95, y: 5.18 + i * 0.34, w: 5.3, h: 0.33, color: INK, fontFace: BFONT, fontSize: 12, bullet: { code: "2022", indent: 12 }, margin: 0, valign: "middle" });
});
// columns table
card(s, 6.85, 3.45, 5.9, 3.15);
s.addText("Variables (9 columnas)", { x: 7.15, y: 3.6, w: 5.4, h: 0.4, color: STEEL, fontFace: HFONT, fontSize: 18, bold: true, margin: 0 });
const colRows = [
  ["id_cliente / id_transacción", "str"],
  ["fecha", "date"],
  ["categoria_producto (12 rubros)", "str"],
  ["cantidad_items (1–300)", "int"],
  ["monto_total (ARS, admite neg.)", "float"],
  ["canal_venta · medio_pago", "str"],
  ["localidad (RG / Ush / Tolhuin)", "str"],
];
const tdata = [[
  { text: "Columna", options: { bold: true, color: WHITE, fill: { color: DARK }, fontSize: 12 } },
  { text: "Tipo", options: { bold: true, color: WHITE, fill: { color: DARK }, fontSize: 12, align: "center" } },
]];
colRows.forEach((r, i) => tdata.push([
  { text: r[0], options: { color: INK, fontSize: 11.5, fill: { color: i % 2 ? "F4F1EC" : "FFFFFF" } } },
  { text: r[1], options: { color: AMBER, bold: true, fontSize: 11.5, align: "center", fill: { color: i % 2 ? "F4F1EC" : "FFFFFF" } } },
]));
s.addTable(tdata, { x: 7.15, y: 4.0, w: 5.4, colW: [4.4, 1.0], rowH: 0.27, fontFace: BFONT, border: { pt: 0.5, color: "E2DCD1" }, valign: "middle" });
s.addText("Nota: las variables RFM no vienen en el CSV — se derivan agrupando por id_cliente.", { x: 7.15, y: 6.32, w: 5.4, h: 0.25, color: MUTED, fontFace: BFONT, fontSize: 9.5, italic: true, margin: 0 });

// ============================================================
// SLIDE 5 — CALIDAD / PREPROCESAMIENTO + EDA limpieza
// ============================================================
s = pres.addSlide();
header(s, "Preprocesamiento", "De datos crudos a tabla RFM por cliente", "2b");
// pipeline steps
const steps = [
  ["Limpieza", "Drop de 84 nulos críticos (canal telefónico), imputación 'Desconocido', filtro de 90 devoluciones, 15 duplicados."],
  ["Normalización texto", "localidad y medio_pago a forma canónica (typos, mayúsculas, abreviaturas)."],
  ["Outliers B2B", "~60 compras de obra (hasta ~$33 M): se conservan, son legítimas."],
  ["Features RFM", "Agrupo por cliente → Recency, Frequency, Monetary + complementarias."],
  ["Deflactación", "Ajuste por inflación: clientes nuevos y antiguos comparables."],
];
steps.forEach((st, i) => {
  const y = 1.75 + i * 1.0;
  card(s, 0.55, y, 5.7, 0.86);
  s.addShape(pres.shapes.OVAL, { x: 0.72, y: y + 0.18, w: 0.5, h: 0.5, fill: { color: STEEL } });
  s.addText(String(i + 1), { x: 0.72, y: y + 0.18, w: 0.5, h: 0.5, align: "center", valign: "middle", color: WHITE, fontFace: HFONT, fontSize: 18, bold: true });
  s.addText(st[0], { x: 1.4, y: y + 0.1, w: 4.7, h: 0.32, color: DARK, fontFace: HFONT, fontSize: 14.5, bold: true, margin: 0 });
  s.addText(st[1], { x: 1.4, y: y + 0.42, w: 4.7, h: 0.42, color: MUTED, fontFace: BFONT, fontSize: 10.8, margin: 0, valign: "top" });
});
// right figure
card(s, 6.5, 1.75, 6.3, 4.85);
s.addImage({ path: fig("nb1_problemas_calidad.png"), x: 6.65, y: 1.95, w: 6.0, h: 3.0, sizing: { type: "contain", w: 6.0, h: 3.0 } });
s.addText("Resultado: 10.132 transacciones limpias → 999 clientes con su perfil RFM.", { x: 6.65, y: 5.05, w: 6.0, h: 0.5, color: DARK, fontFace: BFONT, fontSize: 13, bold: true, align: "center", margin: 0 });
s.addText([
  { text: "R", options: { color: AMBER, bold: true } }, { text: "ecency · ", options: { color: MUTED } },
  { text: "F", options: { color: AMBER, bold: true } }, { text: "requency · ", options: { color: MUTED } },
  { text: "M", options: { color: AMBER, bold: true } }, { text: "onetary (deflactado)", options: { color: MUTED } },
], { x: 6.65, y: 5.55, w: 6.0, h: 0.5, fontFace: BFONT, fontSize: 13, align: "center", margin: 0 });

// ============================================================
// SLIDE 6 — DESARROLLO DEL MODELO (2 min) — algoritmos
// ============================================================
s = pres.addSlide();
header(s, "Desarrollo del modelo", "Cuatro algoritmos de clustering comparados", "3");
const algos = [
  ["K-Means", "Modelo base. K óptimo por codo + Silhouette. Hard clustering, .predict() nativo.", AMBER],
  ["Jerárquico (Ward)", "Dendrograma: valida la estructura sin fijar K a priori.", STEEL],
  ["DBSCAN", "Basado en densidad, robusto a outliers (compras B2B de gran monto).", GREEN],
  ["GMM", "Soft clustering: probabilidad de pertenencia → clientes en frontera.", GOLD],
];
algos.forEach((a, i) => {
  const x = 0.55 + (i % 2) * 3.15;
  const y = 1.75 + Math.floor(i / 2) * 1.7;
  card(s, x, y, 2.95, 1.5);
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.95, h: 0.1, fill: { color: a[2] } });
  s.addText(a[0], { x: x + 0.18, y: y + 0.18, w: 2.6, h: 0.4, color: DARK, fontFace: HFONT, fontSize: 17, bold: true, margin: 0 });
  s.addText(a[1], { x: x + 0.18, y: y + 0.62, w: 2.6, h: 0.85, color: MUTED, fontFace: BFONT, fontSize: 11, margin: 0, valign: "top" });
});
// right: decisions
card(s, 6.9, 1.75, 5.85, 4.85, DARK);
s.addText("Decisiones metodológicas", { x: 7.2, y: 1.95, w: 5.3, h: 0.4, color: AMBER, fontFace: HFONT, fontSize: 18, bold: true, margin: 0 });
const dec = [
  ["Features", "Solo R, F, M(log) — RFM puro. Las complementarias caracterizan, no entran al modelo."],
  ["Escalado", "StandardScaler antes de medir distancias."],
  ["K = 4", "No K=2 (que maximiza Silhouette pero es trivial). K=4 = estándar RFM, accionable."],
  ["Producción", "K-Means: simple, interpretable, .predict() para clientes nuevos."],
];
dec.forEach((d, i) => {
  const y = 2.45 + i * 1.02;
  s.addText(d[0], { x: 7.2, y, w: 5.3, h: 0.32, color: WHITE, fontFace: HFONT, fontSize: 14, bold: true, margin: 0 });
  s.addText(d[1], { x: 7.2, y: y + 0.32, w: 5.35, h: 0.62, color: "9FB3C8", fontFace: BFONT, fontSize: 11.5, margin: 0, valign: "top", lineSpacingMultiple: 1.0 });
});

// ============================================================
// SLIDE 7 — MÉTRICAS DE EVALUACIÓN
// ============================================================
s = pres.addSlide();
header(s, "Evaluación del modelo", "Métricas internas + validación cruzada entre algoritmos", "3b");
// metrics table
const m = [
  ["Algoritmo", "Silhouette", "Davies-Bouldin", "Calinski-H.", "K"],
  ["K-Means", "0.365", "0.927", "1056", "4"],
  ["Jerárquico", "0.372", "0.794", "976", "4"],
  ["GMM", "0.316", "0.926", "901", "4"],
  ["DBSCAN", "0.042*", "0.670", "66", "5"],
];
const mt = m.map((row, ri) => row.map((c, ci) => ({
  text: c,
  options: ri === 0
    ? { bold: true, color: WHITE, fill: { color: DARK }, fontSize: 13, align: ci ? "center" : "left" }
    : { color: ri === 1 ? AMBER : INK, bold: ri === 1, fontSize: 13, align: ci ? "center" : "left", fill: { color: ri % 2 ? "FFFFFF" : "F4F1EC" } },
})));
card(s, 0.55, 1.8, 7.0, 2.55);
s.addTable(mt, { x: 0.75, y: 1.95, w: 6.6, colW: [1.9, 1.3, 1.5, 1.2, 0.7], rowH: 0.4, fontFace: BFONT, border: { pt: 0.5, color: "E2DCD1" }, valign: "middle" });
s.addText("* DBSCAN se evalúa sin outliers; tiende a 1 cluster dominante + ruido (los datos son un gradiente continuo).", { x: 0.75, y: 4.04, w: 6.6, h: 0.3, color: MUTED, fontFace: BFONT, fontSize: 9.5, italic: true, margin: 0 });
// validation card
card(s, 0.55, 4.55, 7.0, 2.05, DARK);
s.addText("Validación de robustez", { x: 0.75, y: 4.7, w: 6.6, h: 0.35, color: AMBER, fontFace: HFONT, fontSize: 16, bold: true, margin: 0 });
s.addText([
  { text: "K-Means, Jerárquico y GMM convergen a la misma estructura (ARI alto entre sí). ", options: { color: WHITE } },
  { text: "Que tres métodos distintos encuentren los mismos grupos confirma que la segmentación es real, no un artefacto.", options: { color: "9FB3C8" } },
], { x: 0.75, y: 5.1, w: 6.6, h: 1.3, fontFace: BFONT, fontSize: 13.5, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
// figure
card(s, 7.75, 1.8, 5.0, 4.8);
s.addImage({ path: fig("nb4_comparacion_metricas.png"), x: 7.9, y: 2.0, w: 4.7, h: 4.4, sizing: { type: "contain", w: 4.7, h: 4.4 } });

// ============================================================
// SLIDE 8 — ANÁLISIS EXPLORATORIO (1.5 min)
// ============================================================
s = pres.addSlide();
header(s, "Análisis exploratorio (EDA)", "Qué nos dijeron los datos antes de modelar", "4");
card(s, 0.55, 1.75, 7.0, 4.85);
s.addImage({ path: fig("nb3_heatmap.png"), x: 0.7, y: 1.95, w: 6.7, h: 4.5, sizing: { type: "contain", w: 6.7, h: 4.5 } });
// findings
const finds = [
  ["Pareto confirmado", "El grueso de la facturación se concentra en muy pocos clientes — justifica segmentar."],
  ["RFM puro suficiente", "ticket_promedio = M/F genera multicolinealidad → se excluye del clustering."],
  ["Deflactar es clave", "Sin ajustar por inflación, los clientes recientes parecerían artificialmente más valiosos."],
  ["B2B vs B2C nítido", "Brecha de varios órdenes de magnitud en monto y frecuencia entre ambos perfiles."],
];
finds.forEach((f, i) => {
  const y = 1.75 + i * 1.22;
  card(s, 7.8, y, 4.95, 1.08);
  s.addShape(pres.shapes.RECTANGLE, { x: 7.8, y, w: 0.1, h: 1.08, fill: { color: STEEL } });
  s.addText(f[0], { x: 8.05, y: y + 0.12, w: 4.6, h: 0.36, color: DARK, fontFace: HFONT, fontSize: 15, bold: true, margin: 0 });
  s.addText(f[1], { x: 8.05, y: y + 0.5, w: 4.6, h: 0.55, color: MUTED, fontFace: BFONT, fontSize: 11.5, margin: 0, valign: "top" });
});

// ============================================================
// SLIDE 9 — RESULTADOS: PARETO + 4 SEGMENTOS
// ============================================================
s = pres.addSlide();
header(s, "Resultados del modelo", "4 segmentos — y un Pareto comercial muy marcado", "5");
card(s, 0.55, 1.75, 6.4, 4.85);
s.addImage({ path: fig("nb5_pareto_comercial.png"), x: 0.7, y: 1.95, w: 6.1, h: 4.5, sizing: { type: "contain", w: 6.1, h: 4.5 } });
// segment table
const seg = [
  ["Segmento", "Clientes", "% base", "% facturación"],
  ["Campeones (B2B)", "154", "15,4 %", "76,7 %"],
  ["Activos Recientes", "306", "30,6 %", "16,4 %"],
  ["Esporádicos / Riesgo", "322", "32,2 %", "5,6 %"],
  ["Perdidos", "217", "21,7 %", "1,2 %"],
];
const segColors = [null, GOLD, GREEN, AMBER2, GRAY];
const st2 = seg.map((row, ri) => row.map((c, ci) => ({
  text: c,
  options: ri === 0
    ? { bold: true, color: WHITE, fill: { color: DARK }, fontSize: 12.5, align: ci ? "center" : "left" }
    : { color: ci === 0 ? segColors[ri] : (ci === 3 ? DARK : INK), bold: ci === 0 || ci === 3, fontSize: 13, align: ci ? "center" : "left", fill: { color: ri % 2 ? "FFFFFF" : "F4F1EC" } },
})));
card(s, 7.15, 1.75, 5.6, 2.55);
s.addTable(st2, { x: 7.3, y: 1.9, w: 5.3, colW: [2.0, 1.05, 1.0, 1.25], rowH: 0.42, fontFace: BFONT, border: { pt: 0.5, color: "E2DCD1" }, valign: "middle" });
// key reading
card(s, 7.15, 4.5, 5.6, 2.1, DARK);
s.addText("Lectura clave", { x: 7.4, y: 4.65, w: 5.2, h: 0.35, color: AMBER, fontFace: HFONT, fontSize: 16, bold: true, margin: 0 });
s.addText([
  { text: "El 15 % de los clientes", options: { color: GOLD, bold: true, fontSize: 22, breakLine: true } },
  { text: "(Campeones B2B) explica el ", options: { color: WHITE, fontSize: 15 } },
  { text: "77 % de la facturación real.", options: { color: AMBER, bold: true, fontSize: 15, breakLine: true } },
  { text: "Esto justifica un trato de marketing diferenciado por segmento.", options: { color: "9FB3C8", fontSize: 12.5 } },
], { x: 7.4, y: 5.05, w: 5.25, h: 1.5, fontFace: BFONT, margin: 0, valign: "top", lineSpacingMultiple: 1.0 });

// ============================================================
// SLIDE 10 — CONCLUSIONES Y RECOMENDACIONES (1 min)
// ============================================================
s = pres.addSlide();
header(s, "Conclusiones y recomendaciones", "Del modelo a la acción comercial", "6");
// conclusions left
card(s, 0.55, 1.75, 5.9, 4.65);
s.addText("Conclusiones", { x: 0.85, y: 1.95, w: 5.3, h: 0.4, color: STEEL, fontFace: HFONT, fontSize: 18, bold: true, margin: 0 });
const concl = [
  "K=4 entrega segmentos coherentes y accionables; tres algoritmos lo validan.",
  "El modelo confirma y cuantifica el Pareto: 15 % de clientes = 77 % de la facturación.",
  "Cada segmento recibe nombre comercial y estrategia concreta.",
  "Pipeline reproducible y listo para aplicarse a datos reales de otra empresa del rubro.",
];
concl.forEach((c, i) => {
  s.addText(c, { x: 0.95, y: 2.4 + i * 0.95, w: 5.3, h: 0.9, color: INK, fontFace: BFONT, fontSize: 13, bullet: { code: "2022", indent: 14 }, margin: 0, valign: "top", lineSpacingMultiple: 1.03 });
});
// strategies right
card(s, 6.7, 1.75, 6.05, 4.65, DARK);
s.addText("Estrategia por segmento", { x: 7.0, y: 1.95, w: 5.4, h: 0.4, color: AMBER, fontFace: HFONT, fontSize: 18, bold: true, margin: 0 });
const strat = [
  [GOLD, "Campeones (B2B)", "Programa premium: cuenta corriente, gestor dedicado, descuentos por volumen."],
  [GREEN, "Activos Recientes", "Up-sell de complementarios + programa de puntos para subir frecuencia."],
  [AMBER2, "Esporádicos / Riesgo", "Campaña de re-activación con descuento personalizado."],
  [GRAY, "Perdidos", "Win-back low-cost: email de re-enganche."],
];
strat.forEach((t, i) => {
  const y = 2.45 + i * 0.96;
  s.addShape(pres.shapes.RECTANGLE, { x: 7.0, y: y + 0.05, w: 0.12, h: 0.8, fill: { color: t[0] } });
  s.addText(t[1], { x: 7.25, y, w: 5.3, h: 0.32, color: t[0], fontFace: HFONT, fontSize: 14.5, bold: true, margin: 0 });
  s.addText(t[2], { x: 7.25, y: y + 0.33, w: 5.3, h: 0.6, color: "C7D3DE", fontFace: BFONT, fontSize: 11.5, margin: 0, valign: "top" });
});
// future line
s.addText("Trabajo futuro: usar los clusters como etiquetas para un clasificador supervisado (Random Forest / XGBoost) y operar la segmentación en tiempo real.", { x: 0.85, y: 6.55, w: 11.8, h: 0.35, color: STEEL, fontFace: BFONT, fontSize: 11, italic: true, align: "center", margin: 0 });

// ============================================================
pres.writeFile({ fileName: "F:/CIENCIA DE DATOS2026/CienciadeDatos/Aprendisajeautomatico/TrabajoFinalApAut/reports/presentacion_video/Presentacion_TrabajoFinal_AA.pptx" })
  .then((f) => console.log("OK ->", f))
  .catch((e) => { console.error("ERR", e); process.exit(1); });
