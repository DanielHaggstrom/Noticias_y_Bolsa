# este script busca devolver el nombre de una empresa dado el símbolo ticker.
import pandas
import json

nyse = pandas.read_csv("D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\NASDAQ.txt", sep="\t")
nasdaq = pandas.read_csv("D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\NYSE.txt", sep="\t")

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

with open("D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\tickers.json", "w") as fp:
    json.dump(translation_dict, fp)
