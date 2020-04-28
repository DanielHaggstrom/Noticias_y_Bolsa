# Este script adquiere y prepara los datos del mercado de valores. De momento sólo carga los datos necesarios para
# el prototipo.

import pandas
import sys
from datetime import datetime

# Importante cambiar según la estructura de directorios de cada uno.
proyect_path = "D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\"
etf_path = proyect_path + "datos\\etfs"
stock_path = proyect_path + "datos\\stocks"

# El prototipo no requiere los fondos de inversión.
"""
ets1 = pandas.read_csv(etf_path+ "\\etss1.csv")
ets2 = pandas.read_csv(etf_path+ "\\etss2.csv")
ets3 = pandas.read_csv(etf_path+ "\\etss3.csv")
"""

stock1 = pandas.read_csv(stock_path + "\\stock1.csv")
# El prototipo sólo requiere datos de Apple, que se encuentran en el archivo de arriba.
"""
stock2 = pandas.read_csv(stock_path + "\\stock2.csv")
stock3 = pandas.read_csv(stock_path + "\\stock3.csv")
stock4 = pandas.read_csv(stock_path + "\\stock4.csv")
stock5 = pandas.read_csv(stock_path + "\\stock5.csv")
stock6 = pandas.read_csv(stock_path + "\\stock6.csv")
stock7 = pandas.read_csv(stock_path + "\\stock7.csv")
stock8 = pandas.read_csv(stock_path + "\\stock8.csv")
stock9 = pandas.read_csv(stock_path + "\\stock9.csv")
stock10 = pandas.read_csv(stock_path + "\\stock10.csv")
stock11 = pandas.read_csv(stock_path + "\\stock11.csv")
stock12 = pandas.read_csv(stock_path + "\\stock12.csv")
stock13 = pandas.read_csv(stock_path + "\\stock13.csv")
stock14 = pandas.read_csv(stock_path + "\\stock14.csv")
stock15 = pandas.read_csv(stock_path + "\\stock15.csv")
stock16 = pandas.read_csv(stock_path + "\\stock16.csv")
stock17 = pandas.read_csv(stock_path + "\\stock17.csv")
stock18 = pandas.read_csv(stock_path + "\\stock18.csv")

# Aquí se concatenan los datos en dos dataframes de pandas.
frames_etf = [ets1,ets2,ets3]
ets = pandas.concat(frames_etf)

frames_stock = [stock1, stock2, stock3, stock4, stock5, stock6, stock7, stock8, stock9, stock10, stock11, stock12,
             stock13, stock14, stock15, stock16, stock17, stock18]
stocks = pandas.concat(frames_stock)
"""

# Limpiamos un poco los nombres de las comañías.
stock1['Source.Name'] = stock1['Source.Name'].str.replace(r'.us.txt', '')

def extract_company(company, start, end, fuente):
    # Esta función extrae y prepara los datos de una empresa específica, entre dos fechas concretas (años),
    # desde un dataframe específico.
    data_raw = fuente[stock1['Source.Name'] == company]
    # Trabajaremos con el crecimiento relativo de cada día.
    data_raw["Growth"] = (data_raw["Close"] - data_raw["Open"]) / data_raw["Open"]
    data = data_raw[["Date", "Growth"]]
    data_final = pandas.DataFrame(columns=['Date', 'Growth'])
    for index, row in data.iterrows():
        # Extraemos los datos entre los años especificados, y transformamos la fecha de formato m/d/y a y/m/d.
        if int(row["Date"][-4:]) >= start and int(row["Date"][-4:]) < end:
            data_final = data_final.append(
                pandas.DataFrame(data= {"Date": [datetime.strptime(row["Date"], "%m/%d/%Y").date()], "Growth": [row["Growth"]]}))
    # Transformamos la fecha de string a DateTime, y la establecemos como el índice.
    data_final['Date'] = pandas.to_datetime(data_final['Date'], format='%Y-%m-%d')
    data_final = data_final.set_index('Date')
    # Obtenemos las fechas faltantes.
    missing_pandas = pandas.date_range(start='2010-01-01', end='2015-12-31').difference(data_final.index).tolist()
    missing = [pandas.to_datetime(element).strftime("%Y-%m-%d") for element in missing_pandas]
    # de momento vamos a imputar un crecimiento de 0 en los días que no tenemos datos.
    # TODO: Buscar otra forma de imputación.
    df_missing = pandas.DataFrame(data= {"Date": [item for  item in missing], "Growth":[0 for element in missing]})
    df_missing["Date"] = pandas.to_datetime(df_missing["Date"], format='%Y-%m-%d')
    df_missing.set_index("Date", inplace=True)
    data_final = data_final.append(df_missing).sort_index()
    return data_final

# Extraemos los datos necesarios para el prototipo, y los guardamos en un archivo.
aapl_final = extract_company("aapl", 2010, 2015, stock1)
print(aapl_final)
aapl_final.to_csv(r'D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\apple-data.csv')
