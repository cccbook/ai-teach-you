# 18. Lire et Modifier les Scripts des Autres

---

## 18.1 Pourquoi Lire les Scripts des Autres

- Prendre en charge la maintenance d'un projet
- Utiliser des outils open source
- Déboguer des problèmes
- Apprendre de nouvelles techniques

L'IA rencontre quotidiennement des scripts inconnus, il est donc essentiel d'apprendre à comprendre rapidement les scripts Shell écrits par d'autres.

---

## 18.2 Observation Initiale

### Étape 1 : Vérifier le shebang

```bash
head -1 script.sh
```

```bash
#!/bin/bash      # Utiliser bash
#!/bin/sh        # Utiliser POSIX sh (plus compatible)
```

### Étape 2 : Vérifier les permissions et la taille

```bash
ls -la script.sh
wc -l script.sh
```

### Étape 3 : Vérification rapide de la syntaxe

```bash
bash -n script.sh  # Vérifier la syntaxe uniquement, ne pas exécuter
```

---

## 18.3 Comprendre la Structure

### Structure Typique

```bash
#!/bin/bash
# Commentaire : description du script

# Configuration
set -euo pipefail
VAR="valeur"

# Définitions de fonctions
function help() { ... }

# Flux principal
main() { ... }

# Exécution
main "$@"
```

### Trouver le Flux Principal

```bash
# Vérifier les dernières lignes
tail -20 script.sh

# Trouver les définitions de fonctions
grep -n "^function\|^[[:space:]]*[a-z_]*\(" script.sh
```

---

## 18.4 Commandes d'Analyse Courantes

```bash
# Trouver toutes les définitions de fonctions
grep -n "^[[:space:]]*function" script.sh

# Trouver tous les conditionnels
grep -n "if\|\[\[" script.sh

# Trouver toutes les boucles
grep -n "for\|while\|do\|done" script.sh

# Trouver les substitutions de commandes
grep -n '\$(' script.sh

# Trouver toutes les sorties
grep -n "exit" script.sh
```

---

## 18.5 Vérifications de Sécurité

```bash
# Trouver les commandes dangereuses
grep -n "rm -rf" script.sh
grep -n "sudo" script.sh
grep -n "eval" script.sh

# Vérifier les risques d'injection de variables
grep -n '\$[A-Za-z_][A-Za-z0-9_]*[^"}]' script.sh
```

---

## 18.6 Exercices

1. Analyser un script Shell existant avec `grep` et `awk`
2. Trouver toutes les variables d'un script et comprendre leur rôle
3. Utiliser `bash -n` pour vérifier la syntaxe d'un script
4. Ajouter des commentaires à un script non commenté expliquant chaque section
