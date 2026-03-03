"""Legacy Financial Times scraping workflow kept for archival reference."""

import json
import os
import pickle
import time

import pandas as pd
from selenium import webdriver

import config


DICT_PATH = os.path.join(config.path_datos, "tickers.json")
URL_PICKLE_PATH = os.path.join(config.path_datos, "listaUrls.pkl")
NOTICIAS_PATH = config.path_datos_noticias
FT_URL = "https://www.ft.com/"

with open(DICT_PATH, encoding="utf-8") as dict_file:
    COMPANY_MAPPING = json.load(dict_file)

COMPANY_NAMES = list(COMPANY_MAPPING.values())
DRIVER = None


def require_credentials():
    username = os.environ.get("FT_EMAIL")
    password = os.environ.get("FT_PASSWORD")
    if not username or not password:
        raise RuntimeError("Set FT_EMAIL and FT_PASSWORD before running FT.py.")
    return username, password


def login(driver, username, password):
    driver.get(FT_URL)
    continua = False
    buscador_sign_in = driver.find_elements_by_class_name("o-header__nav-item")
    while not continua:
        for item in buscador_sign_in:
            sign_in = item.find_element_by_tag_name("a").get_attribute("data-trackable")
            if sign_in == "Sign In":
                item.click()
                continua = True
                break

    time.sleep(0.5)
    introductor_email = driver.find_element_by_id("enter-email")
    introductor_email.send_keys(username)

    enter_email = driver.find_element_by_id("enter-email-next")
    enter_email.click()
    time.sleep(0.5)

    introductor_password = driver.find_element_by_id("enter-password")
    introductor_password.send_keys(password)

    enter_password = driver.find_element_by_tag_name("button")
    enter_password.click()

    input("Complete any FT anti-bot challenge in the browser, then press Enter here...")


def extraer_urls(empresas):
    dic_empresas = {}
    numero_noticias = 10000
    siguiente = False

    with open(URL_PICKLE_PATH, "wb") as file_obj:
        for empresa in empresas:
            lista_urls = []
            if not siguiente:
                posibilidades_buscador = DRIVER.find_elements_by_tag_name("a")
                for elemento in posibilidades_buscador:
                    detector_buscador = elemento.get_attribute("data-trackable")
                    if detector_buscador == "search-toggle":
                        elemento.click()
                        break

                introductor_empresa = DRIVER.find_element_by_class_name("o-header__search-term")
                introductor_empresa.send_keys(empresa[:-1])
            else:
                introductor_empresa.clear()
                introductor_empresa.send_keys(empresa[:-1])

            siguiente = False
            time.sleep(5)
            apartado_noticias = DRIVER.find_elements_by_tag_name("div")
            for elemento in apartado_noticias:
                es_apartado_noticias = elemento.get_attribute("data-trackable")
                if es_apartado_noticias == "news":
                    try:
                        buscar_empresa = elemento.find_elements_by_tag_name("li")
                        buscar_empresa[0].click()
                        break
                    except Exception:
                        siguiente = True
                        break

            if siguiente:
                continue

            time.sleep(1)
            sigue = False
            while len(lista_urls) < numero_noticias:
                if sigue:
                    break
                time.sleep(1)
                noticias = DRIVER.find_elements_by_class_name("o-teaser__heading")
                for noticia in noticias:
                    link_noticia = noticia.find_element_by_tag_name("a").get_attribute("href")
                    lista_urls.append(link_noticia)

                cambio_pagina = DRIVER.find_element_by_class_name(
                    "js-track-scroll-event"
                ).find_elements_by_tag_name("div")
                for elemento in cambio_pagina:
                    if elemento.get_attribute("aria-label") == "Pagination":
                        boton_siguiente = elemento.find_elements_by_tag_name("a")[1]
                        try:
                            boton_siguiente.click()
                        except Exception:
                            sigue = True
                            break

            dic_empresas.setdefault(empresa, lista_urls)
            pickle.dump(dic_empresas, file_obj)


def load_url_mapping():
    dic_empresas = {}
    with open(URL_PICKLE_PATH, "rb") as file_obj:
        while True:
            try:
                dic_empresas = dict(pickle.load(file_obj))
            except EOFError:
                return dic_empresas


def extraer_noticias():
    dic_empresas = load_url_mapping()
    empresas = list(dic_empresas.keys())

    for empresa in empresas:
        lista_urls = dic_empresas[empresa]
        lista_ticker = []
        lista_nombre_completo = []
        lista_datetime = []
        lista_titular = []
        lista_subtitular = []
        lista_texto_completo = []

        for url in lista_urls:
            try:
                DRIVER.get(url)
                datetime_value = DRIVER.find_element_by_tag_name("time").get_attribute("datetime")
                titulo = (
                    DRIVER.find_element_by_class_name("topper__headline")
                    .find_element_by_tag_name("span")
                    .text
                )

                texto_noticia = ""
                detector_texto_noticia = DRIVER.find_element_by_class_name(
                    "article__content"
                ).find_elements_by_tag_name("div")
                for bloque in detector_texto_noticia:
                    texto_detectado = bloque.get_attribute("class")
                    if (
                        texto_detectado
                        == "article__content-body n-content-body js-article__content-body"
                    ):
                        for parrafo in bloque.find_elements_by_tag_name("p"):
                            texto_noticia += parrafo.text

                ticker = next(
                    key for key, nombre_completo in COMPANY_MAPPING.items() if nombre_completo == empresa
                )
                lista_ticker.append(ticker)
                lista_nombre_completo.append(empresa)
                lista_datetime.append(datetime_value)
                lista_titular.append(titulo)

                try:
                    subtitulo = DRIVER.find_element_by_class_name("topper__standfirst").text
                except Exception:
                    subtitulo = ""
                lista_subtitular.append(subtitulo)
                lista_texto_completo.append(texto_noticia)
            except Exception:
                continue

        dataframe = pd.DataFrame(
            {
                "Ticker": lista_ticker,
                "Nombre_Completo": lista_nombre_completo,
                "Date_Time": lista_datetime,
                "Titular": lista_titular,
                "Subtitular": lista_subtitular,
                "Texto": lista_texto_completo,
            }
        )
        dataframe.to_csv(os.path.join(NOTICIAS_PATH, empresa + ".csv"), sep=";", index=False)

    print("Fin")


def main():
    global DRIVER

    start_time = time.time()
    username, password = require_credentials()
    DRIVER = webdriver.Chrome()

    try:
        login(DRIVER, username, password)
        extraer_noticias()
    finally:
        DRIVER.quit()

    print(f"Duracion total: {time.time() - start_time:.2f} segundos")


if __name__ == "__main__":
    main()
