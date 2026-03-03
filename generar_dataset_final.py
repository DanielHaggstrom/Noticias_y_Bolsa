"""Join weekly market data and news sentiment into a learning dataset."""

import datetime
import numbers
import os
from statistics import mean, stdev

import pandas as pd
from numpy import nan

import config


def parse_numeric(value):
    if isinstance(value, str):
        cleaned = value.replace(",", "").strip()
        if not cleaned:
            return None
        try:
            return float(cleaned)
        except ValueError:
            return None
    if isinstance(value, numbers.Real):
        return float(value)
    return None


def get_growth(open_price, close_price):
    open_value = parse_numeric(open_price)
    close_value = parse_numeric(close_price)
    if open_value is None or close_value is None or open_value == 0:
        return None
    return (close_value - open_value) / open_value


def generate_date_list(date1):
    transformed_date = datetime.datetime.strptime(date1, "%Y-%m-%d")
    time_delta = datetime.timedelta(days=1)
    aux = [transformed_date]
    for _ in range(1, 7):
        aux.append(aux[-1] + time_delta)
    return [date.strftime("%Y-%m-%d") for date in aux]


def build_company_frame(file_name):
    if file_name not in os.listdir(config.path_datos_noticias_score):
        return None

    ticker = file_name[:-4]
    news_data = pd.read_csv(os.path.join(config.path_datos_noticias_score, file_name))
    news_data = news_data.loc[:, ~news_data.columns.str.startswith("Unnamed:")]
    if len(news_data) < 400:
        return None

    raw_data = pd.read_csv(os.path.join(config.path_datos_bolsa, file_name))
    raw_data.set_index("Date", inplace=True)
    raw_data.drop(["High", "Low", "Adj Close", "Volume"], axis=1, inplace=True, errors="ignore")
    raw_data.sort_index(inplace=True)

    rows = []
    for index, row in raw_data.iterrows():
        date_list = generate_date_list(index)
        score_list = list(news_data.loc[news_data["Date_Time"].isin(date_list)]["Score"])
        score_num = len(score_list)
        std = nan

        if score_list:
            score = mean(score_list)
            if len(score_list) > 1:
                std = stdev(score_list)
        else:
            score = nan

        rows.append(
            {
                "Date": index,
                f"{ticker}-growth": get_growth(row["Open"], row["Close"]),
                f"{ticker}-score": score,
                f"{ticker}-num": score_num,
                f"{ticker}-std": std,
            }
        )

    dataframe = pd.DataFrame.from_records(rows)
    dataframe.set_index("Date", inplace=True)
    return dataframe


def main():
    dataset_final = pd.DataFrame()

    for file_name in os.listdir(config.path_datos_bolsa):
        if not file_name.endswith(".csv"):
            continue

        company_frame = build_company_frame(file_name)
        if company_frame is None:
            continue

        print(file_name[:-4])
        dataset_final = pd.concat((dataset_final, company_frame), axis=1)

    dataset_final = dataset_final.ffill()
    dataset_final.dropna(inplace=True)
    dataset_final.to_csv(
        os.path.join(config.path_datos_aprendizaje, "dataset.csv"),
        index=True,
        index_label="Date",
    )
    print("Terminado.")


if __name__ == "__main__":
    main()
