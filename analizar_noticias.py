# nuestro objetivo es guardar copias de los datos de noticias, pero que contengan el score del análisis del sentimeinto
# en vez del contenido de la noticia
import pandas
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

sia = SIA()

# creamos la ruta a "noticias" de forma independiente de la ubicación del repo, y del sistema operativo
news_path = os.path.join(os.path.dirname(__file__), "datos", "noticias")
# también hacemos lo mismo para la ruta donde guardaremos los datos completos
score_path = os.path.join(os.path.dirname(__file__), "datos", "noticias - score")

# iteramos sobre la carpeta "noticias", donde se encuentran los dataframes csv que contienen las fechas y artículos
# cada archivo es una empresa
for file in os.listdir(news_path):
    df = pandas.read_csv(os.path.join(news_path, file), delimiter=";")
    ticker = df["Ticker"].iloc[0]
    df["Date_Time"] = df["Date_Time"].str[:10] # eliminamos la hora, dejando sólo la fecha
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
    df[["Date_Time", "Score"]].copy().to_csv(os.path.join(news_path, ticker + ".csv"))
