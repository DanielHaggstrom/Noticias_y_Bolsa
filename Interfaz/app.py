import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import json
import pandas as pd
from dash_table import DataTable
from itertools import dropwhile
import csv


#Lista con las empresas que constan en nuestra aplicación
empresas = ["Apple Inc","Accenture Plc","American International Group","Adv Micro Devices","Bank of America Corp","Bank of New York Mellon Corp"
            ,"Blackrock","Citigroup Inc","Caterpillar Inc","Comcast Corp A","CME Group Inc","Conocophillips","Cisco Systems Inc",
            "Chevron Corp","Delta Air Lines Inc","Ebay Inc","Freeport-Mcmoran Inc","Fedex Corp","Goldman Sachs Group","Home Depot",
            "International Business Machines","Intercontinental Exchange","Intel Corp","Gartner Inc","Johnson & Johnson","Lockheed Martin Corp",
            "Mastercard Inc","McDonald's Corp","Morgan Stanley","MSCI Inc","Microsoft Corp","Nasdaq Inc","Netflix Inc","Nike Inc",
            "Oracle Corp","Pepsico Inc","Pfizer Inc","Qualcomm Inc","Starbucks Corp","State Street Corp","Target Corp","United Parcel Service",
            "Visa Inc","Verizon Communications Inc","Exxon Mobil Corp"]

#Aqui se prepara la tabla que se muestra en el apartado de lista de predicciones
path = r'C:\\Users\\jhern\\PycharmProjects\\AppBigData\\predicciones\\tabla.csv'
with open(path) as f :
    f = dropwhile(lambda x : x.startswith("#!!") ,f)
    r = csv.reader(f)
    df2 = pd.DataFrame().from_records(r)
df2.columns = df2.iloc[0]
df2 = df2.iloc[1 :]
df2.columns = ['Empresas', '5/3/2020','11/22/2020']

columns = [{"name": i, "id": i} for i in df2.columns]

data2 = df2.to_dict('records')

#Esta función nos sirve para invertir un diccionario y poder pasar de nombre de la empresa a ticker y viceversa
def inverse_mapping(f):
    return f.__class__(map(reversed, f.items()))


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.H1('Noticias y Bolsa', style={'color': '#FFFFFF', 'background-color': '#5e03fc'}),
    html.H2('Menú'),
    dcc.Link('Lista de predicciones', href='/page-1'),
    html.Br(),
    dcc.Link('Buscador de empresas', href='/page-2'),
    html.Br(),
    dcc.Link('Ayuda',href='/page-3')
])

page_1_layout = html.Div([
    html.H1('Noticias y Bolsa', style={'color': '#FFFFFF', 'background-color': '#5e03fc'}),

    dcc.Link('Volver al menú', href='/'),
    html.H2('Lista de predicciones'),
    html.Br(),


    DataTable(
                id='table2',
                data=data2,
                columns=columns,
                style_as_list_view=True,
                style_cell={'padding': '5px','textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'}

            )


])




page_2_layout = html.Div([
    html.H1('Noticias y Bolsa', style={'color': '#FFFFFF', 'background-color': '#5e03fc'}),

    dcc.Link('Volver al menú', href='/'),
    html.Div([
        html.Div([
            html.H5('Seleccione una empresa'),
            dcc.Dropdown(
                id='dropdown1',
                options=[{'label': i, 'value': i} for i in empresas],
                value='Netflix Inc'
            ),

            html.Button(id='submit_button', n_clicks=0, children=' click aquí realizar la busqueda'),

            html.H2("Gráfica de evolución en el tiempo"),
            dcc.Graph(
                id='graph'
            ),

        ], style={'width': '48%', 'float': 'left', 'display': 'inline-block'}),
        html.Div([
            html.H3(id='h3', children=""),
            DataTable(
                id='table',
                data=[],
                columns=[],
                style_as_list_view=True,
                style_cell={'padding': '5px','textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'}
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ])
])


@app.callback([Output('graph', 'figure'),
               Output('table', 'data'),
               Output('table', 'columns'),
               Output('h3', 'children')],
              [Input('submit_button', 'n_clicks')],
              [State('dropdown1', 'value')])
def update_fig1(n_clicks, drop1):
    #Esta sección prepara la gráfica que se muestra por pantalla
    #Aqui hacemos uso del diccionario tickers para pasar del nombre de la empresa a su ticker, para ello invertimos el
    #diccionario con la función inverse_mapping
    with open(r'C:\Users\jhern\PycharmProjects\AppBigData\tickers.json') as json_file:
        json_data = json.load(json_file)
    inv_json_data = inverse_mapping(json_data)
    ticker_symbol = inv_json_data.get(drop1)
    #Aqui preparamos un dataframe con las predicciones de las empresas para seleccionar una en concreto y graficarla
    path = r'C:\\Users\\jhern\\PycharmProjects\\AppBigData\\predicciones\\prediccion.csv'
    with open(path) as f :
        f = dropwhile(lambda x : x.startswith("#!!") ,f)
        r = csv.reader(f)
        df = pd.DataFrame().from_records(r)
    df.columns = df.iloc[0]
    predicciones = df.iloc[1 :]
    predicciones = predicciones.set_index('Date')
    predicciones.index = pd.to_datetime(predicciones.index)
    #Aqui se selecciona la empresa en concreto que queremos grafocar
    y = predicciones[ticker_symbol]
    #Aqui preparamos los argumentos de la gráfica
    data = []
    trace_close = go.Scatter(x=list(predicciones.index),
                             y=y,
                             name='Close',
                             line=dict(color='#5e03fc'))
    data.append(trace_close)
    layout = go.Layout(
        title=drop1 + ' Close' ,
        xaxis=dict(title='Año' ,ticks='') ,
        yaxis=dict(title='Valor por acción en $' ,ticks='') ,
        height=400
    )

    #esta sección prepara la tabla con los titulares de las noticias
    filename = drop1

    path = r'C:\\Users\\jhern\\PycharmProjects\\AppBigData\\noticias\\' + filename + '.csv'

    data2 = pd.read_csv(path, sep='\t', delimiter=";")

    df2 = pd.DataFrame(data2)
    columns = [{'name': 'Titulares', 'id': 'Titular'}]
    #Se seleccionan las 10 ultimas noticias
    data2 = df2[-10:-1].to_dict('records')
    h3 = 'Noticias relacionadas con ' + drop1

    return {
               'data': data,
               'layout': layout
           }, data2, columns, h3

page_3_layout = html.Div([
    html.H1('Noticias y Bolsa', style={'color': '#FFFFFF', 'background-color': '#5e03fc'}),
    dcc.Link('Volver al menú', href='/'),
    html.Br(),
    dcc.Markdown(
        '''Bienvenido, esta es la aplicación Noticias y bolsa, en ella podras encontrar predicciones futuras sobre algunas de las empresas
        que conforman el S&P500.
        '''
    ),
    html.Br(),
    dcc.Markdown(
        '''En el apartado de Lista de predicciones podrás ver los valores de cierre predichos para distintas empresas.
        '''
    ),
    html.Br(),
    dcc.Markdown(
        '''En el apartado buscador de empresas deberás seleccionar una empresa y pulsar al botón que aparece debajo del buscador, te aparecera
        '''
    ),
    dcc.Markdown(
        '''una gráfica con la evolución de los valores de cierre de dicha empresa junto con las noticias que hemos utilizado para crear la predicción
        '''
    )

    ])


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname =='/page-3':
        return page_3_layout
    else:
        return index_page



if __name__ == '__main__':
    app.run_server(debug=True)