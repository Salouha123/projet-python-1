from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_book_links(soup, base_url):
    """
    Récupère tous les liens des livres sur une page.
    """
    links = []
    for article in soup.find_all("article", class_="product_pod"):
        href = article.h3.a["href"]
        # Corrige les chemins relatifs (souvent "../../../")
        href = href.replace("../../../", "catalogue/")
        full_link = urljoin(base_url, href)
        links.append(full_link)
    return links


def parse_book_info(soup):
    """
    Extrait toutes les informations d'un livre à partir de sa page détaillée.
    """
    book = {}

    # --- Titre ---
    title_tag = soup.find("h1")
    book["title"] = title_tag.text.strip() if title_tag else "N/A"

    # --- Prix ---
    price_tag = soup.find("p", class_="price_color")
    book["price"] = price_tag.text.strip() if price_tag else "N/A"

    # --- Disponibilité ---
    stock_tag = soup.find("p", class_="instock availability")
    book["availability"] = stock_tag.text.strip() if stock_tag else "N/A"

    # --- Description ---
    desc_tag = soup.find("div", id="product_description")
    if desc_tag and desc_tag.find_next_sibling("p"):
        book["description"] = desc_tag.find_next_sibling("p").text.strip()
    else:
        book["description"] = "N/A"

    # --- Catégorie ---
    category_tag = soup.find("ul", class_="breadcrumb").find_all("li")[2].a
    book["category"] = category_tag.text.strip() if category_tag else "N/A"

    # --- Note (1 à 5 étoiles) ---
    rating_tag = soup.find("p", class_="star-rating")
    if rating_tag:
        rating_classes = rating_tag.get("class", [])
        possible_ratings = ["One", "Two", "Three", "Four", "Five"]
        rating = next((r for r in possible_ratings if r in rating_classes), "N/A")
        book["rating"] = rating
    else:
        book["rating"] = "N/A"

    # --- Image ---
    image_tag = soup.find("img")
    if image_tag and "src" in image_tag.attrs:
        image_url = image_tag["src"].replace("../../", "")
        book["image_url"] = urljoin("http://books.toscrape.com/", image_url)
    else:
        book["image_url"] = None

    return book
