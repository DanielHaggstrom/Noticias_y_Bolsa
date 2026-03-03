from urllib.error import HTTPError
import os
import time

import lxml.html as lh
import pandas as pd
import requests
import wget

import config


def main():
    url = "https://www.slickcharts.com/sp500"
    page = requests.get(url, timeout=30)
    page.raise_for_status()

    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath("//tr")

    columns = []
    for header in tr_elements[0]:
        columns.append((header.text_content(), []))

    for row in tr_elements[1:]:
        if len(row) != 7:
            break
        for index, element in enumerate(row.iterchildren()):
            data = element.text_content()
            if index > 0:
                try:
                    data = int(data)
                except ValueError:
                    pass
            columns[index][1].append(data)

    dataframe = pd.DataFrame({title: column for (title, column) in columns})
    tickers = [ticker.replace(".", "-") for ticker in dataframe.Symbol.unique()]

    for ticker in tickers:
        time.sleep(1)
        download_url = (
            "https://query1.finance.yahoo.com/v7/finance/download/"
            f"{ticker}?period1=1325376000&period2=1588204800&interval=1wk&events=history"
        )
        output_path = os.path.join(config.path_datos_bolsa, f"{ticker}.csv")

        if os.path.exists(output_path):
            os.remove(output_path)

        try:
            wget.download(download_url, out=config.path_datos_bolsa)
            downloaded_dataframe = pd.read_csv(output_path, index_col="Date")
            if downloaded_dataframe.index[0] != "2012-01-01":
                print(ticker)
                os.remove(output_path)
        except HTTPError:
            print("No se pudo descargar " + ticker)

    print("Terminado.")


if __name__ == "__main__":
    main()
