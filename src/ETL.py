import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import date

#Definimos variables ( constantes )
#----------------------------------

#------------IMPORTANTE------------------------------
"""Elegimos el modo que vamos a trabajar directamente
   hacienodo peticiones desde la API o descargando el
   archivo CVS"""
MODO = "API"
# MODO = "CSV"
#---------------------------------
TOP = 30
ANOS_ATRAS = 5
ORDENAR_POR = "popularity.desc"

GENEROS_SELECCIONADOS = {
    28: "Acción",
    12: "Aventura",
    16: "Animación",
    35: "Comedia",
    80: "Crimen",
    18: "Drama",
    27: "Terror",
    878: "Ciencia ficción",
    14: "Fantasía",
    10749: "Romance"
}

# Definimos las rutas de los archivos

ruta_base = "../data"
ruta_peliculas = "../data/peliculas.csv"
ruta_clientes = "../data/clientes.csv"
ruta_alquileres = "../data/alquileres.csv"

# Utilizamos date para ir 5 años atras y nos de una decha 
# que sea 5 años a partir de este año pero el mes 1 y dia 1
hoy = date.today()
fecha_inicio = date(hoy.year - ANOS_ATRAS, 1, 1)


def obtener_pagina_descubrir(api_key: str, id_genero: int, pagina: int):
    """
    Llama a /discover/movie para de un género obtener una página.
    """
    url = "https://api.themoviedb.org/3/discover/movie"
    parametros = {
        "api_key": api_key,
        "language": "es-ES",
        "sort_by": ORDENAR_POR,
        "with_genres": id_genero,
        "primary_release_date.gte": fecha_inicio.isoformat(),
        "primary_release_date.lte": hoy.isoformat(),
        "page": pagina
    }
    respuesta = requests.get(url, params=parametros)
    datos=respuesta.json()
    
    # Debug: total de paginas por genero
    #------------------------------------
    # print(id_genero,datos.get('total_pages'))
    #------------------------------------
    return datos


def obtener_peliculas_por_genero(api_key: str, id_genero: int, limite: int):
    """
    Devuelve una lista de películas para un género concreto,
    gestionando la paginación internamente y evitando duplicados
    dentro del mismo género.
    """
    peliculas = []
    ids_vistos = set()   # Creo medida para evitar duplicados
    pagina = 1
    # Debug: pinta id peli que descargo
    #------------------------------------
    # print(id_genero)
    #------------------------------------
    
    while len(peliculas) < limite:
        
        datos = obtener_pagina_descubrir(api_key, id_genero, pagina)
        resultados = datos.get("results", [])

        # Si funciona la API se detiene 
        if not resultados:
            break
        # Peliculas pag
        for pelicula in resultados:
            id_pelicula = pelicula.get("id")

            # Evita duplicados por paginacion
            if id_pelicula in ids_vistos:
                continue

            ids_vistos.add(id_pelicula)
            peliculas.append(pelicula)

            # Se detiene cuando se alcanza el limite
            if len(peliculas) >= limite:
                # Debug: pinta id peli y numero de pelis se descargo
                #------------------------------------
                # print(f"Creado genero {id_genero}: n pelis {limite}")
                #------------------------------------
                break

        pagina += 1

        # Fin de la paginación
        if pagina > datos.get("total_pages", 1):
            break

    return peliculas


def construir_peliculas_desde_api(api_key: str):
    """
    Descarga películas desde TMDB y construye el DataFrame.
    """
    # Contador para cambiar de filas 
    
    ranking = 1
    filas = []
    
    # Recorre el diccionario por generos 
    for id_genero, nombre_genero in GENEROS_SELECCIONADOS.items():
        # Debug: genero descargando
        #------------------------------------
        # print(f"Descargando {nombre_genero} {id_genero}")
        #------------------------------------
        # Las descarga
        peliculas_genero = obtener_peliculas_por_genero( api_key, id_genero, TOP )
        # Debug:Pelis por genero
        #------------------------------------
        # print(f"{nombre_genero}: películas {len(peliculas_genero)}")
        #------------------------------------

        
        # Avisa si hay menos peliculas que tienen TOP 
        if len(peliculas_genero) < TOP:
            print(f"De: {nombre_genero} tan solo devolvio {len(peliculas_genero)} películas no llega a {TOP} que has marcado")

        # Creo el dataframe por cada peli / fila
        for pelicula in peliculas_genero:
            filas.append({
                "genre_id": id_genero,
                "genre_name": nombre_genero,
                "rank_in_genre": ranking,
                "movie_id": pelicula.get("id"),
                "title": pelicula.get("title"),
                "original_title": pelicula.get("original_title"),
                "original_language": pelicula.get("original_language"),
                "release_date": pelicula.get("release_date"),
                "popularity": pelicula.get("popularity"),
                "vote_average": pelicula.get("vote_average"),
                "vote_count": pelicula.get("vote_count"),
            })
            ranking += 1 
    #DEBUG: Filas descargadas
    #------------------------------------        
    # print(len(filas))
    #------------------------------------
    return pd.DataFrame(filas)


def obtener_peliculas():
    """
    Carga las películas según el modo:
    - API: descarga desde TMDB
    - CSV: lee peliculas.csv o lo crea si no existe
    """
    if MODO == "API":
        ruta_env = "../conf/.env"
        load_dotenv(ruta_env)
        api_key = os.getenv("TMDB_API_KEY")

        if not api_key:
            raise ValueError("COMPRUEBA QUE LA API KEY ESTA EN ../conf/.env")

        return construir_peliculas_desde_api(api_key)

    if MODO == "CSV":
        # Comprueba si existe el archivo
        if os.path.exists(ruta_peliculas):
            # Si existe lee y termina
            return pd.read_csv(ruta_peliculas)
    
        print("PELICULAS NO EXITE, SE CREA DESDE LA API")
        
        # Carga la API KEY
        ruta_env = "../conf/.env"
        load_dotenv(ruta_env)
        api_key = os.getenv("TMDB_API_KEY")
        
        # API KEY bad, ValueError
        if not api_key:
            raise ValueError("COMPRUEBA QUE LA API KEY ESTA EN ../conf/.env")
        # Descarga las pelis
        df = construir_peliculas_desde_api(api_key)

        os.makedirs(ruta_base, exist_ok=True)
        df.to_csv(ruta_peliculas, index=False )

        print(f"✅ Archivo creado: {ruta_peliculas}")
        return df

    raise ValueError("Comprueba MODO de ser 'API' o 'CVS' COMENTA LA QUE NO TE INTERESE")


# Cargo los datos y muestro lo cargado
clientes = pd.read_csv(ruta_clientes)
alquileres = pd.read_csv(ruta_alquileres)
peliculas = obtener_peliculas()

print("Modo:", MODO)
print("Clientes:", clientes.shape)
print("Alquileres:", alquileres.shape)
print("Películas:", peliculas.shape)



