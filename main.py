from fastapi import FastAPI
import os
import pandas as pd
import pyarrow
import fastparquet
nuevo/games_API.parquet

app = FastAPI()

games = pd.read_parquet("/nuevo/games_API.parquet")
reviews = pd.read_parquet("/nuevo/reviews_games_API.parquet")
items = pd.read_parquet("/nuevo/items_games_API.parquet")


# 1
@app.get("/developer")
def developer(desarrollador : str):
# filtramos por desarrollador
    filtro = games[games["developer"] == desarrollador]
# no quedamos con nuestras columnas de interés
    reviews1 = reviews[["item_id", "year_release"]]
# hacemos un merge de tablas
    join = pd.merge(filtro, reviews1, on="item_id", how="inner")
# agrupamos por año, contamos los items y calculamos el porcentaje free
    agrupado = join.groupby('year_release').agg({
    'item_id': 'count',
    'price': lambda x: (x == 0.00).mean() * 100
    }).reset_index()
# renombramos las columnas
    agrupado.columns = ['Año', 'Cantidad de Items', 'Contenido Free']
# volvemos a ordenar de manera descendente por año
    agrupado = agrupado.sort_values(by='Año', ascending=False)
# formateamos el resultado
    diccionario_resultado = agrupado.to_dict(orient='records')

    return diccionario_resultado


# 2
@app.get("/userdata")
def userdata(user_id : str):
# filtramos por usuario
    filtro = reviews[reviews["user_id"] == user_id]
# nos quedamos con nuestras columnas de interés
    filtro_join = games[["item_id", "price"]]
# creamos una nueva tabla
    merge = pd.merge(filtro, filtro_join, on="item_id", how="inner") 
# nos quedamos con las columnas de interés
    seleccion = merge[["user_id", "item_id", "recommend", "price"]]  
# agrupamos por usuario, contamos los items, calculamos el porcentaje y sumamos precios
    userdata = seleccion.groupby("user_id").agg({
    'item_id': 'count',
    'recommend': lambda x: (x == 1).mean() * 100,
    "price": "sum"
    }).reset_index()
# renombramos y reordenamos columnas
    userdata.columns = ['Usuario', 'Items', 'Porcentaje de recomendación', "Dinero gastado"]
    userdata = userdata[['Usuario', 'Dinero gastado', 'Porcentaje de recomendación', 'Items']]
# transformamos el resultado
    diccionario_resultado = userdata.to_dict(orient='records')[0]

    return diccionario_resultado


# 3
@app.get("/user_for_genre")
def user_for_genre(genero : str):
# filtramos por género
    filtro = items[items["game_genre"] == genero]
# buscamos el usuario con mayor playtime_forever
    mascara = filtro["playtime_forever"].max()
    user = filtro["user_id"][mascara]
# agrupamos por total de horas por año
    horas_jugadas = filtro.groupby('year_release').agg({
    'playtime_forever': 'sum'
    }).reset_index()
# corregimos el orden a descendente
    horas_jugadas = horas_jugadas.sort_values(by='year_release', ascending=False)
# cambiamos el nombre de las columnas
    horas_jugadas.columns = ["Año", "Horas"]
# convertimos el df en lista
    lista_resultado = horas_jugadas.to_dict(orient='records')
# formateamos la salida
    out = {"Usuario con más horas jugadas para Género X" : user, "Horas jugadas": lista_resultado}

    return out


# 4
@app.get("/developer_reviews_analysis")
def best_developer_year(año : int):
# trabajamos con nuestras columnas de interés y formamos una nueva tabla
    games = games[["item_id", "developer"]]
    reviews = reviews[["item_id","recommend", "year_posted"]]
    merge = pd.merge(games, reviews, on="item_id", how="inner")
# filtramos de acuerdo al parámetro
    filtro = merge[merge["year_posted"] == año]
# agrupamos según suma de recommend por developer
    agrupado = filtro.groupby('developer').agg({
    'recommend': 'sum'
    }).reset_index()
# filtramos por ascendente y pedimos solo los 3 primeros
    agrupado = agrupado.sort_values("recommend", ascending=False).head(3)
    agrupado = agrupado.reset_index()
# nos quedamos con la columna de interés
    agrupado = agrupado["developer"]
# convertimos a dataframe para asegurar el formateo
    agrupado = pd.DataFrame(agrupado)
# formateamos el resultado
    valores = agrupado['developer'].tolist()
    lista_resultado = [{"Puesto {}: ".format(i + 1): valor} for i, valor in enumerate(valores)]

    return lista_resultado


# 5
@app.get("/developer_reviews_analysis")
def developer_reviews_analysis(desarrollador : str):
# trabajamos con nuestras columnas de interés y formamos una nueva tabla
    games = games[["item_id", "developer"]]
    reviews = reviews[["item_id", "analisis_sentimiento"]]
    merge = pd.merge(games, reviews, on="item_id", how="inner")
#filtramos de acuerdo al parámetro
    filtro = merge[merge["developer"] == desarrollador]
# contamos cada valor del analisis_sentimiento
    conteo_sentimientos = filtro['analisis_sentimiento'].value_counts()
# creamos una lista
    lista_resultado = [f'Negative = {conteo_sentimientos.get(0, 0)}', f'Positive = {conteo_sentimientos.get(2, 0)}']
# convertimos a dict
    out = {desarrollador: lista_resultado}

    return out
