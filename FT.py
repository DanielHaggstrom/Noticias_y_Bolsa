from get_names import dicNombres
from selenium import webdriver
import selenium
import time
import pickle
import pandas as pd
startTime = time.time()

loginUsername = 'arru.aizpu@gmail.com'
loginContraseña = 'usvefñuouyacnrpuybacpl'
empresasTicker = list(dicNombres.keys())
empresas = list(dicNombres.values())

url = 'https://www.ft.com/'
driver = webdriver.Chrome()
driver.get(url)
continua = False
buscadorSignIn = driver.find_elements_by_class_name('o-header__nav-item')
while not continua:
    for k in range(0, len(buscadorSignIn)):
        signIn = buscadorSignIn[k].find_element_by_tag_name(
            'a').get_attribute('data-trackable')
        if signIn == 'Sign In':
            buscadorSignIn[k].click()
            continua = True
            break

time.sleep(0.5)
introductorEmail = driver.find_element_by_id('enter-email')
introductorEmail.send_keys(loginUsername)

enterEmail = driver.find_element_by_id('enter-email-next')
enterEmail.click()
time.sleep(0.5)

introductorPassword = driver.find_element_by_id('enter-password')
introductorPassword.send_keys(loginContraseña)

enterPassword = driver.find_element_by_tag_name('button')
enterPassword.click()
print()


def extraerUrls(empresas):
    f = open("listaUrls.pkl", "wb")
    dicEmpresas = {}
    numeroNoticias = 10000
    siguiente = False
    contador = -1
    for i in empresas:
        contador += 1
        listaUrls = []
        if siguiente != True:
            posibilidadesBuscador = driver.find_elements_by_tag_name('a')
            for j in range(0, len(posibilidadesBuscador)):
                detectorBuscador = posibilidadesBuscador[j].get_attribute(
                    'data-trackable')
                if detectorBuscador == 'search-toggle':
                    posibilidadesBuscador[j].click()
                    break

            introductorEmpresa = driver.find_element_by_class_name(
                'o-header__search-term')
            introductorEmpresa.send_keys(i[:len(i)-1])
        else:
            introductorEmpresa.clear()
            introductorEmpresa.send_keys(i[:len(i)-1])

        siguiente = False
        time.sleep(5)
        apartadoNoticias = driver.find_elements_by_tag_name('div')
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
            # if len(listaUrls) > 2920:
            dicEmpresas.setdefault(i, listaUrls)
            pickle.dump(dicEmpresas, f)
    return None


def extraerNoticias(loginUsername, loginContraseña):
    # Método correcto para leer el archivo pickle en el que estan todas las url de las noticias
    f = open('listaUrls.pkl', 'rb')
    # t = open('listaNoticias.pkl','wb')
    while 1:
        try:
            dicEmpresas = dict(pickle.load(f))
        except EOFError:
            break

    empresas = list(dicEmpresas.keys())
    contador = 17
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
                driver.get(j)
                # Declaramos una lista vacía donde introduciremos el contenido de cada web que recorremos
                dateTime = driver.find_element_by_tag_name(
                    'time').get_attribute('datetime')
                titulo = driver.find_element_by_class_name(
                    'topper__headline').find_element_by_tag_name('span').text
                textoNoticia = ''
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

                for key in dicNombres:
                    nombreCompleto = dicNombres.get(key)
                    if nombreCompleto == empresa:
                        listaTicker.append(key)
                        break
                listaNombreCompleto.append(nombreCompleto)
                listaDateTime.append(dateTime)
                listaTitular.append(titulo)
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
        data = {'Ticker': listaTicker, 'Nombre_Completo': listaNombreCompleto, 'Date_Time': listaDateTime,
                'Titular': listaTitular, 'Subtitular': listaSubtitular, 'Texto': listaTextoCompleto}
        df = pd.DataFrame(
            data, columns=['Ticker', 'Nombre_Completo', 'Date_Time', 'Titular', 'Subtitular', 'Texto'])
        df.to_csv(empresa + '.csv', sep=';')
        contador += 1
    return print('Fin')

# extraerUrls(empresas)


extraerNoticias(loginUsername, loginContraseña)
finalTime = time.time - startTime
