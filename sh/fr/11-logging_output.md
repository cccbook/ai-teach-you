# 11. Journalisation et Sortie

---

## 11.1 Pourquoi la Journalisation est Importante

Sans journalisation :
- Vous ne savez pas ou en est le script
- Vous ne savez pas pourquoi il a echoue
- Vous ne savez pas ce qu'il a fait en cas de succes

Avec journalisation :
- Vous pouvez suivre la progression
- Vous avez assez d'informations pour deboguer les echecs
- Vous pouvez auditer l'historique d'execution

---

## 11.2 Niveaux de Log de Base

```bash
#!/bin/bash

DEBUG=0
INFO=1
WARN=2
ERROR=3

NIVEAU_LOG=${NIVEAU_LOG:-$INFO}

journal() {
    local niveau=$1
    shift
    local message="$@"
    local horodatage=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [[ $niveau -ge $NIVEAU_LOG ]]; then
        echo "[$horodatage] $message"
    fi
}

journal $DEBUG "Ceci est un debug"
journal $INFO "Ceci est une info"
journal $WARN "Ceci est un avertissement"
journal $ERROR "Ceci est une erreur"
```

---

## 11.3 Sortie en Couleurs

```bash
#!/bin/bash

ROUGE='\033[0;31m'
VERT='\033[0;32m'
JAUNE='\033[1;33m'
BLEU='\033[0;34m'
NC='\033[0m'  # No Color

journal_info() { echo -e "${VERT}[INFO]${NC} $@"; }
journal_warn() { echo -e "${JAUNE}[WARN]${NC} $@"; }
journal_error() { echo -e "${ROUGE}[ERROR]${NC} $@" >&2; }

journal_info "Installation terminee"
journal_warn "Utilisation des valeurs par defaut"
journal_error "Connexion echouee"
```

---

## 11.4 Sortie vers un Fichier

```bash
#!/bin/bash

FICHIER_JOURNAL="/var/log/monapp.log"

journal() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] $@"
    echo "$message"
    echo "$message" >> "$FICHIER_JOURNAL"
}

journal "Application demarree"
```

---

## 11.5 `tee` : Sortie vers l'Ecran et le Fichier

```bash
# Afficher et sauvegarder simultanement
echo "Bonjour" | tee sortie.txt

# Mode ajout
echo "Monde" | tee -a sortie.txt

# Capturer aussi stderr
./script.sh 2>&1 | tee journal.log
```

---

## 11.6 Indicateurs de Progression

### Points Simples

```bash
echo -n "Traitement"
for i in {1..10}; do
    echo -n "."
    sleep 0.2
done
echo " Fait"
```

### Barre de Progression

```bash
afficher_progression() {
    local actuel=$1
    local total=$2
    local largeur=40
    local pourcentage=$((actuel * 100 / total))
    local caracteres=$((largeur * actuel / total))
    
    printf "\r[%s%s] %3d%%" \
        "$(printf '%*s' $caracteres | tr ' ' '=')" \
        "$(printf '%*s' $((largeur - caracteres)) | tr ' ' '-')" \
        "$pourcentage"
    
    [[ $actuel -eq $total ]] && echo
}
```

---

## 11.7 Explication de `2>&1`

```bash
# 1 = stdout, 2 = stderr

# Rediriger stderr vers stdout
commande 2>&1

# Rediriger stdout vers fichier, stderr vers ecran
commande > sortie.txt

# Rediriger les deux vers fichier
commande > sortie.txt 2>&1

# Rediriger les deux vers /dev/null (masquer)
commande > /dev/null 2>&1
```

---

## 11.8 Reference Rapide

| Syntaxe | Description |
|---------|-------------|
| `echo "texte"` | Sortie basique |
| `echo -e "\033[31m"` | Sortie coloree |
| `2>&1` | Rediriger stderr vers stdout |
| `> fichier` | Ecraser le fichier |
| `>> fichier` | Ajouter au fichier |
| `tee fichier` | Sortie et sauvegarde |
| `tee -a fichier` | Mode ajout |
| `/dev/null` | Jeter la sortie |

---

## 11.9 Exercices

1. Ecrire un script qui affiche les messages INFO, WARN, ERROR dans differentes couleurs
2. Utiliser `tee` pour afficher et sauvegarder la sortie dans un fichier journal simultanement
3. Creer un script de traitement de fichiers avec une barre de progression
4. Construire une bibliotheque utilitaire de journalisation qui supporte la sortie vers fichier et les niveaux de log
