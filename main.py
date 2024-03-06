from typing import Union, List, Dict
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from dateutil import parser
from typing import List
import pyarrow.parquet as pq
import numpy as np 
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

# Creacion de una aplicacion FastApi

app = FastAPI()



#Presentación------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root():
    message = """
        <head>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    </head>
    <style>
        .custom-text {
            color: #333333;  /* Gris oscuro */
            font-family: 'Roboto', sans-serif;  /* Utiliza la fuente Roboto o la que hayas elegido */
        }
    </style>
    <div style="text-align: center; font-size: 24px; margin-bottom: 20px;" class="custom-text">
        ¡Welcome to my MLOPS project!
    </div>
    <div style="text-align: center; font-size: 18px; margin-bottom: 40px;" class="custom-text">
        FastAPI-Project - Recommendation system of steam games.(MVP)
    </div>
    <div style="text-align: center; font-size: 18px; margin-bottom: 20px;" class="custom-text">
        DataScientist: Lautaro Hillkirk,
    </div>
    <div style="text-align: center; font-size: 18px; margin-bottom: 20px;" class="custom-text">
        "Individual Project"
    </div>    
    <div style="text-align: center;">
        <form action='/redirect' style="display: inline-block;">
            <input type='submit' value='Enter to the API' style="font-size: 16px; background-color: orange; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        </form>
    </div>
    """
    return HTMLResponse(content=message)

@app.get("/redirect", include_in_schema=False)
def redirect_to_docs():
    link = "https://pi01-steam-mlops.onrender.com/docs"
    raise HTTPException(status_code=302, detail="Redirecting", headers={"Location": link})




# ejecutar uvicorn main:app --reload para cargar en el servidor



# ------- 1- FUNCION developer -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.get(path = '/developer',
          description = """ <font color="blue">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el nombre del desarrollador en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver la cantidad de items y porcentaje de contenido Free por año de ese desarrollador.
                        </font>
                      
                                                                      """,
         tags=["Consultas Generales"])


def developer(desarrollador: str = Query(..., 
                            description="Desarrollador del videojuego", 
                            example='Valve')):
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_items_developer.parquet')
    df_items_developer = pq.read_table(path_to_parquet).to_pandas()

    '''
    Esta función devuelve información sobre una empresa desarrolladora de videojuegos.
         
    Args:
        desarrollador (str): Nombre del desarrollador de videojuegos.
    
    Returns:
        list: Una lista de diccionarios que contiene información sobre la empresa desarrolladora.
            - 'anio' (int): Año de lanzamiento.
            - 'cantidad_items' (int): Cantidad de items desarrollados en ese año.
            - 'porcentaje_gratuito' (float): Porcentaje de contenido gratuito desarrollado en ese año.
    '''
    # Filtra el dataframe por desarrollador de interés
    data_filtrada = df_items_developer[df_items_developer['developer'] == desarrollador]
    # Calcula la cantidad de items por año
    cantidad_por_año = data_filtrada.groupby('release_anio')['item_id'].count().astype(int)
    # Calcula la cantidad de elementos gratis por año
    cantidad_gratis_por_año = data_filtrada[data_filtrada['price'] == 0.0].groupby('release_anio')['item_id'].count().astype(int)
    # Calcula el porcentaje de elementos gratis por año
    porcentaje_gratis_por_año = ((cantidad_gratis_por_año / cantidad_por_año) * 100).fillna(0).astype(int)

    result_list = []
    for anio, cantidad_items in cantidad_por_año.items():
        item = {"anio": int(anio)}

        if anio in porcentaje_gratis_por_año:
            item["cantidad_items_gratuitos"] = int(
                cantidad_items * porcentaje_gratis_por_año[anio] / 100
            )
            item["porcentaje_gratuito"] = int(porcentaje_gratis_por_año[anio])
        else:
            item["cantidad_items_gratuitos"] = 0
            item["porcentaje_gratuito"] = 0

        result_list.append(item)

    return result_list


# ------- 2- FUNCION userdata ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.get (path = '/userdata',
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el user_id en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver la cantidad de dinero gastado por el usuario, el porcentaje de recomendación que realiza el usuario y cantidad de items que tiene el mismo.
                        </font>
                        """,
         tags=["Consultas Generales"])
def userdata(user_id: str = Query(..., 
                                description="Identificador único del usuario", 
                                example="EchoXSilence")):

    # Lee los archivos parquet de la carpeta data
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_gastos_items.parquet')
    df_gastos_items = pq.read_table(path_to_parquet).to_pandas()
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_reviews.parquet')
    df_reviews = pq.read_table(path_to_parquet).to_pandas()
    '''
    Esta función devuelve información sobre un usuario según su 'user_id'.
         
    Args:
        user_id (str): Identificador único del usuario.
    
    Returns:
        dict: Un diccionario que contiene información sobre el usuario.
            - 'cantidad_dinero' (int): Cantidad de dinero gastado por el usuario.
            - 'porcentaje_recomendacion' (float): Porcentaje de recomendaciones realizadas por el usuario.
            - 'total_items' (int): Cantidad de items que tiene el usuario.
    '''
    # Filtra por el usuario de interés
    usuario = df_reviews[df_reviews['user_id'] == user_id]
    # Calcula la cantidad de dinero gastado para el usuario de interés
    cantidad_dinero = df_gastos_items[df_gastos_items['user_id'] == user_id]['price'].iloc[0]
    # Busca el count_item para el usuario de interés    
    count_items = df_gastos_items[df_gastos_items['user_id'] == user_id]['items_count'].iloc[0]
    
    # Calcula el total de recomendaciones realizadas por el usuario de interés
    total_recomendaciones = usuario['reviews_recommend'].sum()
    # Calcula el total de reviews realizada por todos los usuarios
    total_reviews = len(df_reviews['user_id'].unique())
    # Calcula el porcentaje de recomendaciones realizadas por el usuario de interés
    porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100
    
    return {
        'Usuario': user_id,
        'cantidad_dinero': int(cantidad_dinero),
        'porcentaje_recomendacion': round(float(porcentaje_recomendaciones), 2),
        'total_items': int(count_items)
    }


# ------- 3- FUNCION user_for_genre ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.get(path = "/user_for_genre/", 
        description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el genero en el box abajo, ejemplo: Action.<br>
                        3. Scrollear a "Resposes" para ver la cantidad de dinero gastado por el usuario, el porcentaje de recomendación que realiza el usuario y cantidad de items que tiene el mismo.
                        </font>
                        """,
         tags=["Consultas Generales"])

@app.get("/user_for_genre/")
def userforgenre(genero):
    # Lee el archivo Parquet
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_UserForGenre.parquet')
    df_playtimeforever = pq.read_table(path_to_parquet).to_pandas()

    # Filtra el DataFrame por el género de interés
    data_por_genero = df_playtimeforever[df_playtimeforever['genres'] == genero]

    # Agrupa el DataFrame filtrado por usuario y suma la cantidad de horas del usuario que se ingresó como input
    top_users = data_por_genero.groupby(['user_id'])['playtime_horas'].sum().nlargest(5).reset_index()

    # Se hace un diccionario vacío para guardar los datos que se necesitan
    top_users_dict = {}
    for index, row in top_users.iterrows():
        # User info recorre cada fila del top 5 y lo guarda en el diccionario
        user_info = {
            'user_id': row['user_id'],
            'hours_game': row['hours_game'],
            'year': row['year']
            }
        top_users_dict[index + 1] = user_info

    return top_users_dict
# ------- 4- FUNCION best_developer_year ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Definir la ruta de FastAPI para la función best_developer_year
@app.get("/best_developer/", 
        description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el año en el box abajo, ejemplo: 2015.<br>
                        3. Scrollear a "Resposes" para ver los mejores developers.
                        </font>
                        """,
         tags=["Consultas Generales"])

def best_developer_year(year: int):

    # Lee el archivo parquet de la carpeta data
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_best_developer.parquet')
    df = pq.read_table(path_to_parquet).to_pandas()




    
    # Filtrar el DataFrame por el año especificado
    result_df = df[df['year'] == year]
    
    response_data = [{"Puesto 1": result_df.iloc[0]['developer']},
                    {"Puesto 2": result_df.iloc[1]['developer']},
                    {"Puesto 3": result_df.iloc[2]['developer']}]
    
    return response_data









# ------- 5- FUNCION developer_reviews_analysis -------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Definir la ruta de FastAPI para la función developer_reviews_analysis
@app.get(path = "/developer_reviews_analysis/",
        description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el desarrollador en el box abajo, ejemplo: Valve.<br>
                        3. Scrollear a "Resposes" para el analisis de sentimiento del desarrollador.
                        </font>
                        """,
         tags=["Consultas Generales"])
def developer_reviews_analysis_endpoint(desarrollador: str):

    # Lee el archivo parquet de la carpeta data
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data','df_items_developer.parquet')
    df = pq.read_table(path_to_parquet).to_pandas()


    # Filtrar por la empresa desarrolladora
    result_df = df[df['developer'] == desarrollador]

    # Convertir a formato de diccionario
    response_data = result_df.set_index('developer').to_dict(orient='index')
    response_data = response_data.tolist
    return response_data










#       RECOMENDACIÓN DE USUARIO   ---------------------------------------------------------------------------

@app.get("/recomendacion_usuario/", tags=['recomendacion_usuario item_item'])
def item(item_id: int) -> List[str]:
    """
    Descripción: Ingresando el id de producto, devuelve una lista con 5 juegos recomendados similares al ingresado.
    
    Parámetros:
        - item_id (str): Id del producto para el cual se busca la recomendación. Debe ser un número, ejemplo: 761140
        
    Ejemplo de retorno: ['弹炸人2222', 'Uncanny Islands', 'Beach Rules', 'Planetarium 2 - Zen Odyssey', 'The Warrior Of Treasures']
    """

    # Lee el archivo parquet de la carpeta data
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'recomienda_item_item.parquet')
    df = pq.read_table(path_to_parquet).to_pandas()
        
    # Filtrar el DataFrame por el año especificado
    result_df = df[df['item_id'] == item_id]
    
    # Obtener la lista de recomendaciones como una lista de strings
    recomendaciones = result_df['Recomendaciones'].tolist()
 
    return recomendaciones


