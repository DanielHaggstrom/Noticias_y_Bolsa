# NO METER A GITHUB
import config
import os
import pandas
import datetime

df = pandas.read_csv(os.path.join(config.path_datos_aprendizaje, "dataset.csv"), index_col="Date")
def check_two_dates(date1, date2):
    # devuelve true si date2 está a exactamente 7 días de date1
    max_date = date1 + datetime.timedelta(days=7)
    return max_date == date2

aux = df.index[0]
for index, row in df.iterrows():
    if index == aux:
        continue
    if not check_two_dates(datetime.datetime.strptime(aux, "%Y-%m-%d"), datetime.datetime.strptime(index, "%Y-%m-%d")):
        print("Error en " + index + " y " + aux)
    aux = index
