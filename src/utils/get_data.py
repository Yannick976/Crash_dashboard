"""Telechargement des donnees brutes depuis data.gouv.fr"""
import os
import urllib.request
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config import DATA_RAW

URLS: dict[str, str] = {
    "caract-2024.csv":  "https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2023/20240924-083952/caract-2024.csv",
    "lieux-2024.csv":   "https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2023/20240924-083952/lieux-2024.csv",
    "usagers-2024.csv": "https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2023/20240924-083952/usagers-2024.csv",
}


def download_all() -> None:
    """Telecharge les fichiers CSV bruts si absents dans data/raw/.

    Returns:
        None
    """
    os.makedirs(DATA_RAW, exist_ok=True)
    for filename, url in URLS.items():
        dest = os.path.join(DATA_RAW, filename)
        if os.path.exists(dest):
            print(f"Deja present : {filename}")
            continue
        try:
            print(f"Telechargement : {filename}...")
            urllib.request.urlretrieve(url, dest)
            print(f"Sauvegarde : {dest}")
        except Exception as e:
            print(f"Erreur lors du telechargement de {filename} : {e}")
            raise


if __name__ == "__main__":
    download_all()