# 7. Contrôle de flux et boucles conditionnelles

---

## 7.1 Combiner des commandes : L'essence de Shell

Les commandes uniques ont des capacités limitées. Ce n'est qu'en les **combinant** que vous pouvez accomplir des tâches complexes.

L'IA est puissante largement parce qu'elle maîtrise ces combinaisons :

```bash
cat access.log | grep "ERREUR" | sort | uniq -c | sort -rn | head -10
```

Cela signifie : "Depuis access.log, trouver les erreurs, compter les occurrences, afficher le top 10"

---

## 7.2 `|` (Pipe) : L'art du flux de données

Le pipe transforme la **sortie** de la commande précédente en **entrée** de la suivante.

```bash
# Trier le contenu d'un fichier
cat non_trie.txt | sort

# Trouver les commandes les plus utilisées
history | awk '{print $2}' | sort | uniq -c | sort -rn | head -10

# Extraire les IP des logs et compter
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -5
```

### Piper stderr

```bash
# Envoyer stderr au pipe
commande1 2>&1 | commande2

# Ou Bash 4+
commande1 |& commande2
```

---

## 7.3 `&&` : Exécuter la suivante seulement si succès

**Seulementsi `commande1` réussit (code de sortie = 0) `commande2` s'exécutera.**

```bash
# Créer le répertoire puis cd dedans
mkdir -p projet && cd projet

# Compiler puis exécuter
gcc -o programme source.c && ./programme

# Télécharger puis extraire
curl -L -o archive.tar.gz http://exemple.com/fichier && tar -xzf archive.tar.gz
```

---

## 7.4 `||` : Exécuter la suivante seulement si échec

**Seulementsi `commande1` échoue (code de sortie ≠ 0) `commande2` s'exécutera.**

```bash
# Créer le fichier s'il n'existe pas
[ -f config.txt ] || echo "Config manquante" > config.txt

# Essayer une façon, se rabattre sur une autre
cd /opt/projet || cd /home/user/projet

# Assurer le succès même en cas d'échec (courant dans les makefiles)
cp fichier.txt fichier.txt.bak || true
```

### Combiner `&&` et `||`

```bash
# Expression conditionnelle
[ -f config ] && echo "Trouvé" || echo "Non trouvé"

# Équivalent à :
if [ -f config ]; then
    echo "Trouvé"
else
    echo "Non trouvé"
fi
```

---

## 7.5 `;` : Exécuter quoiqu'il arrive

```bash
# Les trois s'exécutent
mkdir /tmp/test ; cd /tmp/test ; pwd
```

---

## 7.6 `$()` : Substitution de commande

**Exécuter la commande, remplacer `$()` par sa sortie.**

```bash
# Utilisation basique
echo "Aujourd'hui est $(date +%Y-%m-%d)"
# Sortie : Aujourd'hui est 2026-03-22

# Dans des variables
FICHIERS=$(ls *.txt)

# Obtenir le nom du répertoire
REPERTOIRE=$(dirname /chemin/vers/fichier.txt)
BASE=$(basename /chemin/vers/fichier.txt)

# Calculer
echo "Le résultat est $((10 + 5))"
# Sortie : Le résultat est 15
```

### vs backticks

```bash
# Les deux sont équivalents
echo "Aujourd'hui est $(date +%Y)"
echo "Aujourd'hui est `date +%Y`"

# Mais $() est mieux car il peut s'imbriquer
echo $(echo $(echo imbriqué))
```

---

## 7.7 `[[ ]]` et `[ ]` : Tests conditionnels

### Tests de fichiers

```bash
[[ -f fichier.txt ]]      # Le fichier régulier existe
[[ -d repertoire ]]     # Le répertoire existe
[[ -e chemin ]]           # N'importe quel type existe
[[ -L lien ]]           # Le lien symbolique existe
[[ -r fichier ]]           # Lisible
[[ -w fichier ]]           # Écrivable
[[ -x fichier ]]           # Exécutable
[[ fichier1 -nt fichier2 ]]  # fichier1 est plus récent que fichier2
```

### Tests de chaînes

```bash
[[ -z "$str" ]]        # La chaîne est vide
[[ -n "$str" ]]        # La chaîne n'est pas vide
[[ "$str" == "valeur" ]] # Égal
[[ "$str" =~ motif ]]  # Correspond à l'expression régulière
```

### Tests numériques

```bash
[[ $num -eq 10 ]]      # Égal
[[ $num -ne 10 ]]      # Pas égal
[[ $num -gt 10 ]]      # Supérieur à
[[ $num -lt 10 ]]      # Inférieur à
```

---

## 7.8 `if` : Instructions conditionnelles

```bash
if [[ condition ]]; then
    # faire quelque chose
elif [[ condition2 ]]; then
    # faire autre chose
else
    # alternative
fi
```

### Exemple complet

```bash
#!/bin/bash

FICHIER="config.yaml"

if [[ ! -f "$FICHIER" ]]; then
    echo "Erreur : $FICHIER n'existe pas"
    exit 1
fi

if [[ -r "$FICHIER" ]]; then
    echo "Le fichier est lisible"
else
    echo "Le fichier n'est pas lisible"
fi
```

---

## 7.9 `for` : Boucles

### Syntaxe basique

```bash
for variable in liste; do
    # utiliser $variable
done
```

### Motifs courants de l'IA

```bash
# Traiter tous les fichiers .txt
for fichier in *.txt; do
    echo "Traitement de $fichier"
done

# Plage de nombres
for i in {1..10}; do
    echo "Itération $i"
done

# Tableau
for couleur in rouge vert bleu; do
    echo $couleur
done

# Boucle style C (Bash 3+)
for ((i=0; i<10; i++)); do
    echo $i
done
```

---

## 7.10 `while` : Boucles conditionnelles

```bash
# Lire les lignes
while IFS= read -r ligne; do
    echo "Lu : $ligne"
done < fichier.txt

# Boucle de comptage
compteur=0
while [[ $compteur -lt 10 ]]; do
    echo $compteur
    ((compteur++))
done
```

---

## 7.11 `case` : Correspondance de motifs

```bash
case $ACTION in
    start)
        echo "Démarrage du service..."
        ;;
    stop)
        echo "Arrêt du service..."
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    *)
        echo "Utilisation : $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

### Motifs avec jokers

```bash
case "$fichier" in
    *.txt)
        echo "Fichier texte"
        ;;
    *.jpg|*.png|*.gif)
        echo "Fichier image"
        ;;
    *)
        echo "Type inconnu"
        ;;
esac
```

---

## 7.12 Référence rapide

| Symbole | Nom | Description |
|---------|-----|-------------|
| `\|` | Pipe | Passer la sortie à l'entrée suivante |
| `&&` | ET | Exécuter la suivante seulement si la précédente réussit |
| `\|\|` | OU | Exécuter la suivante seulement si la précédente échoue |
| `;` | Point-virgule | Exécuter quoiqu'il arrive |
| `$()` | Substitution de commande | Exécuter, remplacer par la sortie |
| `[[ ]]` | Test conditionnel | syntaxe de test recommandée |
| `if` | Conditionnel | embranchement basé sur la condition |
| `for` | Boucle de comptage | itérer à travers une liste |
| `while` | Boucle conditionnelle | répéter tant que la condition est vraie |
| `case` | Correspondance de motifs | embranchement multiple |

---

## 7.13 Exercices

1. Utiliser `|` pour combiner `ls`, `grep`, `wc` pour compter les fichiers `.log`
2. Utiliser `&&` pour s'assurer que `cd` réussit avant de continuer
3. Utiliser une boucle `for` pour créer 10 répertoires (rep1 à rep10)
4. Utiliser `while read` pour lire et afficher /etc/hosts
5. Écrire une calculatrice simple avec `case` (add, sous, mul, div)
