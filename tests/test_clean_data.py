"""Tests unitaires pour les fonctions de nettoyage des donnees."""
import pandas as pd
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.utils.clean_data import clean_caract, clean_lieux, clean_usagers
from src.utils.common_functions import filter_df, get_dept_options


# --- Fixtures ---

@pytest.fixture
def sample_caract() -> pd.DataFrame:
    """DataFrame minimal simulant caract-2024.csv."""
    return pd.DataFrame({
        "Num_Acc": ["ACC001", "ACC002", "ACC003"],
        "lat":  ["48,8566", "43,2965", "99,0000"],  # 3e hors France
        "long": ["2,3522",  "5,3698",  "200,0000"],
        "an":   [2024, 2024, 2024],
        "mois": [1, 6, 3],
        "jour": [15, 20, 10],
        "dep":  ["75", "13", "99"],
        "agg":  [1, 2, 1],
        "atm":  [1, 2, 5],
        "lum":  [1, 3, 2],
    })


@pytest.fixture
def sample_lieux() -> pd.DataFrame:
    """DataFrame minimal simulant lieux-2024.csv."""
    return pd.DataFrame({
        "Num_Acc": ["ACC001", "ACC002"],
        "catr": [1, 3],
        "vma":  [130, 50],
        "surf": [1, 2],
    })


@pytest.fixture
def sample_usagers() -> pd.DataFrame:
    """DataFrame minimal simulant usagers-2024.csv."""
    return pd.DataFrame({
        "Num_Acc":    ["ACC001", "ACC001", "ACC002"],
        "grav":       [2, 4, 3],  # ACC001 : gravite max = 2 (tue)
        "id_usager":  [1, 2, 3],
    })


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """DataFrame minimal pour tester les fonctions de filtrage."""
    return pd.DataFrame({
        "dep":  ["75", "75", "13", "33"],
        "grav": [2, 4, 3, 2],
        "lat":  [48.8, 48.9, 43.2, 44.8],
        "long": [2.3,  2.4,  5.3,  0.5],
    })


# --- Tests clean_caract ---

def test_clean_caract_filtre_coordonnees(sample_caract: pd.DataFrame) -> None:
    """Verifie que les coordonnees hors France sont supprimees."""
    result = clean_caract(sample_caract)
    assert len(result) == 2  # ACC003 doit etre supprime


def test_clean_caract_colonnes(sample_caract: pd.DataFrame) -> None:
    """Verifie que les colonnes attendues sont presentes."""
    result = clean_caract(sample_caract)
    colonnes_attendues = ["Num_Acc", "lat", "long", "date", "mois",
                          "mois_nom", "dep", "atm_label", "lum_label"]
    for col in colonnes_attendues:
        assert col in result.columns, f"Colonne manquante : {col}"


def test_clean_caract_date(sample_caract: pd.DataFrame) -> None:
    """Verifie que la colonne date est bien construite."""
    result = clean_caract(sample_caract)
    assert pd.api.types.is_datetime64_any_dtype(result["date"])


def test_clean_caract_atm_label(sample_caract: pd.DataFrame) -> None:
    """Verifie que les labels meteo sont bien assignes."""
    result = clean_caract(sample_caract)
    assert "Normale" in result["atm_label"].values


# --- Tests clean_lieux ---

def test_clean_lieux_colonnes(sample_lieux: pd.DataFrame) -> None:
    """Verifie que les colonnes attendues sont presentes."""
    result = clean_lieux(sample_lieux)
    for col in ["Num_Acc", "catr_label", "vma"]:
        assert col in result.columns


def test_clean_lieux_catr_label(sample_lieux: pd.DataFrame) -> None:
    """Verifie que les labels de type de route sont corrects."""
    result = clean_lieux(sample_lieux)
    assert "Autoroute" in result["catr_label"].values


# --- Tests clean_usagers ---

def test_clean_usagers_gravite_max(sample_usagers: pd.DataFrame) -> None:
    """Verifie que la gravite la plus severe est retenue par accident."""
    result = clean_usagers(sample_usagers)
    acc001 = result[result["Num_Acc"] == "ACC001"]
    assert acc001["grav"].values[0] == 2  # min = plus grave


def test_clean_usagers_nb_usagers(sample_usagers: pd.DataFrame) -> None:
    """Verifie que le nombre d'usagers par accident est correct."""
    result = clean_usagers(sample_usagers)
    acc001 = result[result["Num_Acc"] == "ACC001"]
    assert acc001["nb_usagers"].values[0] == 2


# --- Tests filter_df ---

def test_filter_df_par_departement(sample_df: pd.DataFrame) -> None:
    """Verifie le filtre par departement."""
    result = filter_df(sample_df, "75", 0)
    assert len(result) == 2
    assert all(result["dep"] == "75")


def test_filter_df_par_gravite(sample_df: pd.DataFrame) -> None:
    """Verifie le filtre par gravite."""
    result = filter_df(sample_df, "Tous", 2)
    assert all(result["grav"] == 2)


def test_filter_df_tous(sample_df: pd.DataFrame) -> None:
    """Verifie qu'aucun filtre retourne tout le dataset."""
    result = filter_df(sample_df, "Tous", 0)
    assert len(result) == len(sample_df)


# --- Tests get_dept_options ---

def test_get_dept_options_contient_tous(sample_df: pd.DataFrame) -> None:
    """Verifie que l'option 'Tous' est presente en premier."""
    options = get_dept_options(sample_df)
    assert options[0]["value"] == "Tous"


def test_get_dept_options_nb_departements(sample_df: pd.DataFrame) -> None:
    """Verifie le nombre d'options retournees."""
    options = get_dept_options(sample_df)
    assert len(options) == 4  # "Tous" + 3 departements uniques