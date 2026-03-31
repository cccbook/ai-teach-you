# 3. Opérations sur les fichiers

---

## 3.1 Le modèle mental de l'IA du système de fichiers

Avant d'approfondir chaque commande, comprenez comment l'IA voit le système de fichiers.

Les ingénieurs humains voient généralement le système de fichiers **visuellement** — comme l'Explorateur Windows ou le Finder macOS, comprennant à travers les icônes et les formes de dossiers.

La vue de l'IA est complètement différente :

```
path          = emplacement absolu /home/user/project/src/main.py
relative      = descendre depuis l'emplacement actuel
nodes         = chaque fichier ou répertoire est un "nœud"
attributes    = permissions, taille, horodatages, propriétaire
type          = fichier régulier(-), répertoire(d), lien(l), périphérique(b/c)
```

Quand l'IA exécute `ls -la`, elle voit :

```
drwxr-xr-x  5 ai  staff  170 Mar 22 10:30 .
drwxr-xr-x  3 ai  staff  102 Mar 22 09:00 ..
-rw-r--r--  1 ai  staff  4096 Mar 22 10:30 .env
-rw-r--r--  1 ai  staff  8192 Mar 22 10:31 README.md
drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 src
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 tests
-rw-r--r--  1 ai  staff  2048 Mar 22 10:32 package.json
```

L'IA peut immédiatement lire :
- Lesquels sont des répertoires (`d`)
- Lesquels sont des fichiers cachés (commençant par `.`)
- Qui a quelles permissions
- Les tailles de fichiers (déterminer si fichiers volumineux)
- L'heure de dernière modification

---

## 3.2 `ls` : La commande la plus utilisée de l'IA

Presque avant chaque opération, l'IA exécute `ls` pour confirmer l'état actuel.

### Combinaisons courantes de `ls` de l'IA

```bash
# Liste basique
ls

# Afficher les fichiers cachés (très important !)
ls -a

# Format long (informations détaillées)
ls -l

# Format long + fichiers cachés (le plus courant)
ls -la

# Trier par date de modification (plus récent en premier)
ls -lt

# Trier par date de modification (plus ancien en premier)
ls -ltr

# Tailles lisibles par l'homme (K, M, G)
ls -lh

# Afficher seulement les répertoires
ls -d */

# Afficher récursivement tous les fichiers
ls -R

# Afficher les numéros d'inode (utile pour les liens physiques)
ls -li
```

### Flux de travail réel de l'IA

```bash
cd ~/project && ls -la

# Résultat :
# drwxr-xr-x  5 ai  staff  170 Mar 22 10:30 .
# drwxr-xr-x  3 ai  staff  102 Mar 22 09:00 ..
# -rw-r--r--  1 ai  staff  4096 Mar 22 10:30 .env
# -rw-r--r--  1 ai  staff  8192 Mar 22 10:31 README.md
# drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 src
# drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 tests
# -rw-r--r--  1 ai  staff  2048 Mar 22 10:32 package.json

# Analyse de l'IA : il y a un fichier .env, les répertoires src et tests, package.json
# C'est un projet Node.js
```

---

## 3.3 `cd` : Le répertoire que l'IA n'oublie jamais

### Habitudes de `cd` de l'IA

```bash
# Aller au répertoire personnel
cd ~

# Aller au répertoire précédent (très utile !)
cd -

# Aller au répertoire parent
cd ..

# Entrer dans un sous-répertoire
cd src

# Naviguer dans des chemins profonds (grâce à la complétion Tab)
cd ~/project/backend/api/v2/routes
```

### Le motif `cd` + `&&` de l'IA

C'est l'un des motifs les plus courants de l'IA :

```bash
# D'abord cd, n'exécuter la commande suivante qu'après confirmation du succès
cd ~/project && ls -la
```

### Erreurs courantes

```bash
# Erreur : ne pas confirmer que le répertoire existe
cd inexistant
# Sortie : bash: cd: inexistant: No such file or directory

# Approche de l'IA : vérifier d'abord
[ -d "inexistant" ] && cd inexistant || echo "Le répertoire n'existe pas"
```

---

## 3.4 `mkdir` : L'art de créer des répertoires

### Utilisation basique

```bash
# Créer un seul répertoire
mkdir monprojet

# Créer plusieurs répertoires
mkdir src tests docs

# Créer des répertoires imbriqués (-p est la clé !)
mkdir -p project/src/components project/tests
```

### Pourquoi l'IA utilise presque toujours `-p`

Le drapeau `-p` (parents) signifie :
1. Si le répertoire existe déjà, **pas d'erreur**
2. Si le parent n'existe pas, **le créer automatiquement**

### Motif typique de création de projet de l'IA

```bash
# Créer une structure de projet standard
mkdir -p project/{src,tests,docs,scripts,config}
```

---

## 3.5 `rm` : L'art de la suppression

**Avertissement** : c'est l'une des commandes les plus dangereuses dans Shell.

### Utilisation basique

```bash
# Supprimer un fichier
rm fichier.txt

# Supprimer un répertoire (nécessite -r)
rm -r repertoire/

# Supprimer un répertoire et tout son contenu (dangereux !)
rm -rf repertoire/
```

### Le danger de `rm -rf`

```bash
# Ne jamais exécuter ceci en tant que root !
# rm -rf /

# Si vous ajoutez accidentellement un espace supplémentaire :
rm -rf * 
# (espace) = rm -rf supprime tout dans le répertoire actuel
```

---

## 3.6 `cp` : Copier des fichiers et des répertoires

### Utilisation basique

```bash
# Copier un fichier
cp source.txt destination.txt

# Copier un répertoire (nécessite -r)
cp -r repertoire_source/ repertoire_destination/

# Afficher la progression pendant la copie (-v verbose)
cp -v gros_fichier.iso /sauvegarde/

# Mode interactif (demander avant d'écraser)
cp -i *.py src/
```

### Puissance des jokers

```bash
# Copier tous les fichiers .txt
cp *.txt sauvegarde/

# Copier tous les fichiers image
cp *.{jpg,png,gif,webp} images/
```

---

## 3.7 `mv` : Déplacer et renommer

### Utilisation basique

```bash
# Déplacer un fichier
mv fichier.txt sauvegarde/

# Déplacer et renommer
mv ancien_nom.txt nouveau_nom.txt

# Renommage par lot
for f in *.txt; do
    mv "$f" "${f%.txt}.md"
done
```

---

## 3.8 Référence rapide

| Commande | Utilisation basique | Drapeaux courants | Note de l'IA |
|----------|---------------------|------------------|--------------|
| `ls` | `ls [chemin]` | `-l` long, `-a` cachés, `-h` humain | `ls -la` est toujours bien |
| `cd` | `cd [chemin]` | `-` précédent, `..` parent | `cd xxx &&` est une bonne habitude |
| `mkdir` | `mkdir [dir]` | `-p` imbriqué | presque toujours utiliser `-p` |
| `rm` | `rm [fichier]` | `-r` récursif, `-f` forcer | attention à `rm -rf /*` |
| `cp` | `cp [src] [dst]` | `-r` répertoire, `-i` demander, `-p` préserver | utiliser `-i` pour la sécurité |
| `mv` | `mv [src] [dst]` | `-i` demander, `-n` ne pas écraser | c'est renommer |

---

## 3.9 Exercices

1. Utiliser `mkdir -p` pour créer un répertoire à trois niveaux d'imbrication, puis confirmer avec `tree` ou `find`
2. Copier un gros fichier avec `cp -v` et voir la sortie
3. Renommer par lot 10 fichiers `.txt` en `.md` avec `mv`
4. Supprimer un fichier de test avec `rm -i` pour expérimenter l'invite
