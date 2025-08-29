"""
Ce script Python génère une arborescence visuelle d'un répertoire.

Il parcourt récursivement le répertoire spécifié et imprime les dossiers et les fichiers
dans une structure arborescente, similaire à la commande `tree` sous Linux.
Les fichiers et dossiers spécifiés dans les ensembles de configuration sont ignorés.
"""

# Importe le module 'os' pour interagir avec le système d'exploitation.
import os

# --- Configuration ---
# Add any other directories or files you want to ignore to this set.
IGNORE_SET = {'.git', '.idea', '__pycache__', '.pytest_cache', '.vscode', '.venv', 'venv'}
IGNORE_EXTENSIONS = {'.pyc'}


def print_tree(directory, prefix=''):
    """
    Imprime de manière récursive une arborescence visuelle d'un répertoire.

    Args:
        directory (str): Le chemin absolu du répertoire à parcourir.
        prefix (str): Le préfixe à utiliser pour les lignes d'impression,
                      utilisé pour l'indentation et les connecteurs d'arborescence.
    """
    try:
        # Tente d'obtenir la liste des entrées dans le répertoire,
        # en filtrant les éléments à ignorer et en triant le résultat.
        entries = sorted([e for e in os.listdir(directory) if e not in IGNORE_SET])
    except FileNotFoundError:
        # Si le répertoire n'est pas trouvé, imprime un message d'erreur et arrête.
        print(f"Erreur : Répertoire non trouvé à {directory}")
        # Quitte la fonction si le répertoire n'existe pas.
        return

    # Itère sur chaque entrée (fichier ou dossier) du répertoire.
    for i, entry in enumerate(entries):
        # Construit le chemin complet de l'entrée.
        full_path = os.path.join(directory, entry)
        # Détermine si c'est la dernière entrée de la liste pour utiliser le bon connecteur.
        is_last = (i == len(entries) - 1)
        # Choisit le connecteur d'arborescence : '└── ' pour le dernier, '├── ' pour les autres.
        connector = '└── ' if is_last else '├── '

        # Vérifie si le chemin complet correspond à un répertoire.
        if os.path.isdir(full_path):
            # Si c'est un répertoire, imprime son nom avec une barre oblique.
            print(prefix + connector + entry + '/')
            # Calcule le nouveau préfixe pour le niveau suivant de l'arborescence.
            new_prefix = prefix + ('    ' if is_last else '│   ')
            # Appelle récursivement la fonction pour ce sous-répertoire.
            print_tree(full_path, new_prefix)
        else:
            # Si c'est un fichier, vérifie si son extension doit être ignorée.
            if os.path.splitext(entry)[1] not in IGNORE_EXTENSIONS:
                # Si l'extension n'est pas ignorée, imprime le nom du fichier.
                print(prefix + connector + entry)


# Vérifie si le script est exécuté directement (et non importé).
if __name__ == '__main__':
    # Définit le chemin de départ comme étant le répertoire où se trouve le script.
    start_path = os.path.dirname(os.path.abspath(__file__))

    # Imprime le chemin absolu du répertoire de départ.
    print(f'{os.path.abspath(start_path)}')
    # Appelle la fonction principale pour imprimer l'arborescence à partir du chemin de départ.
    print_tree(start_path)
