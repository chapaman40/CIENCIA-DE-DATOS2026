import json

notebook_path = r"f:\CIENCIA DE DATOS2026\CienciadeDatos\Mineriadedatos\Clase1.2.ipynb"
with open(notebook_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for cell in data.get("cells", []):
    if cell.get("cell_type") == "code":
        sources = cell.get("source", [])
        for i, s in enumerate(sources):
            if "sns.countplot(data=df, x=\"Estado_Cuenta\", palette='Set2')" in s:
                sources[i] = s.replace(
                    "sns.countplot(data=df, x=\"Estado_Cuenta\", palette='Set2')", 
                    "sns.countplot(data=df, x=\"Estado_Cuenta\", hue=\"Estado_Cuenta\", palette='Set2', legend=False)"
                )

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=1)

print("Notebook patched successfully!")
