# FilmRental-Data

Proyecto de **Extracción, Transformación y Carga (ETL)** desarrollado para gestionar y procesar información de un videoclub. Incluye pipelines en Python, uso de archivos CSV como fuente de datos, y notebooks con procesos interactivos para el análisis y transformación.

---

##  Estructura del Proyecto

```
FilmRental-Data/
│
├── conf/
│   └── Guide.env
│
├── data/
│   ├── clientes.csv
│   ├── peliculas.csv   # Descarga si deseas
│   └── alquileres.csv
│
│
├── src/
│   ├── questions.ipynb
│   └── ETL.py
│
└── README.md               
```

---

##  Objetivo del Proyecto

El objetivo es construir un proceso **ETL automatizado** para un videoclub, permitiendo:

-  **Extracción** de los datos desde archivos CSV o APIs.
-  **Transformación**: limpieza, normalización y enriquecimiento.
-  **Carga** hacia el destino deseado.
-  Análisis.

---

## Tecnologías Utilizadas

- **Python 3.13**
- **Pandas**
- **Jupyter Notebook**
- **dotenv**  (Necesaria para manejar variables de entorno)
- **Requests** 
- **ipywidgets** (He tenido que agregar esta libreria para crear menús desplegables en el notebooks.)
- **jupyterlab_widgets** (Necesaria para que los widgets funcionen correctamente en JupyterLab.)
- **datetime** 


---
## Configuración de la API KEY

- Entra en la web https://developer.themoviedb.org/
- Crea una cuenta y guarda tu API KEY
  
---
## Configuración del Entorno

1. Crear un archivo `.env` en la carpeta `conf/` basado en `Guide.env`.

2. Instalar dependencias:

```bash
!pip install python-dotenv
!pip install requests
!pip install ipywidgets
!pip install jupyterlab_widgets
```


3. Ejecutar el script ETL desde consola de JUPYTER LAB:

```bash
python src/ETL.py
```

---

## Uso del ETL

El script `ETL.py` permite:

- Elegir en modo API o modo CSV para descargar el archivo.
- Cargar los datasets `clientes.csv` y `alquileres.csv`.
- Crea o carga `peliculas.csv`.
- Validar y limpiar los datos.
- Generar un dataset final listo para análisis.

---

## Notebooks Disponibles

El notebooks incluido permite:

- Unificar información relevante.
- Exploración de los datasets.
- Resolución de preguntas analíticas.

---

## Posibles Mejoras Futuras

- Conexión a una base de datos MySQL.
- ( Pensando en posibles mejoras. )

---

## Autor

Juan Rafael Rodríguez Gómez

