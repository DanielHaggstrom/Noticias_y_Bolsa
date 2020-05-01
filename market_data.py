from urllib.error import HTTPError
import requests
import lxml.html as lh
import pandas as pd
import wget
import os

url = 'https://www.slickcharts.com/sp500'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
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
    t = t.replace(".", "-")
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + t + \
          "?period1=1325376000&period2=1588204800&interval=1wk&events=history"
    try:
        wget.download(url, out=os.path.join(os.path.dirname(__file__), "datos", "bolsa"))
    except HTTPError:
        print("No se pudo descargar " + t)
