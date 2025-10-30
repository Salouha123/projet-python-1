import os
import requests
from bs4 import BeautifulSoup
import csv

from utils import sanitize_filename, get_category_paths
from parsers import parse_book_info, get_book_links

# Configuration
OUTPUT_DIR = "test_outputs"
BASE_URL = "http://books.toscrape.com/catalogue/"
CSV_FIELDNAMES = ["title", "price", "availability", "description", "category", "rating", "image_url"]

# Stockage des catégories initialisées
initialized_categories = set()


def get_soup(url):
    """Récupère et parse le HTML d'une URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def download_image(image_url, title, category):
    """Télécharge l'image dans le dossier de la catégorie."""
    try:
        images_dir, _ = get_category_paths(category, OUTPUT_DIR)
        filename = f"{sanitize_filename(title)}.jpg"
        filepath = os.path.join(images_dir, filename)
        
        if not os.path.exists(filepath):
            img_data = requests.get(image_url, timeout=10).content
            with open(filepath, "wb") as f:
                f.write(img_data)
            print(f"   Image : {category}/{filename}")
        return True
    except Exception as e:
        print(f"   Erreur image '{title}' : {e}")
        return False


def save_book(book_info):
    """Sauvegarde un livre dans le CSV de sa catégorie."""
    category = book_info.get("category", "Unknown")
    _, csv_file = get_category_paths(category, OUTPUT_DIR)
    
    # Initialiser le CSV si nécessaire
    if category not in initialized_categories:
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, CSV_FIELDNAMES).writeheader()
        initialized_categories.add(category)
        print(f"   Nouvelle catégorie : {category}")
    
    # Ajouter le livre
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, CSV_FIELDNAMES).writerow(book_info)
    
    print(f"   [{category}] {book_info['title']}")


def scrape_book(url):
    """Scrape un livre et sauvegarde ses données."""
    try:
        book_info = parse_book_info(get_soup(url))
        
        # Télécharger l'image
        if book_info.get("image_url"):
            download_image(book_info["image_url"], book_info["title"], book_info["category"])
        
        # Sauvegarder dans le CSV
        save_book(book_info)
        return book_info
        
    except Exception as e:
        print(f"   Erreur : {e}")
        return None


def scrape_all_books():
    """Scrape tous les livres du catalogue."""
    print("\n" + "="*60)
    print(" SCRAPING PAR CATÉGORIE")
    print("="*60 + "\n")
    
    page = 1
    total = 0
    stats = {}

    while True:
        url = f"{BASE_URL}page-{page}.html"
        print(f"\n Page {page}")
        
        try:
            soup = get_soup(url)
        except:
            break
        
        links = get_book_links(soup, BASE_URL)
        print(f"  → {len(links)} livres trouvés")
        
        for link in links:
            book = scrape_book(link)
            if book:
                total += 1
                cat = book.get("category", "Unknown")
                stats[cat] = stats.get(cat, 0) + 1
        
        page += 1
    
    # Résumé
    print("\n" + "="*60)
    print(f" TERMINÉ : {total} livres | {len(stats)} catégories")
    print("="*60)
    print("\n Par catégorie :")
    for cat, count in sorted(stats.items()):
        print("  • {cat}: {count}")
    print(f"\n Données : {OUTPUT_DIR}/")
    print("="*60 + "\n")


if __name__ == "__main__":
    scrape_all_books()