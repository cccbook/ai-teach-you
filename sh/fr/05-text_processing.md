# 5. Traitement de texte

---

## 5.1 La philosophie de traitement de texte de l'IA

Dans le monde de l'IA, **tout est du texte**.

- Le code est du texte
- Les fichiers de configuration sont du texte
- Les logs sont du texte
- JSON, HTML, Markdown sont tous du texte

Donc les commandes de traitement de texte sont le cœur de la boîte à outils de l'IA.

Quand les ingénieurs humains rencontrent des problèmes : "J'ai besoin d'un outil pour gérer ceci..."
Quand l'IA rencontre des problèmes : "Ceci peut être résolu avec `grep | sed | awk` en une seule ligne."

---

## 5.2 `cat` : L'art de lire les fichiers

### Utilisation basique

```bash
# Afficher le contenu du fichier
cat fichier.txt

# Combiner des fichiers
cat partie1.txt partie2.txt > entier.txt

# Afficher les numéros de ligne
cat -n script.sh
```

### Vrai but : combiner et créer

```bash
cat << 'EOF' > nouveau_fichier.txt
Contenu du fichier
Peut écrire plusieurs lignes
EOF
```

---

## 5.3 `head` et `tail` : Voir seulement ce dont vous avez besoin

### `head` : Regarder le début

```bash
# Premières 10 lignes (défaut)
head fichier.txt

# Premières 5 lignes
head -n 5 fichier.txt

# Premiers 100 octets
head -c 100 fichier.txt
```

### `tail` : Regarder la fin

```bash
# Dernières 10 lignes (défaut)
tail fichier.txt

# Dernières 5 lignes
tail -n 5 fichier.txt

# Suivre le fichier en temps réel (le plus courant !)
tail -f /var/log/syslog

# Suivre et filtrer
tail -f app.log | grep --line-buffered ERREUR
```

### Voir une plage de lignes spécifique

```bash
# Voir les lignes 100-150
tail -n +100 fichier.txt | head -n 50
```

---

## 5.4 `wc` : Outil de comptage

```bash
# Compter les lignes
wc -l fichier.txt

# Compter les lignes pour plusieurs fichiers
wc -l *.py

# Compter les fichiers dans un répertoire
ls | wc -l
```

---

## 5.5 `grep` : Le roi de la recherche de texte

### Utilisation basique

```bash
# Rechercher les lignes contenant "erreur"
grep "erreur" log.txt

# Ignorer la casse
grep -i "erreur" log.txt

# Afficher les numéros de ligne
grep -n "erreur" log.txt

# Afficher seulement les noms de fichiers
grep -l "À FAIRE" *.md

# Inverser (lignes ne correspondant pas)
grep -v "debug" log.txt

# Correspondance de mot entier
grep -w "erreur" log.txt
```

### Expressions régulières

```bash
# Correspondance au début
grep "^Erreur" log.txt

# Correspondance à la fin
grep "terminé.$" log.txt

# N'importe quel caractère
grep "e.or" log.txt

# Plage
grep -E "[0-9]{3}-" log.txt
```

### Techniques avancées

```bash
# Recherche récursive
grep -r "À FAIRE" src/

# Seulement une extension spécifique
grep -r "À FAIRE" --include="*.py" src/

# Afficher les lignes de contexte
grep -B 2 -A 2 "ERREUR" log.txt

# Conditions multiples (OU)
grep -E "erreur|avertissement|fatal" log.txt
```

---

## 5.6 `sed` : Outil de remplacement de texte

### Remplacement basique

```bash
# Remplacer la première correspondance
sed 's/ancien/nouveau/' fichier.txt

# Remplacer toutes les correspondances
sed 's/ancien/nouveau/g' fichier.txt

# Remplacement sur place
sed -i 's/ancien/nouveau/g' fichier.txt

# Sauvegarder puis remplacer
sed -i.bak 's/ancien/nouveau/g' fichier.txt
```

### Supprimer des lignes

```bash
# Supprimer les lignes vides
sed '/^$/d' fichier.txt

# Supprimer les lignes de commentaire
sed '/^#/d' fichier.txt

# Supprimer les espaces de fin
sed 's/[[:space:]]*$//' fichier.txt
```

### Exemples pratiques

```bash
# Renommer par lot les extensions (.txt → .md)
for f in *.txt; do
    mv "$f" "$(sed 's/.txt$/.md/' <<< "$f")"
done

# Supprimer les fins de ligne Windows
sed -i 's/\r$//' fichier.txt
```

---

## 5.7 `awk` : Le couteau suisse du traitement de texte

### Concept de base

`awk` traite le texte ligne par ligne, divisant automatiquement en champs ($1, $2, $3...), exécutant des actions spécifiées pour chaque ligne.

### Utilisation basique

```bash
# Division par défaut (espaces)
awk '{print $1}' fichier.txt

# Spécifier le délimiteur
awk -F: '{print $1}' /etc/passwd

# Afficher plusieurs champs
awk -F: '{print $1, $3, $7}' /etc/passwd
```

### Traitement conditionnel

```bash
# Traiter seulement les lignes correspondantes
awk -F: '$3 > 1000 {print $1}' /etc/passwd

# BEGIN et END
awk 'BEGIN {print "Début"} {print} END {print "Terminé"}' fichier.txt
```

### Exemples pratiques

```bash
# Sommer une colonne CSV
awk -F, '{somme += $3} END {print somme}' donnees.csv

# Trouver le maximum
awk 'NR==1 {max=$3} $3>max {max=$3} END {print max}' donnees.csv

# Sortie formatée
awk '{printf "%-20s %10.2f\n", $1, $2}' donnees.txt
```

---

## 5.8 Pratique : Combiner tous les outils

### Scénario : Analyser les logs du serveur

```bash
# 1. Trouver les messages d'erreur
grep -i "erreur" access.log

# 2. Compter les erreurs
grep -ci "erreur" access.log

# 3. Trouver les erreurs les plus courantes
grep "erreur" access.log | awk '{print $NF}' | sort | uniq -c | sort -rn | head

# 4. Compter les requêtes par heure
awk '{print $4}' access.log | cut -d: -f2 | sort | uniq -c
```

### Scénario : Modifier le code par lot

```bash
# Changer "print" en "logger.info" dans tous les .py
find . -name "*.py" -exec sed -i 's/print(/logger.info(/g' {} +

# Changer var en const
find . -name "*.js" -exec sed -i 's/\bvar\b/const/g' {} +
```

---

## 5.9 Référence rapide

| Commande | But | Drapeaux courants |
|----------|-----|-------------------|
| `cat` | Afficher/combiner fichiers | `-n` numéros de ligne |
| `head` | Voir le début du fichier | `-n` lignes, `-c` octets |
| `tail` | Voir la fin du fichier | `-n` lignes, `-f` suivre |
| `wc` | Comptage | `-l` lignes, `-w` mots, `-c` octets |
| `grep` | Recherche de texte | `-i` ignorer, `-n` numéro ligne, `-r` récursif, `-c` compter |
| `sed` | Remplacement de texte | `s/ancien/nouveau/g`, `-i` sur place |
| `awk` | Traitement de champs | `-F` délimiteur, `{print}` action |

---

## 5.10 Exercices

1. Utiliser `head` et `tail` pour voir les lignes 100-120
2. Utiliser `grep` pour trouver tous les utilisateurs avec `/bin/bash` dans /etc/passwd
3. Utiliser `sed` pour remplacer tous les `\r\n` par `\n`
4. Utiliser `awk` pour calculer le max, le min et la moyenne d'un fichier numérique
