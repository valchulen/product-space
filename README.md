# Difusión sobre Espacio de Productos

Para correr es necesario tener `eb-devs` instalado como `pypdevs`.
Luego se puede correr `python main.py`.

Opciones:

- --duration DURATION, -d DURATION: cantidad de iteraciones de simulación
- --logging-level LOGGING_LEVEL, -l LOGGING_LEVEL: nivel de logging de python (default: INFO)
- --X-matrices-file X_MATRICES_FILE, -f X_MATRICES_FILE: archivo con datos de entrada (default: data/stage1_data.pkl)
- --year YEAR, -y YEAR: año del cual tomar los datos para iniciar la simulación (default: 2000)
- --big-omega BIG_OMEGA, -O BIG_OMEGA: parámetro de umbral para regular la difusión (default: 0.55)
- --metrics-folder METRICS_FOLDER, -m METRICS_FOLDER: carpeta donde guardar las métricas generadas por la simulación
- --phi-matrix-update PHI_MATRIX_UPDATE, -u PHI_MATRIX_UPDATE: booleano que regula si usar la versión con retroalimentación (default: False, sin retroalimentación)
- --exports-history EXPORTS_HISTORY, -e EXPORTS_HISTORY: booleano que indica si se debe guardar el historial completo de exportaciones de cada país (default: False)

## Datos de entrada

El script toma un archivo en formato pickle usando la opción --X-matrices-file.
Este debe contener un diccionario con las siguientes claves:

- X_matrices: diccionario donde las claves son años y los valores son matrices binarias de exportaciones por país
- countries: lista de los códigos de los países
- products: lista de los códigos de los productos. Actualmente en desuso por parte del simulador
- phi (opcional): matriz de disimilaridad entre productos. TODO: que el simulador use esta matriz si se encuentra disponible

## Métricas de salida

El script genera los siguientes archivos:

- d_vector.csv: estadísticas sobre el vector de distancias de un país a todos los productos (columnas: "country", "generation", "p25", "p75", "mean_d")
- exports.csv: cantidad de exportaciones de cada país en cada iteración de la simulación (columnas: "country", "generation", "count_exports")
- exports_history.pkl (opcional, según parámetro --exports-history): historial completo de exportaciones de cada país en cada iteración de la simulación, en forma de lista de triplas con (country, generation, exports_vector)

# Notebooks

- TP.ipynb: notebook principal donde se explica el modelo y se muestra resultados de la experimentación realizada para el TP
- Replica.ipynb: testeos hechos para intentar replicar la publicación original de Hidalgo

# Problemas posibles

## JupyterLab no muestra gráficos de Plotly

Instalar extensiones:

```
jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyterlab-plotly
```

