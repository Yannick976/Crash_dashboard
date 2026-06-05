"""Page d'accueil : deux cartes de navigation avec mini-visualisations."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from src.utils.common_functions import GRAVITY_COLORS

DARK_BG    = "#0d0d0d"
CARD_BG    = "#141414"
BORDER_CLR = "#2a2a2a"
RED        = "#ff4444"
MUTED      = "#888888"
WHITE      = "#f0f0f0"


def _mini_map(df: pd.DataFrame) -> go.Figure:
    """Mini scatter mapbox avec un échantillon de points colorés."""
    sample = df[["lat", "long", "grav_label"]].dropna().sample(
        min(3000, len(df)), random_state=42
    )
    # Ordre gravité pour la légende
    order = ["Indemne", "Blesse leger", "Blesse hospitalise", "Tue"]
    sample["grav_label"] = pd.Categorical(sample["grav_label"], categories=order, ordered=True)
    sample = sample.sort_values("grav_label")

    fig = px.scatter_mapbox(
        sample, lat="lat", lon="long",
        color="grav_label",
        color_discrete_map=GRAVITY_COLORS,
        zoom=4.2, center={"lat": 46.8, "lon": 2.3},
        mapbox_style="carto-darkmatter",
        opacity=0.7,
    )
    fig.update_traces(marker=dict(size=4))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=280,
        showlegend=False,
        uirevision="static",
    )
    return fig


def _mini_donut(df: pd.DataFrame) -> go.Figure:
    """Mini donut chart de répartition par gravité."""
    grav = df["grav_label"].value_counts().reset_index()
    grav.columns = ["grav_label", "count"]

    order = ["Indemne", "Blesse leger", "Blesse hospitalise", "Tue"]
    grav["grav_label"] = pd.Categorical(grav["grav_label"], categories=order, ordered=True)
    grav = grav.sort_values("grav_label")

    fig = go.Figure(go.Pie(
        labels=grav["grav_label"],
        values=grav["count"],
        hole=0.65,
        marker=dict(
            colors=[GRAVITY_COLORS.get(l, "#555555") for l in grav["grav_label"]],
            line=dict(color="#0d0d0d", width=2),
        ),
        hovertemplate="<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>",
        textinfo="none",
    ))
    total = len(df)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=280,
        showlegend=True,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=WHITE, size=11),
            orientation="v",
            x=0.62, y=0.5,
        ),
        annotations=[dict(
            text=f"<b>{total:,}</b><br><span style='font-size:11px'>accidents</span>",
            x=0.27, y=0.5,
            font=dict(size=16, color=WHITE),
            showarrow=False,
        )],
    )
    return fig


def _nav_card(
    title: str,
    subtitle: str,
    tag: str,
    href: str,
    figure: go.Figure,
    accent: str = RED,
) -> html.Div:
    """Carte de navigation avec mini-visualisation en haut."""
    return html.A(href=href, style={"textDecoration": "none"}, children=[
        html.Div([
            # Mini visualisation
            dcc.Graph(
                figure=figure,
                config={"displayModeBar": False, "scrollZoom": False},
                style={"borderRadius": "4px 4px 0 0", "overflow": "hidden"},
            ),
            # Texte bas de carte
            html.Div([
                html.P(tag, style={
                    "color": accent, "letterSpacing": "3px",
                    "fontSize": "10px", "fontWeight": "700",
                    "marginBottom": "6px", "margin": "0 0 6px",
                }),
                html.H3(title, style={
                    "color": WHITE, "fontSize": "22px",
                    "fontWeight": "900", "margin": "0 0 8px",
                }),
                html.P(subtitle, style={
                    "color": MUTED, "fontSize": "13px",
                    "margin": "0 0 20px", "lineHeight": "1.5",
                }),
                html.Div("Explorer →", style={
                    "color": accent, "fontSize": "13px",
                    "fontWeight": "700", "letterSpacing": "1px",
                }),
            ], style={"padding": "20px 24px 24px"}),
        ], style={
            "background": CARD_BG,
            "border": f"1px solid {BORDER_CLR}",
            "borderTop": f"3px solid {accent}",
            "borderRadius": "4px",
            "overflow": "hidden",
            "transition": "border-color 0.2s",
            "cursor": "pointer",
        }),
    ])


def layout(df: pd.DataFrame) -> html.Div:
    """Retourne le layout de la page d'accueil."""

    nb_accidents = len(df)
    nb_tues = int((df["grav_label"] == "Tue").sum())
    nb_departements = df["dep"].nunique()
    nb_communes = df["com"].nunique()

    return html.Div([
        # En-tête
        html.Div([
            html.P(
                "CRASH DASHBOARD · FRANCE 2024",
                style={
                    "color": RED,
                    "letterSpacing": "4px",
                    "fontSize": "11px",
                    "fontWeight": "700",
                    "marginBottom": "16px",
                },
            ),

            html.H1(
                "Accidents de la route",
                style={
                    "color": WHITE,
                    "fontSize": "52px",
                    "fontWeight": "900",
                    "margin": "0",
                    "lineHeight": "1",
                },
            ),

            html.H1(
                "en France",
                style={
                    "color": MUTED,
                    "fontSize": "52px",
                    "fontWeight": "900",
                    "margin": "0 0 16px",
                    "lineHeight": "1",
                },
            ),

            html.P(
                f"{nb_accidents:,} accidents recensés · {nb_tues:,} personnes tuées",
                style={
                    "color": MUTED,
                    "fontSize": "15px",
                    "margin": "0 0 48px",
                },
            ),
        ], style={"padding": "60px 40px 0"}),

        # Cartes KPI
        html.Div([
            html.Div([
                html.H2(f"{nb_accidents:,}", style={"color": WHITE, "margin": "0"}),
                html.P("Accidents", style={"color": MUTED, "margin": "0"}),
            ], style={
                "background": CARD_BG,
                "border": f"1px solid {BORDER_CLR}",
                "padding": "20px",
                "borderRadius": "8px",
                "textAlign": "center",
            }),

            html.Div([
                html.H2(f"{nb_tues:,}", style={"color": RED, "margin": "0"}),
                html.P("Personnes tuées", style={"color": MUTED, "margin": "0"}),
            ], style={
                "background": CARD_BG,
                "border": f"1px solid {BORDER_CLR}",
                "padding": "20px",
                "borderRadius": "8px",
                "textAlign": "center",
            }),

            html.Div([
                html.H2(f"{nb_departements}", style={"color": WHITE, "margin": "0"}),
                html.P("Départements", style={"color": MUTED, "margin": "0"}),
            ], style={
                "background": CARD_BG,
                "border": f"1px solid {BORDER_CLR}",
                "padding": "20px",
                "borderRadius": "8px",
                "textAlign": "center",
            }),

            html.Div([
                html.H2(f"{nb_communes:,}", style={"color": WHITE, "margin": "0"}),
                html.P("Communes", style={"color": MUTED, "margin": "0"}),
            ], style={
                "background": CARD_BG,
                "border": f"1px solid {BORDER_CLR}",
                "padding": "20px",
                "borderRadius": "8px",
                "textAlign": "center",
            }),
        ], style={
            "display": "grid",
            "gridTemplateColumns": "repeat(4, 1fr)",
            "gap": "20px",
            "padding": "0 40px 50px",
        }),

        # Deux cartes de navigation
        html.Div([
            _nav_card(
                title="Carte des accidents",
                subtitle="Visualisez la localisation géographique de chaque accident, filtrez par gravité et département.",
                tag="GÉOGRAPHIE",
                href="/carte",
                figure=_mini_map(df),
                accent="#4fc3f7",
            ),
            _nav_card(
                title="Analyse statistique",
                subtitle="Explorez les facteurs d'accidents : météo, type de route, vitesse, répartition des victimes.",
                tag="STATISTIQUES",
                href="/analyse",
                figure=_mini_donut(df),
                accent=RED,
            ),
        ], style={
            "display": "grid",
            "gridTemplateColumns": "1fr 1fr",
            "gap": "24px",
            "padding": "0 40px 60px",
        }),
    ], style={
        "background": DARK_BG,
        "color": WHITE,
        "minHeight": "100vh",
    })
    