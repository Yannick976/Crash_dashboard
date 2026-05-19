import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_CLEANED = os.path.join(BASE_DIR, "data", "cleaned")

CARACT_FILE  = os.path.join(DATA_RAW, "caract-2024.csv")
LIEUX_FILE   = os.path.join(DATA_RAW, "lieux-2024.csv")
USAGERS_FILE = os.path.join(DATA_RAW, "usagers-2024.csv")
CLEANED_FILE = os.path.join(DATA_CLEANED, "accidents_clean.csv")

APP_TITLE = "Accidentologie France 2024"
APP_PORT  = 8050
DEBUG     = False