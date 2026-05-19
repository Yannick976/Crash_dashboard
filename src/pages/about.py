"""Page a propos : sources, methode, auteurs."""
from dash import html

DARK_BG    = "#0d0d0d"
CARD_BG    = "#141414"
BORDER_CLR = "#2a2a2a"
RED        = "#ff4444"
MUTED      = "#888888"
WHITE      = "#f0f0f0"


def layout() -> html.Div:
    """Retourne le layout de la page a propos."""
    return html.Div([
        html.Div([
            html.P("À PROPOS",
                   style={"color": RED, "letterSpacing": "4px",
                          "fontSize": "11px", "fontWeight": "700", "marginBottom": "8px"}),
            html.H2("Sources & Méthode",
                    style={"color": WHITE, "fontSize": "36px",
                           "fontWeight": "900", "margin": "0 0 40px"}),

            html.Div([
                _section("Source des données", [
                    html.P("Ministère de l'Intérieur – Observatoire National Interministériel de la Sécurité Routière (ONISR)", style={"color": MUTED}),
                    html.A("Accéder aux données sur data.gouv.fr →",
                           href="https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere/",
                           target="_blank",
                           style={"color": RED, "textDecoration": "none"}),
                ]),
                _section("Licence", [
                    html.P("Licence Ouverte v2.0 – données publiques, librement réutilisables.", style={"color": MUTED}),
                ]),
                _section("Méthode", [
                    html.P("Les 3 fichiers (caractéristiques, lieux, usagers) sont fusionnés sur l'identifiant unique Num_Acc. La gravité retenue par accident est la plus sévère parmi tous les usagers impliqués.", style={"color": MUTED}),
                ]),
                _section("Technologies", [
                    html.P("Python · Pandas · Dash · Plotly · Dash Bootstrap Components", style={"color": MUTED}),
                ]),
            ]),
        ], style={"padding": "40px", "maxWidth": "800px"}),
    ], style={"background": DARK_BG, "color": WHITE, "minHeight": "100vh"})


def _section(title: str, children: list) -> html.Div:
    """Section stylee pour la page about."""
    return html.Div([
        html.H4(title, style={"color": WHITE, "fontWeight": "700",
                              "marginBottom": "12px", "fontSize": "14px",
                              "letterSpacing": "2px"}),
        *children,
    ], style={
        "background": CARD_BG, "border": f"1px solid {BORDER_CLR}",
        "borderLeft": f"3px solid {RED}",
        "borderRadius": "4px", "padding": "24px",
        "marginBottom": "16px"
    })