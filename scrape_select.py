import sys
import random
from scrape import *

def get_categories():
    """Récupère toutes les catégories du site."""
    soup = get_soup("http://books.toscrape.com/")
    menu = soup.find("ul", class_="nav nav-list").find("ul")
    
    cats = []
    for li in menu.find_all("li"):
        name = li.text.strip()
        url = "http://books.toscrape.com/" + li.find("a")["href"]
        cats.append({"name": name, "url": url})
    
    return cats


def scrape_category(cat_url, cat_name):
    """Scrape une catégorie."""
    print(f"\n {cat_name}")
    print("="*50)
    
    page = 1
    total = 0
    
    while True:
        url = cat_url if page == 1 else cat_url.replace("index.html", f"page-{page}.html")
        
        try:
            links = get_book_links(get_soup(url), "http://books.toscrape.com/")
            if not links:
                break
            
            print(f"  Page {page}: {len(links)} livres", end=" ")
            
            for link in links:
                if scrape_book(link):
                    total += 1
            
            print(f"→ Total: {total}")
            page += 1
        except:
            break
    
    print(f" {cat_name}: {total} livres\n")
    return total


def main():
    """Menu principal."""
    
    # Aide
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("""

    # SCRAPER PAR CATÉGORIE                  

USAGE:
  python scrape_select.py --list          # Liste les catégories
  python scrape_select.py Travel          # Scrape Travel
  python scrape_select.py Travel Mystery  # Scrape 2 catégories
  python scrape_select.py --random 3      # 3 catégories au hasard
  python scrape_select.py --all           # Toutes les catégories


""")
        return
    
    # Récupère les catégories
    print(" Chargement des catégories...")
    all_cats = get_categories()
    print(f" {len(all_cats)} catégories trouvées\n")
    
    # --list : affiche toutes les catégories
    if sys.argv[1] == "--list":
        print(" CATÉGORIES DISPONIBLES:\n")
        for i, cat in enumerate(all_cats, 1):
            print(f"  {i:2d}. {cat['name']}")
        print()
        return
    
    # --random N : N catégories aléatoires
    if sys.argv[1] == "--random":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        selected = random.sample(all_cats, min(n, len(all_cats)))
        to_scrape = selected
        print(f" {n} catégories aléatoires:")
        for cat in to_scrape:
            print(f"   {cat['name']}")
    
    # --all : toutes les catégories
    elif sys.argv[1] == "--all":
        to_scrape = all_cats
        print(f" TOUTES les catégories ({len(to_scrape)})")
    
    # Catégories spécifiques
    else:
        names = sys.argv[1:]
        to_scrape = [c for c in all_cats if c["name"].lower() in [n.lower() for n in names]]
        
        if not to_scrape:
            print(f" Aucune catégorie trouvée!")
            print(f" Utilisez --list pour voir les catégories")
            return
        
        print(f" {len(to_scrape)} catégorie(s):")
        for cat in to_scrape:
            print(f"   {cat['name']}")
    
    # Scraping
    print("\n" + "="*50)
    print(" DÉMARRAGE")
    print("="*50)
    
    total = 0
    for cat in to_scrape:
        total += scrape_category(cat["url"], cat["name"])
    
    # Résumé
    print("="*50)
    print(f" TERMINÉ: {total} livres | {len(to_scrape)} catégories")
    print("="*50)


if __name__ == "__main__":
    main()