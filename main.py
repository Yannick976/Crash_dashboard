import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from src.utils.clean_data import load_clean
from src.pages import home, carte, analyse, about
from config import APP_TITLE, APP_PORT, DEBUG

df = load_clean()

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CYBORG],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
app.title = APP_TITLE

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),

    # NAVBAR
    html.Nav([
        html.Div([
            html.Span("🚨", style={"fontSize": "24px"}),
            html.Span("ACCIDENTOLOGIE FRANCE 2024",
                      style={"fontWeight": "900", "fontSize": "18px",
                             "letterSpacing": "3px", "color": "#ff4444"}),
        ], style={"display": "flex", "alignItems": "center", "gap": "12px"}),

        html.Div([
            dcc.Link("ACCUEIL",  href="/",        className="nav-link-custom"),
            dcc.Link("CARTE",    href="/carte",   className="nav-link-custom"),
            dcc.Link("ANALYSE",  href="/analyse", className="nav-link-custom"),
            dcc.Link("À PROPOS", href="/about",   className="nav-link-custom"),
        ], style={"display": "flex", "gap": "32px"}),
    ], style={
        "display": "flex", "justifyContent": "space-between", "alignItems": "center",
        "padding": "16px 40px", "background": "#0a0a0a",
        "borderBottom": "1px solid #ff4444", "position": "sticky", "top": 0, "zIndex": 999
    }),

    html.Div(id="page-content"),
], style={"background": "#0d0d0d", "minHeight": "100vh", "fontFamily": "'Segoe UI', sans-serif"})


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname: str) -> html.Div:
    """Route vers la bonne page selon l'URL."""
    if pathname == "/carte":
        return carte.layout(df)
    elif pathname == "/analyse":
        return analyse.layout(df)
    elif pathname == "/about":
        return about.layout()
    return home.layout(df)


if __name__ == "__main__":
    app.run(debug=DEBUG, port=APP_PORT)