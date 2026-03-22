# 10. Analyse d'Arguments et Outils CLI

---

## 10.1 Bases des Arguments de Ligne de Commande

```bash
#!/bin/bash

echo "Script: $0"
echo "Premier argument: $1"
echo "Deuxieme argument: $2"
echo "Troisieme argument: ${3:-defaut}"  # valeur par defaut
echo "Nombre d'arguments: $#"
echo "Tous les arguments: $@"
```

### Execution

```bash
./script.sh foo bar
# Sortie :
# Script: ./script.sh
# Premier argument: foo
# Deuxieme argument: bar
# Troisieme argument: defaut
# Nombre d'arguments: 2
# Tous les arguments: foo bar
```

---

## 10.2 Analyse Simple des Arguments

### Parametres Positionnels

```bash
#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "Utilisation : $0 <fichier>"
    exit 1
fi

FICHIER="$1"

if [[ ! -f "$FICHIER" ]]; then
    echo "Erreur : le fichier n'existe pas"
    exit 1
fi

echo "Traitement de $FICHIER..."
```

### Gestion des Arguments Optionnels

```bash
#!/bin/bash

VERBOSE=false
SORTIE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -o|--output)
            SORTIE="$2"
            shift 2
            ;;
        -*)
            echo "Option inconnue : $1"
            exit 1
            ;;
        *)
            FICHIER="$1"
            shift
            ;;
    esac
done

$VERBOSE && echo "mode verbeux active"
[[ -n "$SORTIE" ]] && echo "Sortie vers : $SORTIE"
```

---

## 10.3 `getopts` : Analyse Standard des Options

```bash
#!/bin/bash

while getopts "hv:o:" opt; do
    case $opt in
        h)
            echo "Information d'aide"
            exit 0
            ;;
        v)
            echo "mode verbeux : $OPTARG"
            ;;
        o)
            echo "fichier de sortie : $OPTARG"
            ;;
        \?)
            echo "Option invalide : -$OPTARG" >&2
            exit 1
            ;;
    esac
done

shift $((OPTIND - 1))

echo "Arguments restants : $@"
```

### Reference du Format des Options

| Format | Signification |
|--------|---------------|
| `getopts "hv:"` | `-h` sans arg, `-v` necessite un arg |
| `OPTARG` | Valeur de l'argument de l'option courante |
| `OPTIND` | Index du prochain argument |

---

## 10.4 Entree Interactive

### `read` : Lire l'Entree Utilisateur

```bash
#!/bin/bash

# Lecture basique
read -p "Entrez votre nom : " nom
echo "Bonjour, $nom"

# Mot de passe (cache)
read -sp "Entrez le mot de passe : " motdepasse
echo

# Lire plusieurs valeurs
read -p "Entrez le nom et l'age : " nom age
echo "$nom a $age ans"

# Delai expire
read -t 5 -p "Entrez dans les 5 secondes : " valeur
```

### Invite de Confirmation

```bash
confirmer() {
    read -p "$1 (o/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Oo]$ ]]
}

if confirmer "Supprimer ce fichier ?"; then
    echo "Suppression..."
fi
```

---

## 10.5 Interface de Menu

```bash
#!/bin/bash

PS3="Selectionnez une operation : "

select choix in "Creer projet" "Supprimer projet" "Quitter"; do
    case $choix in
        "Creer projet")
            echo "Creation..."
            ;;
        "Supprimer projet")
            echo "Suppression..."
            ;;
        "Quitter")
            echo "Au revoir !"
            exit 0
            ;;
        *)
            echo "Choix invalide"
            ;;
    esac
done
```

---

## 10.6 Reference Rapide

| Syntaxe | Description |
|---------|-------------|
| `$0` | Nom du script |
| `$1`, `$2`... | Parametres positionnels |
| `$#` | Nombre d'arguments |
| `${var:-defaut}` | Valeur par defaut |
| `getopts "hv:" opt` | Analyser les options |
| `$OPTARG` | Argument de l'option courante |
| `read -p "invite:" var` | Lire l'entree |
| `read -s var` | Entree cachee (mot de passe) |
| `read -t 5 var` | Delai de 5 secondes |
| `select` | Interface de menu |

---

## 10.7 Exercices

1. Ecrire un outil CLI acceptant `-n` pour le nombre, `-v` pour le mode verbeux
2. Utiliser `getopts` pour analyser les options `-h` (aide), `-o` (fichier de sortie)
3. Ecrire une fonction de confirmation qui ne continue que sur reponse o
4. Creer un menu de calculatrice simple avec `select`
