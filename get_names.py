"""Build a ticker-to-company-name lookup from the archived exchange exports."""

import json
import os

import pandas as pd

import config


def main():
    path = config.path_datos
    nasdaq = pd.read_csv(os.path.join(path, "NASDAQ.txt"))
    nyse = pd.read_csv(os.path.join(path, "NYSE.txt"))

    translation_dict = {}

    for symbol, description in zip(nasdaq["Symbol"], nasdaq["Description"]):
        translation_dict.setdefault(symbol, description)

    existing_descriptions = set(translation_dict.values())
    for symbol, description in zip(nyse["Symbol"], nyse["Description"]):
        if description not in existing_descriptions:
            translation_dict.setdefault(symbol, description)

    with open(os.path.join(path, "tickers.json"), "w", encoding="utf-8") as file_obj:
        json.dump(translation_dict, file_obj, ensure_ascii=False, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
