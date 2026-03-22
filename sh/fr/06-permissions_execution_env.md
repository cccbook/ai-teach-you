# 6. Permissions, Exécution, Environnement et Configuration

---

## 6.1 `chmod` : L'art des permissions

### Bases des permissions Linux/Unix

```
drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 .
-rw-r--r--  1 ai  staff  4096 Mar 22 10:30 README.md
-rwxr-xr-x  1 ai  staff   128 Mar 22 10:30 script.sh
```

Les 9 caractères sont en trois groupes :
- `rwx` (propriétaire) : lecture, écriture, exécution
- `r-x` (groupe) : lecture, exécution
- `r--` (autres) : lecture seule

### Les deux représentations de chmod

**Numérique (octal)** :

```
r = 4, w = 2, x = 1

rwx = 7, r-x = 5, r-- = 4
```

Combinaisons courantes :
- `777` = rwxrwxrwx (dangereux !)
- `755` = rwxr-xr-x
- `644` = rw-r--r--
- `700` = rwx------
- `600` = rw-------

**Symbolique** :

```bash
chmod u+x script.sh    # Le propriétaire ajoute l'exécution
chmod g-w fichier.txt # Le groupe supprime l'écriture
chmod +x script.sh    # Tout le monde ajoute l'exécution
```

### Utilisation courante de chmod par l'IA

```bash
# Rendre le script exécutable (presque chaque script)
chmod +x script.sh

# Rendre le répertoire traversable
chmod +x ~/projects

# Répertoires modifiables par le groupe
chmod -R g+w projet/
```

---

## 6.2 Exécuter des scripts Shell

### Méthodes d'exécution

```bash
# Méthode 1 : Exécution par chemin (nécessite la permission d'exécution)
./script.sh

# Méthode 2 : Utiliser bash (ne nécessite pas la permission d'exécution)
bash script.sh

# Méthode 3 : Utiliser source (s'exécute dans le shell actuel)
source script.sh
```

### Quand utiliser quoi ?

| Méthode | Quand utiliser | Caractéristiques |
|---------|-----------------|------------------|
| `./script.sh` | Exécution standard | nécessite `chmod +x`, sous-shell |
| `bash script.sh` | Spécifier le shell | pas de permission d'exécution nécessaire |
| `source script.sh` | Définir l'environnement | s'exécute dans le shell actuel |

### Différence clé entre `source` et `./script`

```bash
# Contenu de script.sh : export MA_VAR="bonjour"

# Exécuter avec ./
./script.sh
echo $MA_VAR  # Sortie : (vide) ← dans le sous-shell, la variable est perdue

# Exécuter avec source
source script.sh
echo $MA_VAR  # Sortie : bonjour ← dans le shell actuel, la variable reste
```

---

## 6.3 `export` : Variables d'environnement

```bash
# Définir une variable d'environnement
export NOM="Alice"
export PATH="$PATH:/nouveau/repertoire"

# Afficher toutes les variables d'environnement
export

# Variables courantes
echo $HOME      # Répertoire personnel
echo $USER      # Nom d'utilisateur
echo $PATH      # Chemin de recherche
echo $PWD       # Répertoire actuel
```

### Persister les variables d'environnement

```bash
# Ajouter à ~/.bashrc
echo 'export EDITOR=vim' >> ~/.bashrc

# Appliquer les changements
source ~/.bashrc
```

---

## 6.4 `source` : Charger des fichiers

Équivalent à : coller directement le **contenu du fichier** à la position actuelle et l'exécuter.

### Utilisations courantes

```bash
# Charger l'environnement virtuel
source venv/bin/activate

# Charger le fichier .env
source .env

# Charger une bibliothèque
source ~/scripts/commun.sh
```

### Pratique : Fichiers de configuration modulaires

```bash
# config.sh
export DB_HOST="localhost"
export DB_PORT="5432"

# Utiliser dans d'autres scripts
source config.sh
psql -h $DB_HOST -p $DB_PORT
```

---

## 6.5 `env` : Gestion de l'environnement

```bash
# Afficher toutes les variables d'environnement
env

# Exécuter avec un environnement propre
env -i HOME=/tmp PATH=/bin sh

# Définir des variables et exécuter
env VAR1=valeur1 VAR2=valeur2 ./mon_programme
```

### Trouver des commandes

```bash
which python      # Trouver l'emplacement de la commande
type cd           # Trouver les builtins du shell
whereis gcc       # Trouver tous les fichiers liés
```

---

## 6.6 `sudo` : Élever les privilèges

```bash
# Exécuter en tant que root
sudo rm /var/log/ancien.log

# Exécuter en tant qu'utilisateur spécifique
sudo -u postgres psql

# Afficher ce que vous pouvez faire
sudo -l
```

### Avertissement de danger

```bash
# Ne jamais exécuter ceci !
sudo rm -rf /

# Ne jamais faire ceci !
sudo curl http://site-inconnu.com | sh
```

---

## 6.7 Référence rapide

| Commande | But | Drapeaux courants |
|----------|-----|-------------------|
| `chmod` | Changer les permissions | `+x` ajouter exec, `755` octal, `-R` récursif |
| `chown` | Changer le propriétaire | `utilisateur:groupe`, `-R` récursif |
| `./script` | Exécuter le script (nécessite x) | - |
| `bash script` | Exécuter le script (pas besoin x) | - |
| `source` | Exécuter dans le shell actuel | - |
| `export` | Définir les variables d'environnement | `-n` supprimer |
| `env` | Afficher/gérer l'environnement | `-i` nettoyer |
| `sudo` | Exécuter en tant que root | `-u utilisateur` spécifier utilisateur |

---

## 6.8 Exercices

1. Créer un script, définir les permissions avec `chmod 755`, puis l'exécuter
2. Exécuter le même script de variable d'environnement avec `source` et `./`, observer la différence
3. Utiliser `env -i` pour créer un environnement propre, exécuter `python --version`
4. Créer un fichier `.env`, utiliser `source` pour charger ses variables
