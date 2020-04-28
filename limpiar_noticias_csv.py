import pandas
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

sia = SIA()

# iteramos sobre NOTICIAS CSV
for file in os.listdir("D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\NOTICIAS CSV"):
    df = pandas.read_csv("D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\NOTICIAS CSV\\" + file, delimiter=";")
    ticker = df["Ticker"].iloc[0]
    # comprobamos que no estén ya los datos, de lo contrario cosas malas podrían ocurrir sobre el archivo
    aux = ticker + ".csv"
    if aux in os.listdir("D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\NOTICIAS CSV - LIMPIAS"):
        continue
    df["Date_Time"] = df["Date_Time"].str[:10]
    df["Score"] = 0
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
        score = sia.polarity_scores(text=articulo)["compound"]
        df.loc[index, "Score"] = score
    df[["Date_Time", "Score"]].copy()\
        .to_csv("D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\NOTICIAS CSV - LIMPIAS\\" + ticker + ".csv")
