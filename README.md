# ProyectoBigData
Repositorio para las asignaturas Proyecto Big Data II y III

El objetivo es predecir los valores de bolsa (índice S&P 500) partiendo del análisis de sentimiento en las noticias. Trabajamos con datos de granularidad semanal. Obtenemos los valores de bolsa de Yahoo Finance, y los datos de prensa de Finantial Times.

## Tareas por hacer
[] Añadir más datos.
[] Probar varios algoritmos para los modelos de series temporales.
[] Probar varios parámetros.
[] Mejorar el análisis de sentimiento.

## Dependencias
Nuestro proyecto emplea las librerías indicadas en `requirements.txt`, notablemente `numpy`, `pandas`, `nltk`, `selenium` y `sklearn`. Estas librerías pueden instalarse mediante `pip install -r requirements.txt`, pero es necesario activar el virtual environment antes.

## Información general
**get_names** construye, a partir de `datos/NASDAQ.txt` y `datos/NYSE.txt` un diccionario que asocia símbolos ticker con nombres de compañía. Este diccionario es guardado como un archivo json en `datos/tickers.json`.

**ExtraccionTexto** ??

**FT** extrae noticias del periódico *Finantial Times* relacionadas con las empresas del S&P 500, y genera una serie de archivos CSV con la fecha y el contenido de la noticia, agrupados por empresa: `datos/noticias/<nombre de empresa>.csv`.

**analizar_noticias** copia los dataframes generados por `FT.py`, pero sustituyendo el contenido de las noticias por la puntuación del análisis de sentimiento. Los resultados se guardan en `datos/noticias - score/<ticker de empresa>.csv`.

**market_data** obtiene los datos de bolsa de las empresas del S&P 500, agrupados semanalmente y por compañía. Los guarda en `datos/bolsa/<ticker de empresa>.csv`.

**generar_dataset_final** a partir de los datos generados por `analizar_noticias.py` y `market_data.py` crea un dataset para alimentar el modelo de serie temporal. Este dataset tiene la fecha del lunes de cada semana, el crecimiento de las empresas en ese periodo, y la media de su puntuación de noticias. Se guarda en `datos/aprendizaje/dataset.csv`.

**prototype** con los datos finales de `generar_dataset_final.py`, particiona los datos para entrenar y testear un modelo de series temporales.
