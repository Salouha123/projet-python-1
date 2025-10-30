import os

# URL de base du site
BASE_URL = "http://books.toscrape.com/"

# Répertoires de sortie
OUTPUT_DIR = "test_outputs"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
CSV_DIR = os.path.join(OUTPUT_DIR, "csv")

# Nom du fichier CSV
CSV_FILENAME = os.path.join(CSV_DIR, "books.csv")

# Délai entre les requêtes pour éviter de surcharger le serveur
REQUEST_SLEEP = 1
