# este script busca crear un archivo json que asocia a cada símbolo ticker la empresa correspondiente
import config
import json
import os
import pandas

# guardamos la ruta para obtener los datos (y luego guardar el resultado)
# este método es independiente de la ubicación del repositorio y del sistema operativo
path = config.path_datos
nyse = pandas.read_csv(os.path.join(path, "NASDAQ.txt"), sep="\t")
nasdaq = pandas.read_csv(os.path.join(path, "NYSE.txt"), sep="\t")

# añadimos los datos a un diccionario, evitando valores repetidos
nyseSymbol = list(nyse["Symbol"])
nyseDescription = list(nyse["Description"])
nasdaqSymbol = list(nasdaq["Symbol"])
nasdaqDescription = list(nasdaq["Description"])

translation_dict = {}

for i in range(0,len(nyseDescription)):
    if nyseDescription[i] not in nasdaqDescription:
        translation_dict.setdefault(nyseSymbol[i], nyseDescription[i])

translation_dictDescription = list(translation_dict.values())

for i in range(0, len(nasdaqDescription)):
    if nasdaqDescription[i] not in translation_dictDescription:
        translation_dict.setdefault(nasdaqSymbol[i], nasdaqDescription[i])

# guardamos el diccionario como json
with open(os.path.join(path, "tickers.json"), "w") as fp:
    json.dump(translation_dict, fp)
