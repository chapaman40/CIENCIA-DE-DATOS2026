import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    print("--- 2. PREPROCESAMIENTO DE DATOS ---")
    # Crear DataFrame con los datos del ejercicio
    datos = {
        "Cliente": [1, 2, 3, 4, 5],
        "Edad": [25, 40, 32, 22, 35],
        "Plan": ["Básico", "Premium", "Estándar", "Básico", "Premium"],
        "Consumo_GB": [5, 50, 10, 7, 45],
        "Reclamos": [1, 0, 2, 3, 0],
        "Estado_Cuenta": ["Pagado", "Pagado", "Moroso", "Moroso", "Pagado"]
    }
    df = pd.DataFrame(datos)

    # Inspeccionar los datos básicos
    print("\n[INFO] Información del DataFrame:")
    print(df.info())
    
    print("\n[INFO] Descripción Estadística:")
    print(df.describe())

    # Verificar valores faltantes (Nulos/NaN)
    print("\n[VALIDACIÓN] Valores Faltantes por columna:")
    print(df.isnull().sum())

    # Verificar valores duplicados
    print("\n[VALIDACIÓN] Cantidad de Filas Duplicadas:")
    print(df.duplicated().sum())
    
    print("\n--- 3. EXPLORACIÓN DE DATOS (Mostrando gráficos...) ---")

    # 1. Generar un histograma del consumo de datos (GB)
    plt.figure(figsize=(8, 4))
    sns.histplot(df["Consumo_GB"], bins=5, kde=True, color='skyblue')
    plt.title('Distribución del Consumo de Datos (GB)')
    plt.xlabel('Consumo (GB)')
    plt.ylabel('Frecuencia')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # 2. Crear un gráfico de barras del "Estado de Cuenta"
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="Estado_Cuenta", palette='Set2')
    plt.title('Proporción de Clientes: Pagado vs Moroso')
    plt.xlabel('Estado de Cuenta')
    plt.ylabel('Cantidad de Clientes')
    plt.show()

if __name__ == "__main__":
    main()
