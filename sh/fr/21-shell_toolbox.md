# 21. Construire Votre Boîte à Outils Shell IA

---

## 21.1 Pourquoi Vous Avez Besoin d'une Boîte à Outils

Quand vous vous surprenez à répéter la même chose, il est temps d'automatiser et de la regrouper dans une boîte à outils.

L'IA est particulièrement efficace pour :
- Créer rapidement des outils
- Envelopper des flux de travail complexes dans des commandes simples
- Améliorer continuellement les scripts couramment utilisés

---

## 21.2 Structure du Répertoire de la Boîte à Outils

```
~/bin/
├── lib/              # Bibliothèques partagées
│   ├── logging.sh
│   ├── utils.sh
│   └── colors.sh
├── project/          # Modèles de projet
│   ├── python/
│   ├── nodejs/
│   └── static-site/
├── scripts/          # Scripts d'outils
│   ├── git-clean
│   ├── docker-clean
│   ├── backup
│   └── log-parse
└── bin/
    ├── greet         # Outil exécutable
    └── monitor       # Outil exécutable
```

---

## 21.3 Créer Votre Bibliothèque

### logging.sh

```bash
cat > ~/bin/lib/logging.sh << 'EOF'
#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $@"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $@"; }
log_error() { echo -e "${RED}[ERROR]${NC} $@" >&2; }
EOF

source ~/bin/lib/logging.sh
```

### utils.sh

```bash
cat > ~/bin/lib/utils.sh << 'EOF'
#!/bin/bash

need_command() {
    command -v "$1" &>/dev/null || {
        echo "Commande requise : $1"
        exit 1
    }
}

need_file() {
    [[ -f "$1" ]] || {
        echo "Fichier requis : $1"
        exit 1
    }
}

need_dir() {
    [[ -d "$1" ]] || {
        echo "Répertoire requis : $1"
        exit 1
    }
}
EOF
```

---

## 21.4 Outil Pratique : git-clean

```bash
cat > ~/bin/git-clean << 'EOF'
#!/bin/bash
set -euo pipefail

DRY_RUN=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        -n|--dry-run) DRY_RUN=true; shift ;;
        *) shift ;;
    esac
done

if $DRY_RUN; then
    echo "[DRY-RUN] Supprimerait :"
fi

git branch --merged main | grep -v "main\|master\|develop" | while read branch; do
    if $DRY_RUN; then
        echo "  Supprimer branche : $branch"
    else
        git branch -d "$branch"
        echo "Supprimé : $branch"
    fi
done

git clean -n -d
EOF

chmod +x ~/bin/git-clean
```

---

## 21.5 Outil Pratique : docker-clean

```bash
cat > ~/bin/docker-clean << 'EOF'
#!/bin/bash
set -euo pipefail

echo "Arrêt de tous les conteneurs..."
docker stop $(docker ps -aq) 2>/dev/null || true

echo "Suppression des conteneurs arrêtés..."
docker container prune -f

echo "Suppression des images inutilisées..."
docker image prune -af

echo "Suppression des réseaux inutilisés..."
docker network prune -f

echo "Suppression du cache de build..."
docker builder prune -af

echo "✅ Nettoyage Docker terminé"
docker system df
EOF

chmod +x ~/bin/docker-clean
```

---

## 21.6 Rendre les Outils Disponibles dans PATH

```bash
# Vérifier si ~/bin est dans PATH
echo $PATH | grep -q "$HOME/bin" && echo "Configuré" || echo "Non configuré"

# Ajouter à PATH (ajouter à ~/.bashrc ou ~/.zshrc)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 21.7 Faire Élargir la Boîte à Outils par l'IA

```bash
# Humain : aide-moi à créer un outil pour analyser les logs d'accès Nginx

# L'IA :
cat > ~/bin/nginx-analyze << 'EOF'
#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage : $0 <fichier_log_acces>"
    exit 1
fi

FILE=$1

echo "=== Analyse Nginx : $FILE ==="
echo ""

echo "Taille du fichier : $(du -h "$FILE" | cut -f1)"
echo "Nombre total de lignes : $(wc -l < "$FILE")"
echo ""

echo "=== Top 10 IPs ==="
awk '{print $1}' "$FILE" | sort | uniq -c | sort -rn | head -10
echo ""

echo "=== Top 10 URLs ==="
awk '{print $7}' "$FILE" | sort | uniq -c | sort -rn | head -10
echo ""

echo "=== Distribution des Codes de Statut ==="
awk '{print $9}' "$FILE" | sort | uniq -c | sort -rn
EOF

chmod +x ~/bin/nginx-analyze
```

---

## 21.8 Amélioration Continue

```bash
# Réviser la boîte à outils annuellement
# - Quels outils sont rarement utilisés ? Supprimer
# - Quels outils peuvent être améliorés ?
# - Quelles tâches répétitives peuvent être automatisées ?

# Versionner votre boîte à outils
cd ~/bin
git init
git add .
git commit -m "Version initiale"
```

---

## 21.9 Exercices

1. Créer votre structure de répertoire ~/bin
2. Écrire les fonctions couramment utilisées dans des bibliothèques réutilisables
3. Écrire un outil pour les tâches que vous répétez quotidiennement
4. Faire créer par l'IA un outil d'analyse de logs Nginx
5. Mettre votre boîte à outils sous contrôle de version Git
