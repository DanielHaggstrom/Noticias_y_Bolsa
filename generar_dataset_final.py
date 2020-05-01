# este script unificará los datos de varias empresas para el prototipo 2
# debe producir un archivo csv con columnas para empresa, con crecimeintos y puntuaciones de noticias
import config
import os
import datetime
from statistics import mean
import pandas
from numpy import nan

# AHORA MISMO ESTÁ EN MODO DE REGRESIÓN

# definimos función para calcular el crecimiento
def get_growth(open_price, close_price):
    # en algunos casos, los datos vienen como string, o aparece algún símbolo para indicar que faltan
    if isinstance(open_price, str):
        try:
            open_price = float(open_price.replace(',', ''))
        except ValueError:
            return None
    if isinstance(close_price, str):
        try:
            close_price = float(close_price.replace(',', ''))
        except ValueError:
            return None
    if not (isinstance(open_price, float) or isinstance(close_price, float)):
        raise TypeError("Incorrect data type: " + type(open_price) + ", " + type(close_price))
    return (close_price - open_price) / open_price


def generate_date_list(date1):
    # dada una date1, produce una lista de las fechas de los siguientes 6 días
    transformed_date = datetime.datetime.strptime(date1, "%Y-%m-%d")
    time_delta = datetime.timedelta(days=1)
    aux = [transformed_date]
    for i in range(1, 7):
        next_day = aux[-1] + time_delta
        aux.append(next_day)
    return [date.strftime("%Y-%m-%d") for date in aux]

# creamos las rutas adecuadas para obtener datos y guardarlos
# guardaremos todos los datos en un dataframe
dataset_final = pandas.DataFrame()

for file in os.listdir(config.path_datos_bolsa):
    # primero buscamos entre los datos de noticias, para comprobar que podemos seguir
    if file not in os.listdir(config.path_datos_noticias_score):
        continue
    ticker = file[:-4]
    # adquirimos el dataframe con scores de noticias, y lo ajustamos a nuestras necesidades
    news_data = pandas.read_csv(os.path.join(config.path_datos_noticias,file))
    news_data.drop(["Unnamed: 0"], axis=1, inplace=True)
    raw_data = pandas.read_csv(os.path.join(config.path_datos_bolsa, file))
    # limpiamos un poco
    raw_data.set_index("Date", inplace=True)
    raw_data.drop(["High", "Low", "Adj Close", "Volume"], axis=1, inplace=True)
    raw_data.sort_index(inplace=True)
    # creamos un dataframe vacío, donde guardaremos los datos de la empresa particular
    df = pandas.DataFrame(columns=["Date"])
    # iteramos sobre las filas del dataframe raw_data
    for index, row in raw_data.iterrows():
        # buscamos las filas del dataframe de scores que se encuentren en la semana correspondiente a esta fila
        # todo asegurarse que no hay problemas con tickers con guiones
        date_list = generate_date_list(index)
        score_list = list(news_data.loc[news_data["Date_Time"].isin(date_list)]["Score"])
        if len(score_list) == 0:
            score = nan
        else:
            score = mean(score_list)
            """
            if score > 0:
                score = 1
            else:
                score = -1
            """
        # adquirimos los datos
        growth = get_growth(row["Open"], row["Close"])
        """
        if growth > 0:
            growth = 1
        else:
            growth = -1
        """
        df = df.append({"Date": index, ticker + "-growth": growth, ticker + "-score": score},
                       ignore_index=True)
    # guardamos los datos en el dataset final
    df.set_index("Date", inplace=True)
    dataset_final = pandas.concat((dataset_final, df), axis=1)

# existen nulls, imputaremos con la media
dataset_final.fillna(dataset_final.mean(), inplace=True)
dataset_final.sort_index(inplace=True)

# finalmente, guardamos el dataframes a csv
dataset_final.to_csv(os.path.join(config.path_datos_aprendizaje, "dataset.csv"), index=True, index_label="Date")
print("Terminado")
