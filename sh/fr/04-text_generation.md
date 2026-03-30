# 4. Génération et écriture de texte

---

## 4.1 Pourquoi l'IA n'a pas besoin d'éditeur

Le flux de travail de la plupart des ingénieurs humains pour écrire du code :
1. Ouvrir l'éditeur (VS Code, Vim, Emacs...)
2. Taper le code
3. Enregistrer le fichier
4. Fermer l'éditeur

Pour l'IA :
```
"Écrire un programme Python" = générer du texte
"Enregistrer ce programme dans un fichier" = écrire du texte sur le disque
```

Le processus de génération de code de l'IA est un **processus de génération de texte**. Donc l'IA utilise les outils texte de Shell :

- `echo` : afficher une seule ligne de texte
- `printf` : sortie formatée
- `heredoc` : afficher du texte multi-lignes (le plus important !)

---

## 4.2 `echo` : La sortie la plus simple

### Utilisation basique

```bash
# Afficher une chaîne
echo "Bonjour, le monde !"

# Afficher une variable
nom="Alice"
echo "Bonjour, $nom !"

# Afficher plusieurs valeurs
echo "Aujourd'hui est $(date +%Y-%m-%d)"
```

### Pièges de `echo`

```bash
# echo ajoute un retour à la ligne par défaut
echo -n "Chargement : "  # Pas de retour à la ligne
```

### Écrire des fichiers avec `echo`

```bash
# Écraser
echo "Bonjour, le monde !" > fichier.txt

# Ajouter
echo "Deuxième ligne" >> fichier.txt
```

**Note** : Utiliser `echo` pour des fichiers multi-lignes est pénible, donc l'IA ne l'utilise presque jamais pour du code. `heredoc` est la star.

---

## 4.3 `printf` : Sortie formatée plus puissante

### Comparaison avec `echo`

```bash
# printf prend en charge le formatage style C
printf "Valeur : %.2f\n" 3.14159
# Sortie : Valeur : 3.14

printf "%s\t%s\n" "Nom" "Âge"
```

### Créer des tableaux

```bash
printf "%-15s %10s\n" "Nom" "Prix"
printf "%-15s %10.2f\n" "iPhone" 999.99
printf "%-15s %10.2f\n" "MacBook" 1999.99
```

---

## 4.4 heredoc : L'arme principale de l'IA pour écrire du code

### Qu'est-ce que heredoc ?

heredoc est une syntaxe Shell spéciale pour **afficher du texte multi-lignes verbatim**.

```bash
cat << 'EOF'
Tout ce contenu
sera affiché verbatim
y compris les retours à la ligne, les espaces
EOF
```

### Écrire des fichiers (utilisation la plus courante de l'IA)

```bash
cat > programme.py << 'EOF'
#!/usr/bin/env python3

def hello(nom):
    print(f"Bonjour, {nom} !")

if __name__ == "__main__":
    hello("Monde")
EOF
```

### Pourquoi utiliser `'EOF'` (guillemet simple) ?

```bash
# Guillemet simple EOF : ne développer rien
cat << 'EOF'
HOME est : $HOME
Aujourd'hui est : $(date)
EOF
# Sortie : HOME est : $HOME (non développé)

# Guillemet double EOF ou pas de guillemets : développera
cat << EOF
HOME est : $HOME
EOF
# Sortie : HOME est : /home/ai (développé)
```

**Choix de l'IA** : presque toujours utiliser `'EOF'` (guillemet simple). Parce que le code n'a généralement pas besoin de développement de variable Shell.

---

## 4.5 L'IA écrit divers fichiers avec heredoc

### Écrire un programme Python

```bash
cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""Point d'entrée principal"""

import sys
import os

def main():
    print("Projet hybride Python + C")
    print(f"Répertoire de travail : {os.getcwd()}")

if __name__ == "__main__":
    main()
EOF
```

### Écrire un script Shell

```bash
cat > scripts/deploy.sh << 'EOF'
#!/bin/bash
set -e

DEPLOY_HOST="serveur.exemple.com"

echo "🚀 Déploiement vers $DEPLOY_HOST"
rsync -avz --delete ./dist/ "$DEPLOY_HOST:/var/www/app/"
ssh "$DEPLOY_HOST" "systemctl restart myapp"
echo "✅ Déploiement terminé !"
EOF

chmod +x scripts/deploy.sh
```

### Écrire un fichier de configuration

```bash
cat > config.json << 'EOF'
{
    "nom_du_site": "Mon Blog",
    "auteur": "Anonyme",
    "thème": "minimal"
}
EOF
```

### Écrire un Dockerfile

```bash
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "http.server", "8000"]
EOF
```

---

## 4.6 Pièges de heredoc et solutions

### Piège 1 : Contient des guillemets simples

```bash
# Problème : guillemet simple EOF ne permet pas les guillemets simples
cat << 'EOF'
Il va.
EOF
# Sortie : erreur de syntaxe

# Solution : utiliser guillemet double EOF
cat << "EOF"
Il va.
EOF
```

### Piège 2 : Contient `$` (mais ne veut pas de développement)

```bash
# Problème : guillemet double EOF développe $
cat << "EOF"
Le prix est $100
EOF
# Sortie : Le prix est (vide)

# Solution : échapper individuellement
cat << "EOF"
Le prix est $$100
EOF
# Sortie : Le prix est $100
```

---

## 4.7 Pratique : Construire un projet complet de zéro

```bash
# 1. Créer la structure de répertoires
mkdir -p monblog/{src,themes,content}

# 2. Créer le fichier de configuration
cat > monblog/config.json << 'EOF'
{
    "nom_du_site": "Mon Blog",
    "auteur": "Anonyme",
    "thème": "minimal"
}
EOF

# 3. Créer le programme principal Python
cat > monblog/src/blog.py << 'EOF'
#!/usr/bin/env python3
"""Générateur de blog simple"""
import json
from pathlib import Path

def charger_config():
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path) as f:
        return json.load(f)

if __name__ == "__main__":
    config = charger_config()
    print(f"Génération : {config['nom_du_site']}")
EOF

# 4. Créer le script de compilation
cat > monblog/build.sh << 'EOF'
#!/bin/bash
set -e
echo "🔨 Construction du blog..."
cd "$(dirname "$0")"
python3 src/blog.py
echo "✅ Construction terminée !"
EOF

chmod +x monblog/build.sh

# 5. Vérifier la structure
find monblog -type f | sort
```

---

## 4.8 Référence rapide

| Outil | Purpose | Exemple |
|------|---------|---------|
| `echo` | Afficher une seule ligne | `echo "Bonjour"` |
| `echo -n` | Pas de retour à la ligne | `echo -n "Chargement..."` |
| `printf` | Sortie formatée | `printf "%s : %d\n" "âge" 25` |
| `>` | Écraser le fichier | `echo "salut" > fichier.txt` |
| `>>` | Ajouter au fichier | `echo "salut" >> fichier.txt` |
| `<< 'EOF'` | heredoc (pas de développement) | préféré pour le code |
| `<< "EOF"` | heredoc (développer) | rarement utilisé |

---

## 4.9 Exercices

1. Créer une animation de chargement avec `echo -n` et une boucle `for`
2. Créer un tableau formaté (nom, âge, métier) avec `printf`
3. Écrire un programme Python de 20 lignes avec heredoc
4. Écrire un docker-compose.yml avec heredoc
