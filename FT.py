# Este script extrae las noticias de bolsa del Financial Times de cada empresa en la que estamos interesados
import json
import config
import os
from selenium import webdriver
import time
import pickle
import pandas as pd


startTime = time.time()
dict_path = os.path.join(config.path_datos, "tickers.json")
dicNombres = json.load(os.path.join(config.path_datos, "tickers.json"))
loginUsername = 'arru.aizpu@gmail.com'
loginContraseña = 'usvefñuouyacnrpuybacpl'
empresasTicker = list(dicNombres.keys())
empresas = list(dicNombres.values())

noticias_path = config.path_datos_noticias

# Este es el código necesario para poder logearnos en el FT
url = 'https://www.ft.com/'
driver = webdriver.Chrome() # Manera de abrir el navegador con el controlador
driver.get(url)
continua = False
buscadorSignIn = driver.find_elements_by_class_name('o-header__nav-item')
while not continua: # De esta manera buscar y pulsar el botón de Sign In
    for k in range(0, len(buscadorSignIn)):
        signIn = buscadorSignIn[k].find_element_by_tag_name(
            'a').get_attribute('data-trackable')
        if signIn == 'Sign In':
            buscadorSignIn[k].click()
            continua = True
            break

time.sleep(0.5) # Durante este script hay muchos descansos, para así asegurarnos de que carga la página
introductorEmail = driver.find_element_by_id('enter-email') # Búsqueda de espacio donde se introduce el email
introductorEmail.send_keys(loginUsername) # Introducción del email

enterEmail = driver.find_element_by_id('enter-email-next') # Búsqueda botón para continuar
enterEmail.click() # Presionar el botón
time.sleep(0.5)

introductorPassword = driver.find_element_by_id('enter-password') # Búsqueda de espacio donde se introduce la contraseña
introductorPassword.send_keys(loginContraseña) # Introducción. contraseña

enterPassword = driver.find_element_by_tag_name('button') # Búsqueda botón para continuar
enterPassword.click()  # Presionar el botón
print() # Importante poner un punto de parada aquí, dado que nos salta el saber si somos un robot, cosa que hay que hacer a mano


def extraerUrls(empresas): # Función para extraer los links de todas las noticias
    f = open("listaUrls.pkl", "wb")
    dicEmpresas = {}
    numeroNoticias = 10000
    siguiente = False
    contador = 0
    for i in empresas:
        contador += 1
        listaUrls = []
        # Esto sirve para detectar el buscador
        if siguiente != True:
            posibilidadesBuscador = driver.find_elements_by_tag_name('a')
            for j in range(0, len(posibilidadesBuscador)):
                detectorBuscador = posibilidadesBuscador[j].get_attribute(
                    'data-trackable')
                if detectorBuscador == 'search-toggle':
                    posibilidadesBuscador[j].click()
                    break

            # Colocar el nombre de la empresa en el buscador, con todas las letras menos una, para que asi el buscador lo encuentre
            introductorEmpresa = driver.find_element_by_class_name(
                'o-header__search-term')
            introductorEmpresa.send_keys(i[:len(i)-1])
        else:
            # En caso de no encontrar la empresa
            introductorEmpresa.clear()
            introductorEmpresa.send_keys(i[:len(i)-1])

        siguiente = False
        time.sleep(5)
        apartadoNoticias = driver.find_elements_by_tag_name('div')
        # Pulsar en la primera empresa que encuentra
        for j in range(0, len(apartadoNoticias)):
            esApartadoNoticias = apartadoNoticias[j].get_attribute(
                'data-trackable')
            if esApartadoNoticias == 'news':
                try:
                    buscarEmpresa = apartadoNoticias[j].find_elements_by_tag_name(
                        'li')
                    buscarEmpresa[0].click()
                    break
                except:
                    siguiente = True
                    break

        # Recorrer todas las noticias y guardar los links
        if siguiente != True:
            time.sleep(1)
            noticias = driver.find_elements_by_class_name('o-teaser__heading')
            sigue = False
            while len(listaUrls) < numeroNoticias:
                if sigue == True:
                    break
                time.sleep(1)
                noticias = driver.find_elements_by_class_name(
                    'o-teaser__heading')
                for j in range(0, len(noticias)):
                    linkNoticia = noticias[j].find_element_by_tag_name(
                        'a').get_attribute('href')
                    listaUrls.append(linkNoticia)

                # Cambiar página
                cambioPagina = driver.find_element_by_class_name(
                    'js-track-scroll-event').find_elements_by_tag_name('div')
                for j in range(0, len(cambioPagina)):
                    esBoton = cambioPagina[j].get_attribute('aria-label')
                    if esBoton == 'Pagination':
                        botonSiguiente = cambioPagina[j].find_elements_by_tag_name('a')[
                            1]
                        try:
                            botonSiguiente.click()
                        except:
                            sigue = True
                            break
            dicEmpresas.setdefault(i, listaUrls)
            # Crear pickle con lista Urls
            pickle.dump(dicEmpresas, f)
    return None


def extraerNoticias(loginUsername, loginContraseña):
    # Método correcto para leer el archivo pickle en el que estan todas las url de las noticias
    f = open('listaUrls.pkl', 'rb')
    while 1:
        try:
            dicEmpresas = dict(pickle.load(f))
        except EOFError:
            break

    empresas = list(dicEmpresas.keys())
    contador = 17 # Contador para poder ir compilando el programa por fases
    for i in range(contador,len(empresas)):
        empresa = empresas[i]
        # Cojemos la lista de urls de cada empresa
        listaUrls = dicEmpresas[empresa]
        # Declaramos lista vacía donde introduciremos el contenido de todas las web por separado
        listaTicker = []
        listaNombreCompleto = []
        listaDateTime = []
        listaTitular = []
        listaSubtitular = []
        listaTextoCompleto = []
        for j in listaUrls:
            try:
                # Entramos en cada link
                driver.get(j)
                # Almacenamos la fecha
                dateTime = driver.find_element_by_tag_name(
                    'time').get_attribute('datetime')
                # Almacenamos el titular
                titulo = driver.find_element_by_class_name(
                    'topper__headline').find_element_by_tag_name('span').text
                textoNoticia = ''
                # Almacenamos todo el texto de la noticia
                detectorTextoNoticia = driver.find_element_by_class_name(
                    'article__content').find_elements_by_tag_name('div')
                for k in range(0, len(detectorTextoNoticia)):
                    textoDetectado = detectorTextoNoticia[k].get_attribute(
                        'class')
                    if textoDetectado == 'article__content-body n-content-body js-article__content-body':
                        texto = detectorTextoNoticia[k].find_elements_by_tag_name(
                            'p')
                        for c in range(0, len(texto)):
                            textoNoticia += texto[c].text
                # Almacenamos cada noticia con su empresa mediante el código ticker
                for key in dicNombres:
                    nombreCompleto = dicNombres.get(key)
                    if nombreCompleto == empresa:
                        listaTicker.append(key)
                        break
                # Almacenamos cada noticia con su empresa mediante el nombre de la empresa
                listaNombreCompleto.append(nombreCompleto)
                listaDateTime.append(dateTime)
                listaTitular.append(titulo)
                # Almacenamos el titular
                try:
                    subtitulo = driver.find_element_by_class_name(
                        'topper__standfirst').text
                    listaSubtitular.append(subtitulo)
                except:
                    subtitulo = ''
                    listaSubtitular.append(subtitulo)
                listaTextoCompleto.append(textoNoticia)
            except:
                continue
        # Manera de guardar toda la información en csv
        data = {'Ticker': listaTicker, 'Nombre_Completo': listaNombreCompleto, 'Date_Time': listaDateTime,
                'Titular': listaTitular, 'Subtitular': listaSubtitular, 'Texto': listaTextoCompleto}
        df = pd.DataFrame(
            data, columns=['Ticker', 'Nombre_Completo', 'Date_Time', 'Titular', 'Subtitular', 'Texto'])
        df.to_csv(os.path.join(noticias_path, empresa + '.csv'), sep=';')
        contador += 1
    return print('Fin')

# extraerUrls(empresas)


extraerNoticias(loginUsername, loginContraseña)
finalTime = time.time - startTime
