#  Web Scraper - Books to Scrape

Un scraper Python complet pour extraire les données du site [Books to Scrape](http://books.toscrape.com/).

##  Fonctionnalités

- **Scraping complet** : Titre, prix, description, disponibilité, note, catégorie
- **Téléchargement d'images** : Organisation automatique par catégories
- **Export CSV** : Fichiers séparés par catégorie
- **Interface flexible** : Scraping par catégorie, aléatoire ou complet
- **Analyse intégrée** : Notebook Jupyter pour l'analyse des données

##  Installation

```bash
# Installer les dépendances
pip install requests beautifulsoup4 pandas matplotlib jupyter
 Utilisation
Scraping complet
bash
python scrape.py
Scraping par catégorie
bash
# Lister toutes les catégories
python scrape_select.py --list

# Scraper des catégories spécifiques
python scrape_select.py Travel
python scrape_select.py Travel Mystery

# Scraper 3 catégories aléatoires
python scrape_select.py --random 3

# Scraper toutes les catégories
python scrape_select.py --all
Analyse des données
bash
jupyter notebook analysis.ipynb
Données extraites
Colonne	Description
title	Titre du livre
price	Prix
availability	Disponibilité
description	Description
category	Catégorie
rating	Note
image_url	URL de l'image

 Structure
text
projet-python-1/
├── scrape.py              # Script principal
├── scrape_select.py       # Sélection par catégorie
├── parsers.py             # Extraction des données
├── utils.py               # Utilitaires
├── settings.py            # Configuration
├── analysis.ipynb         # Analyse des données
└── test_outputs/          # Données générées
    ├── csv/
    └── images/

Résultats

Exemple de statistiques pour la catégorie Travel :

11 livres scrapés

Prix moyen : £39.79

Distribution des notes analysée

Visualisations matplotlib

 Test rapide

# Tester avec une catégorie
python scrape_select.py Travel

# Vérifier les résultats
ls -la test_outputs/