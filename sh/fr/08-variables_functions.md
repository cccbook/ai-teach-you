# 8. Variables et Fonctions

---

## 8.1 Bases des Variables

### Assignation de Base

```bash
# Chaine de caracteres
nom="Alice"
salutation="Bonjour, le Monde !"

# Nombre
age=25
compteur=0

# Vide
vide=
vide2=""
```

### Lire les Variables

```bash
echo $nom
echo ${nom}    # Forme recommandee, plus explicite

# Entre guillemets
echo "Mon nom est ${nom}"
```

### Erreurs Courantes

```bash
# Faux : espaces autour de =
nom = "Alice"   # Interprete comme commande

# Faux : pas de guillemets
salutation=Bonjour Monde  # Affiche seulement "Bonjour"

# Correct :
nom="Alice"
salutation="Bonjour Monde"
```

---

## 8.2 L'Art des Guillemets

### Guillemets Doubles `"`
Developpent les variables et les substitutions de commandes

```bash
nom="Alice"
echo "Bonjour, $nom"           # Bonjour, Alice
echo "Aujourd'hui est $(date +%Y)"     # Aujourd'hui est 2026
```

### Guillemets Simples `'`
Sortent litteralement, ne developpent rien

```bash
nom="Alice"
echo 'Bonjour, $nom'           # Bonjour, $nom
echo 'Aujourd'hui est $(date +%Y)'     # Aujourd'hui est $(date +%Y)
```

### Sans Guillemets
Eviter sauf si vous etes sur que la variable ne contient pas d'espaces

---

## 8.3 Variables Speciales

```bash
$0          # Nom du script
$1, $2...   # Parametres positionnels
$#          # Nombre d'arguments
$@          # Tous les arguments (individuels)
$*          # Tous les arguments (en une chaine)
$?          # Code de sortie de la derniere commande
$$          # PID du processus courant
$!          # PID du dernier processus en arriere-plan
$-          # Options du shell courant
```

---

## 8.4 Tableaux

### Utilisation de Base

```bash
# Definir un tableau
couleurs=("rouge" "vert" "bleu")

# Lire les elements
echo ${couleurs[0]}    # rouge
echo ${couleurs[1]}    # vert

# Lire tout
echo ${couleurs[@]}    # rouge vert bleu

# Longueur du tableau
echo ${#couleurs[@]}   # 3
```

### Tableaux Associatifs (Bash 4+)

```bash
declare -A utilisateur
utilisateur["nom"]="Alice"
utilisateur["email"]="alice@example.com"

echo ${utilisateur["nom"]}    # Alice
```

---

## 8.5 Bases des Fonctions

### Definir des Fonctions

```bash
# Methode 1 : mot-cle function
function saluer {
    echo "Bonjour !"
}

# Methode 2 : definition directe (recommande)
saluer() {
    echo "Bonjour !"
}
```

### Parametres de Fonction

```bash
saluer() {
    echo "Bonjour, $1 !"
}

saluer "Alice"    # Bonjour, Alice !
```

### Valeurs de Retour

```bash
# return : pour le code de sortie (0-255)
verifier() {
    if [[ $1 -gt 10 ]]; then
        return 0  # succes
    else
        return 1  # echec
    fi
}

if verifier 15; then
    echo "Superieur a 10"
fi
```

---

## 8.6 Variables Locales

```bash
compteur() {
    local count=0
    ((count++))
    echo $count
}
```

---

## 8.7 Bibliotheques de Fonctions

### Creer une Bibliotheque

```bash
cat > lib.sh << 'EOF'
#!/bin/bash

journal() {
    echo "[$(date +%H:%M:%S)] $@"
}

erreur() {
    echo "[$(date +%H:%M:%S)] ERREUR: $@" >&2
}

confirmer() {
    read -p "$1 (o/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Oo]$ ]]
}
EOF
```

### Utiliser une Bibliotheque

```bash
#!/bin/bash

source lib.sh

journal "Demarrage du processus"
erreur "Quelque chose s'est mal passe"
confirmer "Continuer ?" && echo "Suite du processus"
```

---

## 8.8 Reference Rapide

| Sujet | Syntaxe | Description |
|-------|---------|-------------|
| Assignation | `var=valeur` | Pas d'espaces autour de = |
| Lecture | `$var` ou `${var}` | Utiliser `${var}` |
| Guillemets doubles | `"..."` | Developpent les variables |
| Guillemets simples | `'...'` | Pas de developpement |
| Arguments | `$1`, `$2`, `$@` | Obtenir les parametres |
| Fonction | `nom() { }` | definition recommandee |
| Variable locale | `local var=valeur` | uniquement dans une fonction |
| Tableau | `tab=(a b c)` | indexe et associatif |
| source | `source fichier.sh` | Charger une bibliotheque |

---

## 8.9 Exercices

1. Ecrire un script qui accepte les parametres nom et age, affiche "Bonjour Y, vous avez X ans !"
2. Creer une bibliotheque avec les fonctions `journal` et `erreur`, l'utiliser dans un autre script
3. Ecrire une fonction recursive pour calculer les nombres de Fibonacci
4. Utiliser `mapfile` pour lire un fichier ligne par ligne dans un tableau, puis afficher a l'envers
