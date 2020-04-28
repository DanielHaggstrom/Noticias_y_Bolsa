# este script adquirirá las noticias para el proyecto
import requests
import json

r = requests.get("http://api.nytimes.com/svc/search/v2/articlesearch.json?q=Apple&begin_date=20100101&end_date=20151231&api-key=bZvV29QOmyUw74K0Las0bzo08O6Zihhp")
data = r.json()

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
