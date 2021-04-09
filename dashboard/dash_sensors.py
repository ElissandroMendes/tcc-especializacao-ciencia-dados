import os
import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np


from dash.dependencies import Input, Output, State
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)
app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

app.layout = html.Div(
    [
        html.Div([
            html.H4("DASHBOARD IoT GRID - Acme Ltd.", className="app__header__title"),
        ], className="app__header"),
        html.Div([
            html.Div([
                html.Div([
                    html.H6("Controls...", className="graph__controls")
                ]),
            ], className="wind__speed__container"),
        ], className="controls__header"),
        html.Div([
            html.Div(
                [
                    html.Div(
                        [html.H6("TEMPERATURE (K)", className="graph__title")]
                    ),
                    dcc.Graph(
                        id="temp",
                        figure=dict(
                            layout=dict(
                                plot_bgcolor=app_color["graph_bg"],
                                paper_bgcolor=app_color["graph_bg"],
                            )
                        ),
                    ),
                    dcc.Interval(
                        id="temp-update",
                        interval=int(GRAPH_INTERVAL),
                        n_intervals=0,
                    ),
                ],
                className="one-half column wind__speed__container",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H6("HUMIDITY", className="graph__title")]
                    ),
                    dcc.Graph(
                        id="humid",
                        figure=dict(
                            layout=dict(
                                plot_bgcolor=app_color["graph_bg"],
                                paper_bgcolor=app_color["graph_bg"],
                            )
                        ),
                    ),
                    dcc.Interval(
                        id="humid-update",
                        interval=int(GRAPH_INTERVAL),
                        n_intervals=0,
                    ),
                ],
                className="one-half column wind__speed__container",
            ),
        ], className="app__content")
    ], className="app__container")

if __name__ == '__main__':
    app.run_server(debug=True)