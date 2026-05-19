import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config import CARACT_FILE, LIEUX_FILE, USAGERS_FILE, CLEANED_FILE

GRAVITE_LABELS: dict[int, str] = {1: "Indemne", 2: "Tue", 3: "Blesse hospitalise", 4: "Blesse leger"}
ATM_LABELS: dict[int, str] = {
    1: "Normale", 2: "Pluie legere", 3: "Pluie forte", 4: "Neige/grele",
    5: "Brouillard", 6: "Vent fort", 7: "Temps eblouissant", 8: "Temps couvert", 9: "Autre"
}
CATR_LABELS: dict[int, str] = {
    1: "Autoroute", 2: "Route nat.", 3: "Route dep.", 4: "Voie commun.",
    5: "Hors reseau", 6: "Parking", 7: "Voie urbaine", 9: "Autre"
}
LUM_LABELS: dict[int, str] = {
    1: "Plein jour", 2: "Crepuscule", 3: "Nuit sans eclairage",
    4: "Nuit eclairage eteint", 5: "Nuit eclairage allume"
}
MOIS_MAP: dict[int, str] = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Avr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Aou", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}


def load_raw() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Charge les 3 fichiers CSV bruts depuis data/raw/.

    Returns:
        tuple: (caract, lieux, usagers) en tant que DataFrames pandas.

    Raises:
        FileNotFoundError: si un fichier CSV est absent.
    """
    for path in [CARACT_FILE, LIEUX_FILE, USAGERS_FILE]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fichier introuvable : {path}")
    caract  = pd.read_csv(CARACT_FILE,  sep=";", encoding="utf-8", low_memory=False)
    lieux   = pd.read_csv(LIEUX_FILE,   sep=";", encoding="utf-8", low_memory=False)
    usagers = pd.read_csv(USAGERS_FILE, sep=";", encoding="utf-8", low_memory=False)
    return caract, lieux, usagers


def clean_caract(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie le fichier caracteristiques : coordonnees GPS, date, labels.

    Args:
        df (pd.DataFrame): DataFrame brut du fichier caract-2024.csv.

    Returns:
        pd.DataFrame: DataFrame nettoye avec colonnes utiles.
    """
    df = df.copy()
    df["lat"]  = df["lat"].astype(str).str.replace(",", ".").pipe(pd.to_numeric, errors="coerce")
    df["long"] = df["long"].astype(str).str.replace(",", ".").pipe(pd.to_numeric, errors="coerce")
    # Filtre France metropolitaine uniquement
    df = df[(df["lat"].between(41.0, 51.5)) & (df["long"].between(-5.5, 10.0))]
    df["date"] = pd.to_datetime(
        df["an"].astype(str) + "-" +
        df["mois"].astype(str).str.zfill(2) + "-" +
        df["jour"].astype(str).str.zfill(2),
        errors="coerce"
    )
    df["mois_nom"]  = df["mois"].map(MOIS_MAP)
    df["atm_label"] = df["atm"].map(ATM_LABELS).fillna("Inconnu")
    df["lum_label"] = df["lum"].map(LUM_LABELS).fillna("Inconnu")
    return df[["Num_Acc", "lat", "long", "date", "mois", "mois_nom",
               "dep", "agg", "atm", "atm_label", "lum", "lum_label"]]


def clean_lieux(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie le fichier lieux : type de route et vitesse maximale.

    Args:
        df (pd.DataFrame): DataFrame brut du fichier lieux-2024.csv.

    Returns:
        pd.DataFrame: DataFrame nettoye avec colonnes utiles.
    """
    df = df.copy()
    df["catr_label"] = df["catr"].map(CATR_LABELS).fillna("Autre")
    df["vma"] = pd.to_numeric(df["vma"], errors="coerce")
    return df[["Num_Acc", "catr", "catr_label", "vma", "surf"]]


def clean_usagers(df: pd.DataFrame) -> pd.DataFrame:
    """Agregat par accident : gravite maximale et nombre d'usagers impliques.

    La gravite la plus severe est retenue (valeur numerique minimale = plus grave).

    Args:
        df (pd.DataFrame): DataFrame brut du fichier usagers-2024.csv.

    Returns:
        pd.DataFrame: Une ligne par accident avec grav, grav_label, nb_usagers.
    """
    df = df.copy()
    df["grav"] = pd.to_numeric(df["grav"], errors="coerce")
    grav_max = df.groupby("Num_Acc")["grav"].min().reset_index()
    grav_max["grav_label"] = grav_max["grav"].map(GRAVITE_LABELS).fillna("Inconnu")
    nb_vic = df.groupby("Num_Acc").size().reset_index(name="nb_usagers")
    return grav_max.merge(nb_vic, on="Num_Acc")


def build_clean_dataset() -> pd.DataFrame:
    """Fusionne les 3 sources nettoyees et sauvegarde le resultat.

    Returns:
        pd.DataFrame: Dataset fusionne et nettoye.

    Raises:
        Exception: si une erreur survient pendant le nettoyage.
    """
    try:
        print("Chargement des donnees brutes...")
        caract, lieux, usagers = load_raw()
        print("Nettoyage en cours...")
        df = clean_caract(caract)
        df = df.merge(clean_lieux(lieux),    on="Num_Acc", how="left")
        df = df.merge(clean_usagers(usagers), on="Num_Acc", how="left")
        os.makedirs(os.path.dirname(CLEANED_FILE), exist_ok=True)
        df.to_csv(CLEANED_FILE, index=False)
        print(f"OK {len(df)} accidents sauvegardes dans {CLEANED_FILE}")
        return df
    except Exception as e:
        print(f"Erreur pendant le nettoyage : {e}")
        raise


def load_clean() -> pd.DataFrame:
    """Charge le dataset nettoye, le construit si absent.

    Returns:
        pd.DataFrame: Dataset pret pour le dashboard.
    """
    if not os.path.exists(CLEANED_FILE):
        return build_clean_dataset()
    return pd.read_csv(CLEANED_FILE, parse_dates=["date"], low_memory=False)