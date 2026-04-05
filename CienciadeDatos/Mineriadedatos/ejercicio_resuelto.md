# Resolución de Ejercicio: KDD y CRISP-DM

## 1. Identificación de Fases en KDD y CRISP-DM

**¿Cómo aplicaría el proceso KDD a estos datos?**
El proceso KDD (Knowledge Discovery in Databases) se aplicaría de la siguiente manera secuencial:
1. **Selección:** Elegiríamos todas las variables relevantes del conjunto de datos (Edad, Plan, Consumo_GB, Reclamos, Estado_Cuenta) para entender el comportamiento de pago o morosidad de los clientes.
2. **Preprocesamiento:** Revisaríamos si existen valores nulos (vacíos), duplicados o atípicos (por ejemplo, edades negativas o consumos imposibles). En esta muestra pequeña, los datos parecen limpios.
3. **Transformación:** Las variables categóricas de texto (`Plan` y `Estado_Cuenta`) deberían ser convertidas a valores numéricos para que un algoritmo pueda procesarlas.
4. **Minería de Datos (Modeling):** Aplicar modelos (como árboles de decisión o regresión logística) para descubrir qué tipo de cliente tiende a ser moroso.
5. **Interpretación/Evaluación:** Analizar los resultados del modelo para validar y obtener "conocimiento" útil para el negocio, como por ejemplo: "clientes con más de 2 reclamos tienden a ser morosos".

**¿Qué pasos seguirías antes de extraer patrones y qué fase de CRISP-DM corresponde?**
Antes de aplicar algoritmos para extraer patrones (fase de *Modeling* en CRISP-DM), seguiría estos pasos:
1. **Entendimiento del Negocio (Business Understanding):** Definir el objetivo, que en este caso parece ser identificar por qué los clientes caen en estado de cuenta "Moroso".
2. **Comprensión de los Datos (Data Understanding):** Ver estadísticas descriptivas, tipos de datos y gráficos para conocer la distribución de las variables.
3. **Preparación de los Datos (Data Preparation):** Llenar/eliminar valores nulos, estandarizar el texto y codificar variables categóricas para dejarlas listas para el algoritmo.

---

## 2. Preprocesamiento de Datos

**¿Qué problemas podrías encontrar en los datos?**
En un dataset real de telecomunicaciones podríamos encontrar: valores faltantes (NaN), consumos de datos registrados en diferentes unidades (MB vs GB), edades erróneas (ej. 150 años) o errores tipográficos en los nombres de los planes (ej. "basico" vs "Básico").

**¿Hay valores inconsistentes o que deban transformarse?**
En esta muestra de 5 registros no hay inconsistencias puras (como edades negativas), pero los atributos textuales (`Plan` y `Estado_Cuenta`) **deben transformarse** a valores numéricos para su uso algorítmico. 

**¿Cómo manejarías los valores categóricos?**
*   **Estado de Cuenta:** Utilizaría un *Label Encoding* o reemplazo binario (ej. `Pagado = 0`, `Moroso = 1`), al ser la variable a predecir.
*   **Plan Contratado:** Dado que hay una jerarquía de valor (Básico < Estándar < Premium), usaría *Ordinal Encoding* (ej. `Básico = 1`, `Estándar = 2`, `Premium = 3`).

**Código en Python:**

```python
import pandas as pd

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
print("--- Información del DataFrame ---")
print(df.info())
print("\n--- Descripción Estadística ---")
print(df.describe())

# Verificar valores faltantes (Nulos/NaN)
print("\n--- Valores Faltantes ---")
print(df.isnull().sum())

# Verificar valores duplicados
print("\n--- Filas Duplicadas ---")
print("Cantidad:", df.duplicated().sum())
```

---

## 3. Exploración de Datos

```python
import seaborn as sns 
import matplotlib.pyplot as plt 

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
```

---

## 4. Interpretación de Resultados

**¿Qué tendencias observas en los datos?**
Existe una segmentación clara. Por un lado, tenemos usuarios mayores (35 y 40 años) con planes "Premium" que tienen un consumo de datos muy alto (45-50 GB) y cero reclamos. Por otro lado, tenemos clientes con planes "Básico" o "Estándar" que tienen un consumo de datos mucho menor (5-10 GB) y presentan reclamos.

**¿Hay alguna relación entre el consumo de datos y el estado de cuenta?**
Contrario a lo que podría pensarse, los clientes con **mayor consumo de datos** (45 y 50 GB) tienen su estado de cuenta **"Pagado"**. Los clientes que son morosos tienen consumos bajos a moderados (7 y 10 GB). 

**¿Los clientes morosos tienen características en común?**
Sí, comparten características marcadas:
1.  **Alta cantidad de reclamos:** Los clientes morosos tienen 2 y 3 reclamos, mientras que los clientes que pagan tienen 0 o 1. La insatisfacción con el servicio podría ser un detonante para dejar de pagar.
2.  **Planes más económicos:** Pertenecen a los planes "Básico" e "Estándar".
3.  **Consumo moderado/bajo:** Consumen entre 7 y 10 GB.
4.  **Edad:** Suelen ser ligeramente más jóvenes (22 y 32 años), aunque hay excepciones (cliente de 25 años que pagó).
