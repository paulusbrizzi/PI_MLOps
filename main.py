from fastapi import FastAPI
import os
import pandas as pd


app = FastAPI()

# 1
@app.get("/developer")
def developer(desarrollador : str):
    """
    Función developer(desarrollador)

    Parámetro
    ---------
    Recibe nombre de empresa desarrolladora como String
    
    Devuelve por año, cantidad de ítems (juegos) y porcentaje de contenido gratuito.
    """
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
    out = agrupado.to_dict(orient='records')

    return out


# 2
@app.get("/userdata")
def userdata(user_id : str):
    """
    Función userdata(user_id)

    Parámetro
    ---------
    Recibe id del usuario como String
    
    Devuelve total del dinero gastado, porcentaje de recomendación positivo y cantidad de ítems adquiridos.
    """
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
    out = userdata.to_dict(orient='records')

    return out



# 3
@app.get("/user_for_genre")
def user_for_genre(genero : str):
    """
    Función user_for_genre(genero)

    Parámetro
    ---------
    Recibe el género como String
    
    Devuelve el usuario con más horas jugadas en el género dado, y una lista acumulación de horas jugadas por años de lanzamiento.
    """
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


#4
@app.get("/best_developer_year")
def best_developer_year(año : int):
    """
    Función best_developer_year(año)

    Parámetro
    ---------
    Recibe el año como Int
    
    Devuelve las 3 empresas desarrolladoras con juegos más recomendados por los usuarios según el año dado.
    """
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
    out = [{"Puesto 1" : f"{X}"}, {"Puesto 2" : f"{Y}"},{"Puesto 3" : f"{Z}"}]

    return out


# 5
@app.get("/developer_reviews_analysis")
def developer_reviews_analysis(desarrollador : str):
    """
    Función developer_reviews_analysis(desarrollador)

    Parámetro
    ---------
    Recibe el nombre de la empresa desarrolladora como String.
    
    Devuelve el nombre del desarrollador como llave, y una lista con la cantidad de reseñas negativas y positivas totales.
    """
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


# 6
@app.get("/recomendacion_juego")
def recomendacion_juego(id_de_producto : int):
    rec = pd.read_csv("data_api/recomendaciones.csv")
    rec = rec["recomendaciones"][rec["item_id"] == id_de_producto].iloc[0]
    rec = eval(rec)
    out = {f"ID del Juego: {id_de_producto}": rec}
    
    return out
