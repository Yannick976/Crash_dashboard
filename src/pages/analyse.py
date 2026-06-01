"""Page analyse : graphiques detailles sur les facteurs d'accidents."""
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from src.utils.common_functions import GRAVITY_COLORS
import pandas as pd

DARK_BG    = "#0d0d0d"
CARD_BG    = "#141414"
BORDER_CLR = "#2a2a2a"
RED        = "#ff4444"
MUTED      = "#888888"
WHITE      = "#f0f0f0"


def _dark_fig(fig, height: int = 350) -> go.Figure:
    """Applique le theme sombre a une figure Plotly."""
    fig.update_layout(
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=MUTED),
        xaxis=dict(gridcolor="#1f1f1f", showline=False),
        yaxis=dict(gridcolor="#1f1f1f", showline=False),
        margin=dict(l=0, r=0, t=50, b=0),
        height=height,
        coloraxis_showscale=False,
    )
    return fig


def layout(df: pd.DataFrame) -> html.Div:
    """Retourne le layout de la page analyse."""

    # Graphique 1 : gravité
    grav = df["grav_label"].value_counts().reset_index()
    grav.columns = ["grav_label", "count"]
    fig_pie = go.Figure(go.Pie(
        labels=grav["grav_label"], values=grav["count"],
        hole=0.6,
        marker=dict(colors=[GRAVITY_COLORS.get(l, "#555555") for l in grav["grav_label"]],
                    line=dict(color="#0d0d0d", width=2)),
        hovertemplate="<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>",
    ))
    fig_pie.update_layout(
        title=dict(text="Répartition par gravité",
                   font=dict(color=WHITE, size=16), x=0),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=MUTED),
        legend=dict(bgcolor=CARD_BG, font=dict(color=WHITE)),
        margin=dict(l=0, r=0, t=50, b=0), height=350,
        annotations=[dict(text=f"<b>{len(df):,}</b>", x=0.5, y=0.5,
                          font=dict(size=20, color=WHITE), showarrow=False)]
    )

    # Graphique 2 : type de route
    route = df["catr_label"].value_counts().reset_index()
    route.columns = ["catr_label", "count"]
    fig_route = _dark_fig(px.bar(
        route.sort_values("count"), x="count", y="catr_label",
        orientation="h",
        title="Accidents par type de route",
        labels={"catr_label": "", "count": "Accidents"},
        color="count", color_continuous_scale=["#1a1a2e", "#ff8c00", "#ff4444"],
    ))

    # Graphique 3 : météo
    atm = df["atm_label"].value_counts().reset_index()
    atm.columns = ["atm_label", "count"]
    fig_atm = _dark_fig(px.bar(
        atm.sort_values("count", ascending=False),
        x="atm_label", y="count",
        title="Accidents par condition météorologique",
        labels={"atm_label": "", "count": "Accidents"},
        color="count", color_continuous_scale=["#1a1a2e", "#ff8c00", "#ff4444"],
    ))
    fig_atm.update_layout(xaxis_tickangle=-30)

    # Graphique 4 : vitesse limite
    if "vma" in df.columns:
        vma = df["vma"].dropna()
        fig_vma = _dark_fig(go.Figure(go.Histogram(
            x=vma, nbinsx=20,
            marker=dict(color="#ff4444", line=dict(color="#0d0d0d", width=1)),
            hovertemplate="Vitesse %{x} km/h<br>%{y:,} accidents<extra></extra>",
        )))
        fig_vma.update_layout(
            title=dict(text="Distribution des vitesses maximales autorisées",
                       font=dict(color=WHITE, size=16), x=0),
            xaxis=dict(title="Vitesse (km/h)", gridcolor="#1f1f1f"),
            yaxis=dict(title="Accidents", gridcolor="#1f1f1f"),
        )
    else:
        fig_vma = go.Figure()

    def _card(graph) -> html.Div:
        return html.Div(
            dcc.Graph(figure=graph, config={"displayModeBar": False}),
            style={"background": CARD_BG, "borderRadius": "4px",
                   "border": f"1px solid {BORDER_CLR}", "padding": "24px"}
        )

    return html.Div([
        html.Div([
            html.P("ANALYSE DÉTAILLÉE",
                   style={"color": RED, "letterSpacing": "4px",
                          "fontSize": "11px", "fontWeight": "700", "marginBottom": "8px"}),
            html.H2("Comprendre les facteurs d'accidents",
                    style={"color": WHITE, "fontSize": "36px",
                           "fontWeight": "900", "margin": "0 0 40px"}),
        ], style={"padding": "40px 40px 0"}),

        html.Div([
            html.Div([_card(fig_pie), _card(fig_route)],
                     style={"display": "grid", "gridTemplateColumns": "1fr 2fr",
                            "gap": "24px", "marginBottom": "24px"}),
            html.Div([_card(fig_atm), _card(fig_vma)],
                     style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px"}),
        ], style={"padding": "0 40px 40px"}),
    ], style={"background": DARK_BG, "color": WHITE})