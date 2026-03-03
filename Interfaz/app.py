import json
import os
from pathlib import Path

import pandas as pd
import plotly.graph_objs as go
from dash import Dash, Input, Output, State, dash_table, dcc, html


BASE_DIR = Path(__file__).resolve().parent
NEWS_DIR = BASE_DIR / "noticias"
PREDICTION_TABLE_PATH = BASE_DIR / "predicciones" / "tabla.csv"
PREDICTION_SERIES_PATH = BASE_DIR / "predicciones" / "prediccion.csv"
TICKERS_PATH = BASE_DIR / "tickers.json"

EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
PRIMARY_COLOR = "#124559"
ACCENT_COLOR = "#f59e0b"
PAGE_STYLE = {
    "maxWidth": "1100px",
    "margin": "0 auto",
    "padding": "24px 16px 40px",
}
CARD_STYLE = {
    "backgroundColor": "#ffffff",
    "border": "1px solid #d0d7de",
    "borderRadius": "12px",
    "padding": "20px",
    "boxShadow": "0 8px 24px rgba(15, 23, 42, 0.08)",
}


def inverse_mapping(mapping):
    return {value: key for key, value in mapping.items()}


def drop_generated_index_columns(dataframe):
    return dataframe.loc[:, ~dataframe.columns.str.startswith("Unnamed:")]


def load_company_mapping():
    with TICKERS_PATH.open(encoding="utf-8") as json_file:
        return json.load(json_file)


def load_prediction_table():
    dataframe = pd.read_csv(PREDICTION_TABLE_PATH)
    return drop_generated_index_columns(dataframe)


def load_prediction_series():
    dataframe = pd.read_csv(PREDICTION_SERIES_PATH)
    dataframe = drop_generated_index_columns(dataframe)
    dataframe["Date"] = pd.to_datetime(dataframe["Date"])
    return dataframe


TICKER_TO_COMPANY = load_company_mapping()
COMPANY_TO_TICKER = inverse_mapping(TICKER_TO_COMPANY)
PREDICTION_TABLE = load_prediction_table()
PREDICTION_SERIES = load_prediction_series()
AVAILABLE_COMPANIES = sorted(
    TICKER_TO_COMPANY[ticker]
    for ticker in PREDICTION_SERIES.columns
    if ticker != "Date" and ticker in TICKER_TO_COMPANY
)
DEFAULT_COMPANY = "Apple Inc" if "Apple Inc" in AVAILABLE_COMPANIES else AVAILABLE_COMPANIES[0]


def make_archive_notice():
    return html.Div(
        [
            html.Strong("Archived project."),
            html.Span(
                " The dashboard is preserved as a read-only demo of the original academic work."
            ),
        ],
        style={
            "backgroundColor": "#fff7ed",
            "border": "1px solid #fdba74",
            "borderRadius": "10px",
            "color": "#9a3412",
            "padding": "12px 16px",
            "marginBottom": "20px",
        },
    )


def make_header():
    return html.Div(
        [
            html.H1(
                "Noticias y Bolsa",
                style={"color": "#ffffff", "margin": 0, "fontSize": "2.4rem"},
            ),
            html.P(
                "Sentiment-driven stock prediction project archived for reference.",
                style={"color": "#dbeafe", "margin": "8px 0 0"},
            ),
        ],
        style={
            "background": f"linear-gradient(135deg, {PRIMARY_COLOR}, #1d3557)",
            "borderRadius": "16px",
            "padding": "24px",
            "marginBottom": "20px",
        },
    )


def make_nav():
    link_style = {"marginRight": "16px"}
    return html.Div(
        [
            dcc.Link("Inicio", href="/", style=link_style),
            dcc.Link("Lista de predicciones", href="/page-1", style=link_style),
            dcc.Link("Buscador de empresas", href="/page-2", style=link_style),
            dcc.Link("Ayuda", href="/page-3"),
        ],
        style={"marginBottom": "24px"},
    )


def wrap_page(children):
    return html.Div([make_header(), make_archive_notice(), make_nav(), *children], style=PAGE_STYLE)


def build_prediction_figure(company_name):
    ticker_symbol = COMPANY_TO_TICKER.get(company_name)
    if ticker_symbol is None or ticker_symbol not in PREDICTION_SERIES:
        return go.Figure()

    figure = go.Figure(
        data=[
            go.Scatter(
                x=PREDICTION_SERIES["Date"],
                y=PREDICTION_SERIES[ticker_symbol],
                mode="lines",
                name="Predicted close",
                line={"color": PRIMARY_COLOR, "width": 3},
            )
        ]
    )
    figure.update_layout(
        title=f"{company_name} close prediction",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin={"l": 40, "r": 20, "t": 60, "b": 40},
        xaxis_title="Date",
        yaxis_title="Share price (USD)",
    )
    return figure


def load_latest_news(company_name):
    news_path = NEWS_DIR / f"{company_name}.csv"
    if not news_path.exists():
        return [], [{"name": "Titular", "id": "Titular"}], f"No bundled news found for {company_name}."

    dataframe = pd.read_csv(news_path, sep=";")
    dataframe = drop_generated_index_columns(dataframe)
    if "Date_Time" in dataframe.columns:
        dataframe = dataframe.sort_values("Date_Time", ascending=False)
    headlines = dataframe.loc[:, ["Titular"]].head(10).to_dict("records")
    columns = [{"name": "Titular", "id": "Titular"}]
    return headlines, columns, f"Noticias relacionadas con {company_name}"


DEFAULT_NEWS_DATA, DEFAULT_NEWS_COLUMNS, DEFAULT_NEWS_HEADING = load_latest_news(DEFAULT_COMPANY)


def create_app():
    app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=EXTERNAL_STYLESHEETS)
    app.title = "Noticias y Bolsa"

    index_page = wrap_page(
        [
            html.Div(
                [
                    html.H2("Menu"),
                    html.P(
                        "Explore the archived prediction table, browse bundled company data, "
                        "or review the project notes."
                    ),
                ],
                style=CARD_STYLE,
            )
        ]
    )

    page_1_layout = wrap_page(
        [
            html.Div(
                [
                    html.H2("Lista de predicciones"),
                    dash_table.DataTable(
                        id="table2",
                        data=PREDICTION_TABLE.to_dict("records"),
                        columns=[{"name": column, "id": column} for column in PREDICTION_TABLE.columns],
                        style_as_list_view=True,
                        style_cell={"padding": "8px", "textAlign": "left"},
                        style_header={
                            "backgroundColor": "#f8fafc",
                            "fontWeight": "bold",
                        },
                        page_size=15,
                    ),
                ],
                style=CARD_STYLE,
            )
        ]
    )

    page_2_layout = wrap_page(
        [
            html.Div(
                [
                    html.H2("Buscador de empresas"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Seleccione una empresa"),
                                    dcc.Dropdown(
                                        id="dropdown1",
                                        options=[
                                            {"label": company_name, "value": company_name}
                                            for company_name in AVAILABLE_COMPANIES
                                        ],
                                        value=DEFAULT_COMPANY,
                                        clearable=False,
                                    ),
                                    html.Button(
                                        id="submit_button",
                                        n_clicks=0,
                                        children="Actualizar vista",
                                        style={
                                            "marginTop": "12px",
                                            "backgroundColor": ACCENT_COLOR,
                                            "border": "none",
                                            "borderRadius": "8px",
                                            "color": "#111827",
                                            "padding": "10px 16px",
                                        },
                                    ),
                                    dcc.Graph(id="graph", figure=build_prediction_figure(DEFAULT_COMPANY)),
                                ],
                                style={"width": "100%"},
                            ),
                            html.Div(
                                [
                                    html.H3(id="h3", children=DEFAULT_NEWS_HEADING),
                                    dash_table.DataTable(
                                        id="table",
                                        data=DEFAULT_NEWS_DATA,
                                        columns=DEFAULT_NEWS_COLUMNS,
                                        style_as_list_view=True,
                                        style_cell={"padding": "8px", "textAlign": "left"},
                                        style_header={
                                            "backgroundColor": "#f8fafc",
                                            "fontWeight": "bold",
                                        },
                                        page_size=10,
                                    ),
                                ],
                                style={"width": "100%"},
                            ),
                        ],
                        style={"display": "grid", "gap": "20px"},
                    ),
                ],
                style=CARD_STYLE,
            )
        ]
    )

    page_3_layout = wrap_page(
        [
            html.Div(
                [
                    html.H2("Ayuda"),
                    dcc.Markdown(
                        """
This archived dashboard shows:

- bundled prediction outputs for a subset of S&P 500 companies
- the historical headlines used by the original project
- a read-only view of the final academic artifact

The repository also includes the legacy data collection and model training scripts,
but those scripts depend on third-party sites and older ML tooling.
"""
                    ),
                ],
                style=CARD_STYLE,
            )
        ]
    )

    app.layout = html.Div([dcc.Location(id="url", refresh=False), html.Div(id="page-content")])

    @app.callback(
        [
            Output("graph", "figure"),
            Output("table", "data"),
            Output("table", "columns"),
            Output("h3", "children"),
        ],
        [Input("submit_button", "n_clicks")],
        [State("dropdown1", "value")],
    )
    def update_company_view(_n_clicks, selected_company):
        figure = build_prediction_figure(selected_company)
        table_data, table_columns, heading = load_latest_news(selected_company)
        return figure, table_data, table_columns, heading

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        if pathname == "/page-1":
            return page_1_layout
        if pathname == "/page-2":
            return page_2_layout
        if pathname == "/page-3":
            return page_3_layout
        return index_page

    return app


app = create_app()
server = app.server


if __name__ == "__main__":
    debug = os.getenv("DASH_DEBUG", "").lower() in {"1", "true", "yes"}
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8050"))
    app.run(host=host, port=port, debug=debug)
