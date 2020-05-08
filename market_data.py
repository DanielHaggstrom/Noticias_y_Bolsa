from urllib.error import HTTPError
import requests
import lxml.html as lh
import pandas as pd
import wget
import os
import datetime
import time

url = 'https://www.slickcharts.com/sp500'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')

# Create empty list
col = []
# For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    name = t.text_content()
    col.append((name, []))

for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]
    # If row is not of size 10, the //tr data is not from our table
    if len(T) != 7:
        break
    # i is the index of our column
    i = 0
    # Iterate through each element of the row
    for t in T.iterchildren():
        data = t.text_content()
        # Check if row is empty
        if i > 0:
            # Convert any numerical value to integers
            try:
                data = int(data)
            except:
                pass
        # Append the data to the empty list of the i'th column
        col[i][1].append(data)
        # Increment i for the next column
        i += 1

Dict = {title: column for (title, column) in col}
df = pd.DataFrame(Dict)

names = df.Symbol.unique()
namesList = list(names)
tickers = namesList

# todo comprobar que la lista de símbolos ticker del S&P 500 sea correcta

for t in tickers:
    time.sleep(1)  # no queremos sobrecargar sus servidores
    t = t.replace(".", "-")
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + t + \
          "?period1=1325376000&period2=1588204800&interval=1wk&events=history"
    if os.path.exists(os.path.join(os.path.dirname(__file__), "datos", "bolsa", t + ".csv")):  # eliminamos si ya existe
        os.remove(os.path.join(os.path.dirname(__file__), "datos", "bolsa", t + ".csv"))
    try:
        wget.download(url, out=os.path.join(os.path.dirname(__file__), "datos", "bolsa"))
        # hemos descargado los datos, pero hay que comprobar que sean correctos (si la empresa existía en 2012-01-01)
        dataframe = pd.read_csv(os.path.join(os.path.dirname(__file__), "datos", "bolsa", t + ".csv"), index_col="Date")
        date = dataframe.index[0]
        if date == "2012-01-01":
            continue  # es correcto, y no hace falta seguir
        # eliminamos el archivo, pues o es incorrecto, o la empresa no nos interesa
        os.remove(os.path.join(os.path.dirname(__file__), "datos", "bolsa", t + ".csv"))
        # todo una vez que tengamos un modelo funcional, probar con diferentes fechas cutoff
        if date > "2014-01-01":  # demasiados pocos datos, excluimos la empresa del análisis
            print("Eliminada: " + t)
            continue
        day_of_week = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()
        days_to_next_sunday = 6 - day_of_week
        next_sunday = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=days_to_next_sunday)
        input(next_sunday)
        period1 = int(next_sunday.timestamp())
        # volvemos a intentar el archivo, esta vez con la fecha modificada
        url = "https://query1.finance.yahoo.com/v7/finance/download/" + t + \
              "?period1=" + str(period1) + "&period2=1588204800&interval=1wk&events=history"
        wget.download(url, out=os.path.join(os.path.dirname(__file__), "datos", "bolsa"))

    except HTTPError:
        print("No se pudo descargar " + t)
