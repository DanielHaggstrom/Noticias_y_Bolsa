# Aquí se almacenarán algunas variables útiles de uso general
import os

# estas rutas de archivo son independientes de la ubicación del proyecto o del sistema operativo
path_datos = os.path.join(os.path.dirname(__file__), "datos")
path_datos_aprendizaje = os.path.join(path_datos, "aprendizaje")
path_datos_bolsa = os.path.join(path_datos, "bolsa")
path_datos_noticias = os.path.join(path_datos, "noticias")
path_datos_noticias_score = os.path.join(path_datos, "noticias - score")
path_graph = os.path.join(path_datos, "gráficos de modelo")
