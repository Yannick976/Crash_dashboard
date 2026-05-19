import pandas as pd


def filter_df(df: pd.DataFrame, dep: str | None, gravite: int | None) -> pd.DataFrame:
    """Filtre le dataframe selon departement et gravite.

    Args:
        df (pd.DataFrame): Dataset complet.
        dep (str | None): Code departement ou "Tous".
        gravite (int | None): Code gravite (2,3,4) ou 0 pour toutes.

    Returns:
        pd.DataFrame: Dataset filtre.
    """
    if dep and dep != "Tous":
        df = df[df["dep"].astype(str) == str(dep)]
    if gravite is not None and gravite != 0:
        df = df[df["grav"] == gravite]
    return df


def get_dept_options(df: pd.DataFrame) -> list[dict]:
    """Retourne la liste des departements pour un Dropdown Dash.

    Args:
        df (pd.DataFrame): Dataset contenant la colonne 'dep'.

    Returns:
        list[dict]: Liste d'options {label, value} pour dcc.Dropdown.
    """
    deps = sorted(df["dep"].dropna().astype(str).unique())
    return [{"label": "Tous les departements", "value": "Tous"}] + [
        {"label": d, "value": d} for d in deps
    ]