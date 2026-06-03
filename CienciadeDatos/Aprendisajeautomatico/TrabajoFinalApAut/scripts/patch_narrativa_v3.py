"""Reconcilia la narrativa hardcodeada (v1: 1.000 clientes) de los notebooks
a los números de la v3 (5.000 clientes). Toca SOLO celdas markdown, salvo una
anotación específica de figura en una celda de código de NB4.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks"

MD = {
    "1.0-ig-eda-y-limpieza.ipynb": [
        ("10.321 trans", "50.730 trans"),
        ("el 15 % de los clientes (Campeones B2B)", "el 14 % de los clientes (Campeones B2B)"),
        ("explica el 77 % de la facturación. Sobre eso", "explica el 73 % de la facturación. Sobre eso"),
        ("El README documenta `~60 compras masivas`", "El README documenta `~150 compras masivas`"),
        ("`data/raw/transacciones_ecommerce.csv` (10.321 transacciones)",
         "`data/raw/transacciones_ecommerce.csv` (50.730 transacciones)"),
        ("`data/interim/transacciones_limpias.parquet` (10.132 filas)",
         "`data/interim/transacciones_limpias.parquet` (49.909 filas)"),
        ("**NO eliminar** los 3 outliers extremos (>$10M ARS)",
         "**NO eliminar** los 10 outliers extremos (>$10M ARS)"),
    ],
    "2.0-ig-features-rfm.ipynb": [
        ("`data/processed/clientes_rfm.parquet` (999 clientes)",
         "`data/processed/clientes_rfm.parquet` (4.992 clientes)"),
        ("inflación acumulada ~120 % en 24 meses", "inflación acumulada ~160 % en 24 meses"),
    ],
    "_disabled_0.0-ig-resumen-ejecutivo.ipynb": [
        ("el **15 % de los clientes", "el **14 % de los clientes"),
        ("(Campeones B2B) explica el 77 % de la facturación real**",
         "(Campeones B2B) explica el 73 % de la facturación real**"),
        ("| **🏆 Campeones (B2B)** | 154 | 15.4 % | **76.7 %**",
         "| **🏆 Campeones (B2B)** | 691 | 13.8 % | **73.1 %**"),
        ("| 🛒 Activos Recientes | 306 | 30.6 % | 16.4 %",
         "| 🛒 Activos Recientes | 1.697 | 34.0 % | 19.0 %"),
        ("| ⚠️ Esporádicos / En Riesgo | 322 | 32.2 % | 5.6 %",
         "| ⚠️ Esporádicos / En Riesgo | 1.694 | 33.9 % | 6.9 %"),
        ("| 💤 Perdidos | 217 | 21.7 % | 1.2 %",
         "| 💤 Perdidos | 910 | 18.2 % | 1.0 %"),
        ("Dataset limpio (10.132 transacciones)", "Dataset limpio (49.909 transacciones)"),
        ("complementarias (999 clientes)", "complementarias (4.992 clientes)"),
    ],
    "_disabled_4.0-ig-clustering.ipynb": [
        ("para legibilidad con 999 clientes", "para legibilidad con 4.992 clientes"),
        ("El Silhouette **promedio** (0.365)", "El Silhouette **promedio** (0.368)"),
    ],
    "_disabled_5.0-ig-interpretacion-y-estrategias.ipynb": [
        ("Recency media-alta (~265 dias)", "Recency media-alta (~287 dias)"),
        ("Se construyó sobre 999 clientes", "Se construyó sobre 4.992 clientes"),
        ("🏆 Campeones (B2B): **15 % clientes / 77 % facturación**",
         "🏆 Campeones (B2B): **14 % clientes / 73 % facturación**"),
        ("🛒 Activos Recientes: 31 % / 16 %", "🛒 Activos Recientes: 34 % / 19 %"),
        ("⚠️ Esporádicos / En Riesgo: 32 % / 6 %", "⚠️ Esporádicos / En Riesgo: 34 % / 7 %"),
        ("💤 Perdidos: 22 % / 1 %", "💤 Perdidos: 18 % / 1 %"),
    ],
}

# Reemplazos en celdas de CÓDIGO (solo NB4: anotación de la figura del codo + comentarios)
CODE = {
    "4.0-ig-clustering.ipynb": [
        ("K=2 (rojo): maximiza Silhouette\\npero produce particion trivial\\n(solo activos vs inactivos)",
         "K=2-3: maximo Silhouette\\npero particion demasiado gruesa\\n(activos vs inactivos)"),
        ("# El K que MAXIMIZA Silhouette es K=2, pero produce solo una particion trivial",
         "# El K que MAXIMIZA Silhouette es bajo (K=2-3), pero produce particiones triviales"),
        ("print(\"Justificacion: K=2 es trivial para marketing, K=4 es estandar RFM.\")",
         "print(\"Justificacion: K bajo (2-3) es trivial para marketing, K=4 es estandar RFM.\")"),
    ],
}


def patch(fname, md_reps, code_reps):
    path = NB / fname
    if not path.exists():  # claves "_disabled_" → ya aplicadas en corridas previas
        return
    nb = json.loads(path.read_text(encoding="utf-8"))
    counts = {}
    for cell in nb["cells"]:
        if cell.get("cell_type") == "markdown":
            reps = md_reps
        elif cell.get("cell_type") == "code":
            reps = code_reps
        else:
            continue
        if not reps:
            continue
        text = "".join(cell.get("source", []))
        for old, new in reps:
            if old in text:
                text = text.replace(old, new)
                counts[old] = counts.get(old, 0) + 1
        cell["source"] = text.splitlines(keepends=True)
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n== {fname} ==")
    for old, _ in (md_reps + code_reps):
        safe = old[:60].encode("ascii", "replace").decode()
        print(f"  [{'OK' if counts.get(old) else 'MISS'}] {safe}")


for fname, md_reps in MD.items():
    patch(fname, md_reps, CODE.get(fname, []))
print("\nListo.")
