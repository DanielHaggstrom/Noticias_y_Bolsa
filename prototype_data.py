# este script unificará los datos de las acciones de Apple y los puntajes de las noticias
import pandas
from datetime import datetime

# adquirimos el dataframe
data = pandas.read_csv("D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\apple-data.csv")
# añadimos una columna para la puntuación, con valor default 0
data["Score"] = 0.0

for year in range(2010, 2016):
    # iteramos año a año
    year_s = str(year)  # conviene tener el año en string
    for month in range(1, 13):
        # mes a mes
        month_s = str(month)  # conviene tener el mes en string
        # añadimos un 0 delante si hace falta
        if len(month_s) == 1:
            month_s = "0" + month_s
        # leemos el archivo
        f = open("D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\year " + year_s + " month " + month_s + ".txt", "r")
        lines = f.readlines()
        for aux_line in lines:
            line = aux_line.strip().split()
            date = line[0]
            score = float(line[1])
            data.loc[data["Date"] == date, "Score"] = score

# guardamos el resultado
data.to_csv(r'D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\prototype_data.csv')
