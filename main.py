from fastapi import FastAPI
import os
import pandas as pd


app = FastAPI()

##### 1
# Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.
@app.get("/developer")
def developer(desarrollador : str):
# importamos la tabla de la función
    developer = pd.read_csv("data_api/developer.csv")
# filtramos por developer
    developer = developer[developer["developer"] == desarrollador]
# agrupamos por año, contamos los items y calculamos el porcentaje free
    agrupado = developer.groupby('year_release').agg({
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


##### 2
# Cantidad de dinero gastado por el usuario, el porcentaje de recomendación y cantidad de items.
@app.get("/userdata")
def userdata(user_id : str):
# importamos la tabla de la función
    userdata = pd.read_csv("data_api/userdata.csv")
#filtramos por usuario
    userdata = userdata[userdata["user_id"] == user_id]
# nos quedamos con las columnas de interés
    seleccion = userdata[["user_id", "item_id", "recommend", "price"]]  
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
    diccionario_resultado = userdata.to_dict(orient='records')

    return diccionario_resultado



##### 3
# Usuario que acumula más horas jugadas para el género dado y lista de la acumulación de horas jugadas por año de lanzamiento.
@app.get("/user_for_genre")
def user_for_genre(genero : str):
# importamos la primera tabla
    u1 = pd.read_csv("data_api/user_for_genre1.csv")
# filtramos por género
    u1 = u1["user_id"][u1["game_genre"] == genero]
    u1 = u1.values[0]
# importamos la segunda tabla
    u2 = pd.read_csv("data_api/user_for_genre2.csv")
# nos quedamos con las columnas de interés según género
    u2 = u2[["year_release", "playtime_forever"]][u2["game_genre"] == genero]
# ordenamos según año
    horas_jugadas = u2.sort_values(by='year_release', ascending=False)
# cambiamos el nombre de las columnas
    horas_jugadas.columns = ["Año", "Horas"]
# convertimos el df en lista
    lista_resultado = horas_jugadas.to_dict(orient='records')
# formateamos la salida
    out = {f"Usuario con más horas jugadas para Género {genero}" : u1, "Horas jugadas": lista_resultado}

    return out


##### 4
# Top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
@app.get("/best_developer_year")
def best_developer_year(año : int):
# importamos la tabla a usar
    bdy = pd.read_csv("data_api/best_developer_year.csv")
# nos quedamos con las columnas de utilidad
    bdy = bdy[["Año", "Desarrollador"]]
# filtramos desarrolladores top por año
    filtro = bdy["Desarrollador"][bdy["Año"] == año]
# convertimos cada valor en una variable independiente
    X = filtro.iloc[0]
    Y = filtro.iloc[1]
    Z = filtro.iloc[2]
# formateamos la salida
    lista_resultado = [{"Puesto 1" : f"{X}"}, {"Puesto 2" : f"{Y}"},{"Puesto 3" : f"{Z}"}]

    return lista_resultado


##### 5
# diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registro
# de reseñas como valor positivo o negativo.
@app.get("/developer_reviews_analysis")
def developer_reviews_analysis(desarrollador : str):
# importamos la tabla a usar
    dra = pd.read_csv("data_api/developer_reviews_analysis.csv")
# nos quedamos con las columnas de utilidad
    dra = dra[["developer", "Negative", "Positive"]]
#filtramos de acuerdo al parámetro
    filtro = dra[["Negative", "Positive"]][dra["developer"] == desarrollador]
# creamos las variables para el formateo del return
    neg = filtro["Negative"].iloc[0]
    pos = filtro["Positive"].iloc[0]
# creamos el diccionario de salida
    out = {f'{desarrollador}' : [f"Negative = {neg}", f"Positive = {pos}"]}

    return out