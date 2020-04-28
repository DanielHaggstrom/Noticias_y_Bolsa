# este script adquirirá las noticias para el proyecto, versión de clasificación
import requests
import json
import time
from calendar import monthrange
from os import path
import math
from ExtraccionTexto import extraccionDatos
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

api_key = "SkjFNCl2LcXgGPAne1K8AoDuRPe01MS7"
sia = SIA()


def merge(list1, list2):
    # Esta función junta dos listas en una lista de tuplas
    merged_list = []
    for i in range(max((len(list1), len(list2)))):
        while True:
            try:
                tup = (list1[i], list2[i])
            except IndexError:
                if len(list1) > len(list2):
                    list2.append('')
                    tup = (list1[i], list2[i])
                elif len(list1) < len(list2):
                    list1.append('')
                    tup = (list1[i], list2[i])
                continue
            merged_list.append(tup)
            break
    return merged_list


for year in range(2010, 2016):
    # iteramos año a año
    year_s = str(year)  # conviene tener el año en string
    print("=====")
    print("Year " + year_s)
    for month in range(1, 13):
        # mes a mes
        month_s = str(month)  # conviene tener el mes en string
        date_url = []
        # añadimos un 0 delante si hace falta
        if len(month_s) == 1:
            month_s = "0" + month_s
        # nos saltamos este mes de este año si los datos ya han sido recogidos
        if path.exists("class - year " + year_s + " month " + month_s + ".txt"):
            continue
        print("    month " + month_s)
        # obtenemos el día fianl de este mes, en este año, y añadimos un 0 si hace falta
        day_s = str(monthrange(year, month)[1])
        if len(day_s) == 1:
            day_s = "0" + day_s
        page = 0
        page_max = 100000
        status = True
        # obtenemos el número de resultados, para saber cuantas páginas hay que buscar
        url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=body=('Apple')&begin_date=" + year_s + month_s + "01&end_date=" + year_s + month_s +\
              day_s + "&sort=oldest&page=&api-key=" + api_key
        time.sleep(6)
        response = requests.get(url)
        if response.status_code == 200:
            hits = float(json.loads(response.text)["response"]["meta"]["hits"])
            page_max = math.ceil(hits/10) - 1
            print("        hits " + str(hits))
            print("        pages " + str(page_max))
        else:
            print("Something fucky is happening")
            print(response.status_code)
            continue
        # iteramos sobre todas las páginas
        while page <= page_max and status:
            url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=body=('Apple')&begin_date=" + year_s\
                  + month_s + "01&end_date=" + year_s + month_s + day_s + "&sort=oldest&page=" + str(page) +\
                  "&api-key=" + api_key
            response = requests.get(url)
            if response.status_code == 200:
                # obtenemos las urls, y las fechas, y las juntamos
                data = json.loads(response.text)["response"]
                news = data["docs"]
                urls = [x['web_url'] for x in news]
                dates = [x['pub_date'][:-14] for x in news]
                date_url.extend(merge(dates, urls))
                final_list = []
                for (date, link) in date_url:
                    # nos quedamos sólo con las noticias del NYT
                    # TODO ver si podemos incluir blogs u otros formatos
                    # TODO considerar fechas repetidas
                    if len(link) < 24 or link[:24] != "https://www.nytimes.com/":
                        continue
                    # obtenemos una lista de tuplas (fecha, puntuación)
                    text = extraccionDatos(link)
                    score = sia.polarity_scores(text=text)["compound"]
                    label = "0"
                    if score > 0:
                        label = "1"
                    if score < 0:
                        label = "-1"
                    final_list.append((date, label))
                print("        cumulative " + str(len(date_url)))
                page += 1
                time.sleep(6)
            else:
                print(str(response.status_code) + " <----")
                status = False
        # cuando tenemos todos los datos del mes, los escribimos en un archivo
        f = open("D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\class - year " + year_s + " month " + month_s + ".txt", "w")
        for date_score in final_list:
            f.write(str(date_score[0]) + " " + str(date_score[1]) + "\n")
