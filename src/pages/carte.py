"""Page carte : accidents geolocalisés sur la France."""
import io
import pandas as pd
from dash import dcc, html, Input, Output, callback
from src.utils.common_functions import filter_df, get_dept_options, GRAVITY_COLORS
import plotly.graph_objects as go

DARK_BG    = "#0d0d0d"
CARD_BG    = "#141414"
BORDER_CLR = "#2a2a2a"
RED        = "#ff4444"
MUTED      = "#888888"
WHITE      = "#f0f0f0"


def layout(df: pd.DataFrame) -> html.Div:
    """Retourne le layout de la page carte."""
    return html.Div([
        html.Div([
            html.P("VISUALISATION GÉOGRAPHIQUE",
                   style={"color": RED, "letterSpacing": "4px",
                          "fontSize": "11px", "fontWeight": "700", "marginBottom": "8px"}),
            html.H2("Où les accidents se produisent-ils ?",
                    style={"color": WHITE, "fontSize": "36px",
                           "fontWeight": "900", "margin": "0 0 32px"}),

            html.Div([
                html.Div([
                    html.Label("Département",
                               style={"color": MUTED, "fontSize": "12px", "marginBottom": "8px"}),
                    dcc.Dropdown(id="carte-dep", options=get_dept_options(df),
                                 value="Tous", clearable=False),
                ], style={"flex": 1}),
                html.Div([
                    html.Label("Gravité",
                               style={"color": MUTED, "fontSize": "12px", "marginBottom": "8px"}),
                    dcc.Dropdown(
                        id="carte-grav",
                        options=[
                            {"label": "Toutes", "value": 0},
                            {"label": "Tués", "value": 2},
                            {"label": "Blessés hospitalisés", "value": 3},
                            {"label": "Blessés légers", "value": 4},
                        ],
                        value=0, clearable=False,
                    ),
                ], style={"flex": 1}),
            ], style={"display": "flex", "gap": "24px", "marginBottom": "24px"}),
        ], style={"padding": "40px 40px 0"}),

        dcc.Graph(id="carte-map", config={"displayModeBar": False},
                  style={"height": "75vh"}),

        dcc.Store(id="carte-store", data=df[
            ["Num_Acc", "lat", "long", "grav", "grav_label",
             "dep", "atm_label", "catr_label", "mois_nom"]
        ].to_json()),
    ], style={"background": DARK_BG, "color": WHITE})



@callback(
    Output("carte-map", "figure"),
    Input("carte-dep",   "value"),
    Input("carte-grav",  "value"),
    Input("carte-store", "data"),
)
def update_carte(dep: str, grav: int, data_json: str):
    """Met a jour la carte selon les filtres."""
    dff = filter_df(pd.read_json(io.StringIO(data_json)), dep, grav)

    if len(dff) > 20000:
        dff = dff.sample(20000, random_state=42)

    order = ["Indemne", "Blesse leger", "Blesse hospitalise", "Tue"]

    fig = go.Figure()
    for cat in order:
        sub = dff[dff["grav_label"] == cat]
        if sub.empty:
            continue
        fig.add_trace(go.Scattermapbox(
            lat=sub["lat"],
            lon=sub["long"],
            mode="markers",
            marker=dict(size=5, color=GRAVITY_COLORS[cat], opacity=0.7),
            name=cat,
            hovertemplate="<b>" + cat + "</b><br>%{text}<extra></extra>",
            text=sub["atm_label"] + " · " + sub["catr_label"],
        ))

    fig.update_layout(
        mapbox=dict(style="carto-darkmatter", zoom=5, center={"lat": 46.8, "lon": 2.3}),
        paper_bgcolor="#0d0d0d",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(
            bgcolor="#141414", bordercolor="#2a2a2a", borderwidth=1,
            font=dict(color="#f0f0f0"),
            title=dict(text="Gravité", font=dict(color="#ff4444")),
        ),
        uirevision="stable",
    )
    return fig