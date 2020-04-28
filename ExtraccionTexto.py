import requests
import bs4


def extraccionDatos(url):
    contenido = ""
    page = requests.get(url).text
    soup = bs4.BeautifulSoup(page, 'html.parser')
    titulo = str(soup.h1.string)
    contenido = contenido + titulo + " "
    try:
        subtitulo = str(soup.find(id="article-summary").string)
        contenido = contenido + subtitulo + " "
        listaTexto = soup.find(itemprop="articleBody").contents
        for i in range(0, len(listaTexto)):
            contenido += listaTexto[i].text
    except:
        next
    return contenido
