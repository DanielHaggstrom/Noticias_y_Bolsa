# nuestro objetivo es guardar copias de los datos de noticias, pero que contengan el score del análisis del sentimiento
# en vez del contenido de la noticia
import config
import os
import pandas
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

sia = SIA()

# iteramos sobre la carpeta "noticias", donde se encuentran los dataframes csv que contienen las fechas y artículos
# cada archivo es una empresa
for file in os.listdir(config.path_datos_noticias):
    df = pandas.read_csv(os.path.join(config.path_datos_noticias, file), delimiter=";")
    ticker = df["Ticker"].iloc[0]
    df["Date_Time"] = df["Date_Time"].str[:10]  # eliminamos la hora, dejando sólo la fecha
    df["Score"] = 0
    # iteramos sobre las filas
    for index, row in df.iterrows():
        titular = row["Titular"]
        subtitular = row["Subtitular"]
        texto = row["Texto"]
        if not isinstance(titular, str):
            titular = ""
        if not isinstance(subtitular, str):
            subtitular = ""
        if not isinstance(texto, str):
            texto = ""
        articulo = titular + " " + subtitular + " " + texto
        # obtenemos el puntaje del análisis de sentimiento
        score = sia.polarity_scores(text=articulo)["compound"]
        df.loc[index, "Score"] = score
    # guardamos el resultado
    df[["Date_Time", "Score"]].copy().to_csv(os.path.join(config.path_datos_noticias_score, ticker + ".csv"))
