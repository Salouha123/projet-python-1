import os
import re


def ensure_directories(*dirs):
    """Crée les répertoires s'ils n'existent pas."""
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)


def sanitize_filename(filename):
    """Nettoie un nom de fichier pour tous les OS."""
    # Remplace les caractères interdits par des underscores
    clean = re.sub(r'[<>:"/\\|?*,]', '_', filename)
    
    # Remplace les espaces multiples par un seul
    clean = re.sub(r'\s+', ' ', clean)
    
    # Supprime les points et espaces en début/fin
    clean = clean.strip('. ')
    
    # Limite à 100 caractères (plus sûr que 200)
    if len(clean) > 100:
        clean = clean[:100].rsplit(' ', 1)[0]  # Coupe au dernier espace
    
    # Si vide après nettoyage, retourne un nom par défaut
    return clean if clean else "unnamed"


def get_category_paths(category, output_dir):
    """Retourne les chemins (images_dir, csv_file) pour une catégorie."""
    safe_cat = sanitize_filename(category)
    
    images_dir = os.path.join(output_dir, "images", safe_cat)
    csv_dir = os.path.join(output_dir, "csv", safe_cat)
    
    ensure_directories(images_dir, csv_dir)
    
    csv_file = os.path.join(csv_dir, f"{safe_cat}.csv")
    
    return images_dir, csv_file