import requests
import lxml.html as lh
import pandas as pd

url = 'https://www.slickcharts.com/sp500'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
tr_elements = doc.xpath('//tr')

# Create empty list
col = []
i = 0
# For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i += 1
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

cont = 0
for t in tickers:
    url = 'https://finance.yahoo.com/quote/' + t + '/history?period1=1429401600&period2=1587254400&interval=1wk&filter=history&frequency=1wk'
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    tr_elements = doc.xpath('//tr')
    #Create empty list
    col = []
    i = 0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        col.append((name, []))
    erase = []
    for j in range(1,len(tr_elements)):
        T = tr_elements[j]
        if len(T) <= 2:
            erase.append(j)
    tr_elements = [i for j, i in enumerate(tr_elements) if j not in erase]
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
    path = 'D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\prototipo 2\\' + tickers[cont] + '.csv'
    df.to_csv(path, index=False)
    cont = cont + 1
