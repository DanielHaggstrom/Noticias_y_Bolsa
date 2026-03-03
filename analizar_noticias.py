"""Generate sentiment score CSVs from the archived article dataset."""

import os

import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

import config


def build_sentiment_analyzer():
    try:
        return SIA()
    except LookupError:
        nltk.download("vader_lexicon")
        return SIA()


def main():
    sia = build_sentiment_analyzer()

    for file_name in os.listdir(config.path_datos_noticias):
        if not file_name.endswith(".csv"):
            continue

        dataframe = pd.read_csv(os.path.join(config.path_datos_noticias, file_name), delimiter=";")
        dataframe = dataframe.loc[:, ~dataframe.columns.str.startswith("Unnamed:")]
        if dataframe.empty:
            continue

        ticker = dataframe["Ticker"].iloc[0]
        dataframe["Date_Time"] = dataframe["Date_Time"].astype(str).str[:10]
        dataframe["Score"] = 0.0

        for index, row in dataframe.iterrows():
            titular = row["Titular"] if isinstance(row["Titular"], str) else ""
            subtitular = row["Subtitular"] if isinstance(row["Subtitular"], str) else ""
            texto = row["Texto"] if isinstance(row["Texto"], str) else ""
            articulo = " ".join((titular, subtitular, texto)).strip()
            dataframe.loc[index, "Score"] = sia.polarity_scores(text=articulo)["compound"]

        output_path = os.path.join(config.path_datos_noticias_score, f"{ticker}.csv")
        dataframe[["Date_Time", "Score"]].copy().to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
