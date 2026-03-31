# 9. Gestion des Erreurs

---

## 9.1 Pourquoi la Gestion des Erreurs est Importante

Sans gestion des erreurs :
- Apres l'echec d'une commande, continuer avec de mauvaises operations
- Peut supprimer de mauvais fichiers
- Peut ecraser des donnees importantes
- Peut laisser le systeme dans un etat incoherent

Avec gestion des erreurs :
- Arreter immediatement en cas d'erreur
- Fournir des messages d'erreur significatifs
- Nettoyer avant de quitter

---

## 9.2 Codes de Sortie

Chaque commande retourne un code de sortie apres execution :

- `0` : succes
- `non-zero` : echec

```bash
# Verifier le code de sortie de la derniere commande
ls /tmp
echo $?  # Sortie : 0 (si reussi)

ls /inexistant
echo $?  # Sortie : 2 (si echoue)
```

---

## 9.3 `set -e` : Arreter sur Erreur

```bash
#!/bin/bash
set -e

mkdir -p sauvegarde
cp important.txt sauvegarde/  # Si ceci echoue, le script s'arrete ici
rm important.txt            # N'ira pas jusqu'ici
```

### Quand Utiliser

Presque tous les scripts doivent utiliser `set -e` :
- Scripts d'initialisation
- Scripts de deploiement
- Scripts de tests automatises

---

## 9.4 `set -u` : Erreur sur Variables Indefinies

```bash
#!/bin/bash
set -u

echo $variable_indefinie
# Sortie : bash: variable_indefinie: variable non definie
```

### Utilisation Combinee

```bash
#!/bin/bash
set -euo pipefail

# -e : arreter sur erreur
# -u : erreur sur variable non definie
# -o pipefail : le pipe echoue si une commande echoue
```

**C'est l'en-tete standard de script pour l'IA !**

---

## 9.5 `trap` : Gestion Elegantee des Erreurs

### Utilisation de Base

```bash
#!/bin/bash
set -euo pipefail

nettoyer() {
    echo "Nettoyage..."
    rm -f /tmp/fichier_temp
}

trap nettoyer EXIT

# Programme principal
echo "Demarrage du processus..."
```

### Capturer les Erreurs

```bash
#!/bin/bash
set -euo pipefail

gestionnaire_erreur() {
    local code_sortie=$?
    echo "Echec du script a la ligne $1, code de sortie : $code_sortie"
    exit $code_sortie
}

trap 'gestionnaire_erreur $LINENO' ERR
```

---

## 9.6 Fonctions d'Erreur Personnalisees

```bash
#!/bin/bash
set -euo pipefail

die() {
    echo "Echec : $@" >&2
    exit 1
}

warn() {
    echo "Attention : $@"
}

necessite_commande() {
    command -v "$1" &>/dev/null || die "Commande requise : $1"
}

necessite_fichier() {
    [[ -f "$1" ]] || die "Fichier requis : $1"
}
```

---

## 9.7 Reference Rapide

| Commande | Description |
|---------|-------------|
| `$?` | Code de sortie de la derniere commande |
| `set -e` | Arreter sur erreur |
| `set -u` | Erreur sur variable non definie |
| `set -o pipefail` | Pipe echoue si une commande echoue |
| `set -euo pipefail` | Combine (recommande) |
| `trap 'func' EXIT` | Executer a la sortie |
| `trap 'func' ERR` | Executer sur erreur |
| `trap 'func' INT` | Executer sur Ctrl+C |
| `exit 1` | Quitter avec le code d'erreur 1 |

---

## 9.8 Exercices

1. Ecrire un script avec `set -euo pipefail` qui affiche "Erreur survenue" en cas d'echec
2. Creer une fonction `die()` qui affiche un message et quitte
3. Utiliser `trap` pour afficher "Au revoir" quand le script se termine
4. Ecrire un script de deploiement avec retour arriere automatique en cas d'echec
